"""
Library domain class - CATALOG MANAGEMENT (12 methods).
REAL implementations with database interactions.
Central coordinator for library operations.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Book, BorrowingRecord, User
from app.enums import BookStatus, BorrowingStatus, BookCategory


class Library:
    """
    Library domain operations (Catalog management).
    
    Central coordinator for library-wide operations:
    - Book catalog searches
    - Availability checks
    - Statistics and analytics
    - System-wide queries
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize Library domain.
        
        Args:
            db: Database session
        """
        self.db = db
    
    # ========== CATALOG SEARCHES (5 methods) ==========
    
    async def search_books(
        self,
        query: str | None = None,
        category: BookCategory | None = None,
        available_only: bool = False,
        min_rating: float = 0.0,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """
        Advanced book search - REAL IMPLEMENTATION.
        
        Args:
            query: Search term (title or author)
            category: Filter by category
            available_only: Only available books
            min_rating: Minimum rating filter
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            tuple[list[Book], int]: (books, total_count)
        """
        conditions = []
        
        if query:
            conditions.append(
                or_(
                    Book.title.ilike(f"%{query}%"),
                    Book.author.ilike(f"%{query}%"),
                    Book.isbn.ilike(f"%{query}%"),
                )
            )
        
        if category:
            conditions.append(Book.category == category)
        
        if available_only:
            conditions.append(Book.is_available == True)
        
        if min_rating > 0:
            conditions.append(Book.average_rating >= min_rating)
        
        # Count total
        count_query = select(func.count(Book.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Get books
        books_query = (
            select(Book)
            .order_by(Book.average_rating.desc(), Book.title.asc())
            .limit(limit)
            .offset(offset)
        )
        
        if conditions:
            books_query = books_query.where(and_(*conditions))
        
        books_result = await self.db.execute(books_query)
        books = list(books_result.scalars().all())
        
        return books, total
    
    async def get_book_by_isbn(
        self,
        isbn: str,
    ) -> Book | None:
        """
        Find book by ISBN - REAL IMPLEMENTATION.
        
        Args:
            isbn: ISBN number
            
        Returns:
            Book | None: Book or None
        """
        result = await self.db.execute(
            select(Book).where(Book.isbn == isbn)
        )
        
        return result.scalar_one_or_none()
    
    async def get_books_by_category(
        self,
        category: BookCategory,
        limit: int = 50,
    ) -> list[Book]:
        """
        Get books by category - REAL IMPLEMENTATION.
        
        Args:
            category: Book category
            limit: Maximum results
            
        Returns:
            list[Book]: Books in category
        """
        result = await self.db.execute(
            select(Book)
            .where(Book.category == category)
            .order_by(Book.average_rating.desc())
            .limit(limit)
        )
        
        return list(result.scalars().all())
    
    async def get_new_arrivals(
        self,
        limit: int = 20,
    ) -> list[Book]:
        """
        Get recently added books - REAL IMPLEMENTATION.
        
        Args:
            limit: Maximum results
            
        Returns:
            list[Book]: Newest books
        """
        result = await self.db.execute(
            select(Book)
            .order_by(Book.created_at.desc())
            .limit(limit)
        )
        
        return list(result.scalars().all())
    
    async def get_trending_books(
        self,
        days: int = 30,
        limit: int = 10,
    ) -> list[Book]:
        """
        Get trending books (most borrowed recently) - REAL IMPLEMENTATION.
        
        Args:
            days: Time window in days
            limit: Maximum results
            
        Returns:
            list[Book]: Trending books
        """
        since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Count borrowings per book in time window
        result = await self.db.execute(
            select(Book, func.count(BorrowingRecord.id).label('recent_count'))
            .join(BorrowingRecord, Book.id == BorrowingRecord.book_id)
            .where(BorrowingRecord.created_at >= since)
            .group_by(Book.id)
            .order_by(func.count(BorrowingRecord.id).desc())
            .limit(limit)
        )
        
        books = [row[0] for row in result.all()]
        
        return books
    
    # ========== AVAILABILITY CHECKS (2 methods) ==========
    
    async def check_availability(
        self,
        book_id: UUID,
    ) -> dict:
        """
        Check book availability - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            
        Returns:
            dict: Availability details
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            return {
                "available": False,
                "reason": "Book not found",
            }
        
        if book.is_available:
            return {
                "available": True,
                "book_id": str(book_id),
                "title": book.title,
                "category": book.category.value,
                "status": book.status.value,
            }
        
        # Find current borrowing
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.user))
            .where(
                and_(
                    BorrowingRecord.book_id == book_id,
                    BorrowingRecord.status.in_([
                        BorrowingStatus.ACTIVE,
                        BorrowingStatus.EXTENDED,
                        BorrowingStatus.OVERDUE,
                    ])
                )
            )
        )
        
        current = result.scalar_one_or_none()
        
        if current:
            return {
                "available": False,
                "reason": "Currently borrowed",
                "due_date": current.due_date.isoformat(),
                "days_until_available": (current.due_date - datetime.utcnow()).days,
            }
        
        return {
            "available": False,
            "reason": f"Book status: {book.status.value}",
        }
    
    async def get_available_copies(
        self,
        isbn: str,
    ) -> int:
        """
        Count available copies by ISBN - REAL IMPLEMENTATION.
        
        Args:
            isbn: ISBN number
            
        Returns:
            int: Number of available copies
        """
        result = await self.db.execute(
            select(func.count(Book.id))
            .where(
                and_(
                    Book.isbn == isbn,
                    Book.is_available == True,
                )
            )
        )
        
        return result.scalar() or 0
    
    # ========== STATISTICS (3 methods) ==========
    
    async def get_library_statistics(self) -> dict:
        """
        Get library-wide statistics - REAL IMPLEMENTATION.
        
        Returns:
            dict: Library statistics
        """
        # Total books
        total_books_result = await self.db.execute(
            select(func.count(Book.id))
        )
        total_books = total_books_result.scalar()
        
        # Available books
        available_result = await self.db.execute(
            select(func.count(Book.id)).where(Book.is_available == True)
        )
        available = available_result.scalar()
        
        # Active borrowings
        active_result = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(
                BorrowingRecord.status.in_([
                    BorrowingStatus.ACTIVE,
                    BorrowingStatus.EXTENDED,
                    BorrowingStatus.OVERDUE,
                ])
            )
        )
        active = active_result.scalar()
        
        # Overdue count
        overdue_result = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(BorrowingRecord.status == BorrowingStatus.OVERDUE)
        )
        overdue = overdue_result.scalar()
        
        # Total users
        users_result = await self.db.execute(
            select(func.count(User.id))
        )
        total_users = users_result.scalar()
        
        return {
            "total_books": total_books,
            "available_books": available,
            "borrowed_books": total_books - available,
            "active_borrowings": active,
            "overdue_borrowings": overdue,
            "total_users": total_users,
            "utilization_rate": round((total_books - available) / total_books * 100, 2) if total_books > 0 else 0,
        }
    
    async def get_category_statistics(self) -> list[dict]:
        """
        Get statistics per category - REAL IMPLEMENTATION.
        
        Returns:
            list[dict]: Category statistics
        """
        result = await self.db.execute(
            select(
                Book.category,
                func.count(Book.id).label('total'),
                func.sum(func.cast(Book.is_available, type_=func.INTEGER)).label('available'),
                func.avg(Book.average_rating).label('avg_rating'),
            )
            .group_by(Book.category)
        )
        
        stats = []
        for row in result.all():
            category, total, available, avg_rating = row
            stats.append({
                "category": category.value,
                "total_books": total,
                "available": available or 0,
                "borrowed": total - (available or 0),
                "average_rating": round(avg_rating or 0, 2),
            })
        
        return stats
    
    async def get_popular_books(
        self,
        limit: int = 10,
    ) -> list[dict]:
        """
        Get most borrowed books - REAL IMPLEMENTATION.
        
        Args:
            limit: Maximum results
            
        Returns:
            list[dict]: Popular books with stats
        """
        result = await self.db.execute(
            select(Book)
            .order_by(Book.total_borrowings.desc())
            .limit(limit)
        )
        
        books = result.scalars().all()
        
        popular = []
        for book in books:
            popular.append({
                "id": str(book.id),
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "total_borrowings": book.total_borrowings,
                "average_rating": book.average_rating,
                "is_available": book.is_available,
            })
        
        return popular
    
    # ========== CATALOG VALIDATION (2 methods) ==========
    
    async def validate_isbn_unique(
        self,
        isbn: str,
        exclude_id: UUID | None = None,
    ) -> bool:
        """
        Validate ISBN uniqueness - REAL IMPLEMENTATION.
        
        Args:
            isbn: ISBN to check
            exclude_id: Book ID to exclude (for updates)
            
        Returns:
            bool: True if unique
        """
        query = select(Book).where(Book.isbn == isbn)
        
        if exclude_id:
            query = query.where(Book.id != exclude_id)
        
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        return existing is None
    
    async def get_book_borrowing_history(
        self,
        book_id: UUID,
        limit: int = 50,
    ) -> list[BorrowingRecord]:
        """
        Get borrowing history for a book - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            limit: Maximum results
            
        Returns:
            list[BorrowingRecord]: Borrowing history
        """
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.user))
            .where(BorrowingRecord.book_id == book_id)
            .order_by(BorrowingRecord.created_at.desc())
            .limit(limit)
        )
        
        return list(result.scalars().all())
