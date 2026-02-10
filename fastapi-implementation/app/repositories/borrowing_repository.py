"""
Borrowing repository implementation.

Concrete implementation of IBorrowingRepository using SQLAlchemy.
Handles all borrowing transaction data access operations.
"""

from typing import Any
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.interfaces.repositories import IBorrowingRepository
from app.models import BorrowingRecord, Book, User
from app.enums import BorrowingStatus


class BorrowingRepository(IBorrowingRepository):
    """
    SQLAlchemy implementation of IBorrowingRepository.
    
    Encapsulates all borrowing transaction data access logic.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, borrowing_id: UUID) -> BorrowingRecord | None:
        """Get borrowing by ID with relationships loaded."""
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .options(selectinload(BorrowingRecord.user))
            .where(BorrowingRecord.id == borrowing_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, borrowing_data: dict[str, Any]) -> BorrowingRecord:
        """
        Create new borrowing.
        
        Args:
            borrowing_data: Borrowing fields (user_id, book_id, dates, etc.)
            
        Returns:
            BorrowingRecord: Created borrowing
        """
        borrowing = BorrowingRecord(**borrowing_data)
        self.db.add(borrowing)
        await self.db.flush()
        await self.db.refresh(borrowing)
        return borrowing
    
    async def update(self, borrowing_id: UUID, updates: dict[str, Any]) -> BorrowingRecord:
        """
        Update borrowing.
        
        Args:
            borrowing_id: ID of borrowing to update
            updates: Fields to update
            
        Returns:
            BorrowingRecord: Updated borrowing
            
        Raises:
            ValueError: If borrowing not found
        """
        borrowing = await self.get_by_id(borrowing_id)
        if not borrowing:
            raise ValueError(f"Borrowing {borrowing_id} not found")
        
        for key, value in updates.items():
            if value is not None and hasattr(borrowing, key):
                setattr(borrowing, key, value)
        
        await self.db.flush()
        await self.db.refresh(borrowing)
        return borrowing
    
    async def delete(self, borrowing_id: UUID) -> None:
        """
        Delete borrowing.
        
        Args:
            borrowing_id: ID of borrowing to delete
            
        Raises:
            ValueError: If borrowing not found
        """
        borrowing = await self.get_by_id(borrowing_id)
        if not borrowing:
            raise ValueError(f"Borrowing {borrowing_id} not found")
        
        await self.db.delete(borrowing)
        await self.db.flush()
    
    async def get_user_history(self, user_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """
        Get user's borrowing history.
        
        Args:
            user_id: ID of the user
            limit: Maximum results
            
        Returns:
            list[BorrowingRecord]: Borrowing history
        """
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .where(BorrowingRecord.user_id == user_id)
            .order_by(BorrowingRecord.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_active_borrowings(self, user_id: UUID) -> list[BorrowingRecord]:
        """
        Get user's active borrowings.
        
        Args:
            user_id: ID of the user
            
        Returns:
            list[BorrowingRecord]: Active borrowings
        """
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .where(
                and_(
                    BorrowingRecord.user_id == user_id,
                    BorrowingRecord.status.in_([
                        BorrowingStatus.ACTIVE,
                        BorrowingStatus.EXTENDED,
                        BorrowingStatus.OVERDUE,
                    ])
                )
            )
            .order_by(BorrowingRecord.due_date.asc())
        )
        return list(result.scalars().all())
    
    async def get_due_soon(self, user_id: UUID, days: int = 3) -> list[BorrowingRecord]:
        """
        Get books due soon for a user.
        
        Args:
            user_id: ID of the user
            days: Number of days threshold
            
        Returns:
            list[BorrowingRecord]: Books due within specified days
        """
        threshold = datetime.utcnow() + timedelta(days=days)
        
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .where(
                and_(
                    BorrowingRecord.user_id == user_id,
                    BorrowingRecord.status.in_([BorrowingStatus.ACTIVE, BorrowingStatus.EXTENDED]),
                    BorrowingRecord.due_date <= threshold,
                    BorrowingRecord.due_date >= datetime.utcnow(),
                )
            )
            .order_by(BorrowingRecord.due_date.asc())
        )
        return list(result.scalars().all())
    
    async def get_all_active(self) -> list[BorrowingRecord]:
        """
        Get all active borrowings (admin view).
        
        Returns:
            list[BorrowingRecord]: All active borrowings
        """
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .options(selectinload(BorrowingRecord.user))
            .where(
                BorrowingRecord.status.in_([
                    BorrowingStatus.ACTIVE,
                    BorrowingStatus.EXTENDED,
                    BorrowingStatus.OVERDUE,
                ])
            )
            .order_by(BorrowingRecord.due_date.asc())
        )
        return list(result.scalars().all())
    
    async def get_overdue(self) -> list[BorrowingRecord]:
        """
        Get all overdue borrowings.
        
        Returns:
            list[BorrowingRecord]: Overdue borrowings
        """
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .options(selectinload(BorrowingRecord.user))
            .where(BorrowingRecord.status == BorrowingStatus.OVERDUE)
            .order_by(BorrowingRecord.due_date.asc())
        )
        return list(result.scalars().all())
    
    async def get_book_history(self, book_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """
        Get borrowing history for a book.
        
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
    
    async def detect_overdue(self) -> list[BorrowingRecord]:
        """
        Detect borrowings that should be marked as overdue.
        
        Returns:
            list[BorrowingRecord]: Borrowings to mark as overdue
        """
        now = datetime.utcnow()
        
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.user))
            .options(selectinload(BorrowingRecord.book))
            .where(
                and_(
                    BorrowingRecord.status.in_([BorrowingStatus.ACTIVE, BorrowingStatus.EXTENDED]),
                    BorrowingRecord.due_date < now,
                )
            )
        )
        return list(result.scalars().all())
