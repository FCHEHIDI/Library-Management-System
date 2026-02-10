"""
Book repository implementation.

Concrete implementation of IBookRepository using SQLAlchemy.
Handles all book catalog data access operations.
"""

from typing import Any
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repositories import IBookRepository
from app.models import Book, BorrowingRecord
from app.enums import BookStatus, BookCategory


class BookRepository(IBookRepository):
    """
    SQLAlchemy implementation of IBookRepository.
    
    Encapsulates all book catalog data access logic.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, book_id: UUID) -> Book | None:
        """Get book by ID."""
        return await self.db.get(Book, book_id)
    
    async def get_by_isbn(self, isbn: str) -> Book | None:
        """Get book by ISBN."""
        result = await self.db.execute(
            select(Book).where(Book.isbn == isbn)
        )
        return result.scalar_one_or_none()
    
    async def create(self, book_data: dict[str, Any]) -> Book:
        """
        Create new book.
        
        Args:
            book_data: Book fields (isbn, title, author, etc.)
            
        Returns:
            Book: Created book
        """
        book = Book(**book_data)
        self.db.add(book)
        await self.db.flush()
        await self.db.refresh(book)
        return book
    
    async def update(self, book_id: UUID, updates: dict[str, Any]) -> Book:
        """
        Update book.
        
        Args:
            book_id: ID of book to update
            updates: Fields to update
            
        Returns:
            Book: Updated book
            
        Raises:
            ValueError: If book not found
        """
        book = await self.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        for key, value in updates.items():
            if value is not None and hasattr(book, key):
                setattr(book, key, value)
        
        await self.db.flush()
        await self.db.refresh(book)
        return book
    
    async def delete(self, book_id: UUID) -> None:
        """
        Delete book.
        
        Args:
            book_id: ID of book to delete
            
        Raises:
            ValueError: If book not found
        """
        book = await self.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        await self.db.delete(book)
        await self.db.flush()
    
    async def search(
        self,
        query: str | None = None,
        category: BookCategory | None = None,
        available_only: bool = False,
        min_rating: float = 0.0,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """
        Advanced book search.
        
        Args:
            query: Search term (title, author, ISBN)
            category: Filter by category
            available_only: Only available books
            min_rating: Minimum rating
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
    
    async def get_all(
        self,
        status: BookStatus | None = None,
        category: BookCategory | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """
        Get all books with filters.
        
        Args:
            status: Filter by status
            category: Filter by category
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            tuple[list[Book], int]: (books, total_count)
        """
        conditions = []
        
        if status:
            conditions.append(Book.status == status)
        
        if category:
            conditions.append(Book.category == category)
        
        # Count total
        count_query = select(func.count(Book.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Get books
        books_query = (
            select(Book)
            .order_by(Book.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        if conditions:
            books_query = books_query.where(and_(*conditions))
        
        books_result = await self.db.execute(books_query)
        books = list(books_result.scalars().all())
        
        return books, total
    
    async def get_available_books(self, limit: int = 50) -> list[Book]:
        """Get available books."""
        result = await self.db.execute(
            select(Book)
            .where(Book.is_available == True)
            .order_by(Book.average_rating.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_category(self, category: BookCategory, limit: int = 50) -> list[Book]:
        """Get books by category."""
        result = await self.db.execute(
            select(Book)
            .where(Book.category == category)
            .order_by(Book.average_rating.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_new_arrivals(self, limit: int = 20) -> list[Book]:
        """Get recently added books."""
        result = await self.db.execute(
            select(Book)
            .order_by(Book.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_trending(self, days: int = 30, limit: int = 10) -> list[Book]:
        """
        Get trending books (most borrowed recently).
        
        Args:
            days: Time window in days
            limit: Maximum results
            
        Returns:
            list[Book]: Trending books
        """
        since = datetime.utcnow() - timedelta(days=days)
        
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
    
    async def get_popular(self, limit: int = 10) -> list[Book]:
        """Get most borrowed books (all-time)."""
        result = await self.db.execute(
            select(Book)
            .order_by(Book.total_borrowings.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def check_isbn_exists(
        self,
        isbn: str,
        exclude_id: UUID | None = None,
    ) -> bool:
        """
        Check if ISBN exists.
        
        Args:
            isbn: ISBN to check
            exclude_id: Book ID to exclude (for updates)
            
        Returns:
            bool: True if exists
        """
        query = select(Book).where(Book.isbn == isbn)
        
        if exclude_id:
            query = query.where(Book.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
