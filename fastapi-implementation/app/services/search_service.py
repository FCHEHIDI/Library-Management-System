"""
Search service implementation.

Concrete implementation of ISearchService.
Provides advanced search capabilities including recommendations.
"""

from uuid import UUID

from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.services import ISearchService
from app.interfaces.repositories import IBookRepository, IBorrowingRepository
from app.models import Book, BorrowingRecord
from app.enums import BookCategory


class SearchService(ISearchService):
    """
    Advanced search service.
    
    Provides full-text search, filtering, and recommendation features.
    Can be extended with Elasticsearch for production use.
    """
    
    def __init__(
        self,
        db: AsyncSession,
        book_repo: IBookRepository,
        borrowing_repo: IBorrowingRepository,
    ):
        """
        Initialize search service.
        
        Args:
            db: Database session
            book_repo: Book repository
            borrowing_repo: Borrowing repository
        """
        self.db = db
        self.book_repo = book_repo
        self.borrowing_repo = borrowing_repo
    
    async def search_books(
        self,
        query: str,
        filters: dict[str, any] | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict], int]:
        """
        Full-text search for books.
        
        Searches across: title, author, ISBN, description.
        
        Args:
            query: Search query string
            filters: Optional filters (category, min_rating, available_only)
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            tuple[list[dict], int]: (results as dicts, total_count)
        """
        filters = filters or {}
        
        # Extract filter parameters
        category = filters.get("category")
        min_rating = filters.get("min_rating", 0.0)
        available_only = filters.get("available_only", False)
        
        # Use repository search
        books, total = await self.book_repo.search(
            query=query,
            category=BookCategory[category] if category else None,
            available_only=available_only,
            min_rating=min_rating,
            limit=limit,
            offset=offset,
        )
        
        # Convert to dicts
        results = [
            {
                "id": str(book.id),
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category.value,
                "average_rating": book.average_rating,
                "is_available": book.is_available,
                "total_borrowings": book.total_borrowings,
            }
            for book in books
        ]
        
        return results, total
    
    async def search_by_author(
        self,
        author: str,
        limit: int = 20,
    ) -> list[dict]:
        """
        Search books by author name.
        
        Args:
            author: Author name (partial match)
            limit: Maximum results
            
        Returns:
            list[dict]: Matching books
        """
        result = await self.db.execute(
            select(Book)
            .where(Book.author.ilike(f"%{author}%"))
            .order_by(Book.average_rating.desc())
            .limit(limit)
        )
        
        books = result.scalars().all()
        
        return [
            {
                "id": str(book.id),
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category.value,
                "average_rating": book.average_rating,
                "is_available": book.is_available,
            }
            for book in books
        ]
    
    async def search_by_isbn(
        self,
        isbn: str,
    ) -> dict | None:
        """
        Search book by ISBN (exact match).
        
        Args:
            isbn: ISBN number
            
        Returns:
            dict | None: Book details or None
        """
        book = await self.book_repo.get_by_isbn(isbn)
        
        if not book:
            return None
        
        return {
            "id": str(book.id),
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "category": book.category.value,
            "publisher": book.publisher,
            "year_published": book.year_published,
            "average_rating": book.average_rating,
            "total_ratings": book.total_ratings,
            "total_borrowings": book.total_borrowings,
            "is_available": book.is_available,
            "status": book.status.value,
        }
    
    async def get_recommendations(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[dict]:
        """
        Get book recommendations for user.
        
        Recommendation algorithm:
        1. Find categories user has borrowed
        2. Find highly-rated books in those categories
        3. Exclude books user has already borrowed
        4. Sort by rating and popularity
        
        Args:
            user_id: ID of the user
            limit: Maximum recommendations
            
        Returns:
            list[dict]: Recommended books
        """
        # Get user's borrowing history
        user_borrowings = await self.borrowing_repo.get_user_history(user_id, limit=100)
        
        if not user_borrowings:
            # New user - return popular books
            return await self._get_popular_recommendations(limit)
        
        # Extract borrowed book IDs
        borrowed_book_ids = [b.book_id for b in user_borrowings]
        
        # Find categories user has borrowed
        result = await self.db.execute(
            select(Book.category, func.count(Book.id))
            .join(BorrowingRecord, Book.id == BorrowingRecord.book_id)
            .where(BorrowingRecord.user_id == user_id)
            .group_by(Book.category)
            .order_by(func.count(Book.id).desc())
            .limit(3)
        )
        
        preferred_categories = [row[0] for row in result.all()]
        
        if not preferred_categories:
            return await self._get_popular_recommendations(limit)
        
        # Find highly-rated books in preferred categories
        # excluding already borrowed books
        result = await self.db.execute(
            select(Book)
            .where(
                and_(
                    Book.category.in_(preferred_categories),
                    Book.id.notin_(borrowed_book_ids),
                    Book.average_rating >= 3.5,
                )
            )
            .order_by(
                desc(Book.average_rating),
                desc(Book.total_borrowings)
            )
            .limit(limit)
        )
        
        books = result.scalars().all()
        
        return [
            {
                "id": str(book.id),
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category.value,
                "average_rating": book.average_rating,
                "total_ratings": book.total_ratings,
                "is_available": book.is_available,
                "reason": f"Based on your interest in {book.category.value} books",
            }
            for book in books
        ]
    
    async def get_similar_books(
        self,
        book_id: UUID,
        limit: int = 5,
    ) -> list[dict]:
        """
        Get similar books (same author, category, etc.).
        
        Args:
            book_id: ID of the reference book
            limit: Maximum results
            
        Returns:
            list[dict]: Similar books
        """
        book = await self.book_repo.get_by_id(book_id)
        
        if not book:
            return []
        
        # Find books by same author OR same category
        result = await self.db.execute(
            select(Book)
            .where(
                and_(
                    Book.id != book_id,
                    or_(
                        Book.author == book.author,
                        Book.category == book.category,
                    ),
                )
            )
            .order_by(
                # Prioritize same author
                desc(Book.author == book.author),
                desc(Book.average_rating),
            )
            .limit(limit)
        )
        
        books = result.scalars().all()
        
        return [
            {
                "id": str(b.id),
                "isbn": b.isbn,
                "title": b.title,
                "author": b.author,
                "category": b.category.value,
                "average_rating": b.average_rating,
                "is_available": b.is_available,
                "similarity": "Same author" if b.author == book.author else "Same category",
            }
            for b in books
        ]
    
    async def _get_popular_recommendations(self, limit: int) -> list[dict]:
        """
        Get popular books as fallback recommendations.
        
        Args:
            limit: Maximum results
            
        Returns:
            list[dict]: Popular books
        """
        books = await self.book_repo.get_popular(limit=limit)
        
        return [
            {
                "id": str(book.id),
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "category": book.category.value,
                "average_rating": book.average_rating,
                "total_borrowings": book.total_borrowings,
                "is_available": book.is_available,
                "reason": "Popular with other readers",
            }
            for book in books
        ]
