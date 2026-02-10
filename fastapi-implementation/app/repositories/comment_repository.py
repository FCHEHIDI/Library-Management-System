"""
Comment repository implementation.

Concrete implementation of ICommentRepository using SQLAlchemy.
Handles all comment/review data access operations.
"""

from typing import Any
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.interfaces.repositories import ICommentRepository
from app.models import Comment
from app.enums import CommentStatus


class CommentRepository(ICommentRepository):
    """
    SQLAlchemy implementation of ICommentRepository.
    
    Encapsulates all comment/review data access logic.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, comment_id: UUID) -> Comment | None:
        """Get comment by ID."""
        return await self.db.get(Comment, comment_id)
    
    async def create(self, comment_data: dict[str, Any]) -> Comment:
        """
        Create new comment.
        
        Args:
            comment_data: Comment fields (user_id, book_id, rating, content, etc.)
            
        Returns:
            Comment: Created comment
        """
        comment = Comment(**comment_data)
        self.db.add(comment)
        await self.db.flush()
        await self.db.refresh(comment)
        return comment
    
    async def update(self, comment_id: UUID, updates: dict[str, Any]) -> Comment:
        """
        Update comment.
        
        Args:
            comment_id: ID of comment to update
            updates: Fields to update
            
        Returns:
            Comment: Updated comment
            
        Raises:
            ValueError: If comment not found
        """
        comment = await self.get_by_id(comment_id)
        if not comment:
            raise ValueError(f"Comment {comment_id} not found")
        
        for key, value in updates.items():
            if value is not None and hasattr(comment, key):
                setattr(comment, key, value)
        
        await self.db.flush()
        await self.db.refresh(comment)
        return comment
    
    async def delete(self, comment_id: UUID) -> None:
        """
        Delete comment.
        
        Args:
            comment_id: ID of comment to delete
            
        Raises:
            ValueError: If comment not found
        """
        comment = await self.get_by_id(comment_id)
        if not comment:
            raise ValueError(f"Comment {comment_id} not found")
        
        await self.db.delete(comment)
        await self.db.flush()
    
    async def get_book_comments(
        self,
        book_id: UUID,
        status: CommentStatus = CommentStatus.APPROVED,
        limit: int = 20,
    ) -> list[Comment]:
        """
        Get comments for a book.
        
        Args:
            book_id: ID of the book
            status: Comment status filter
            limit: Maximum results
            
        Returns:
            list[Comment]: Comments for the book
        """
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.user))
            .where(
                and_(
                    Comment.book_id == book_id,
                    Comment.status == status,
                )
            )
            .order_by(Comment.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_user_comments(self, user_id: UUID, limit: int = 50) -> list[Comment]:
        """
        Get user's comments.
        
        Args:
            user_id: ID of the user
            limit: Maximum results
            
        Returns:
            list[Comment]: User's comments
        """
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.book))
            .where(Comment.user_id == user_id)
            .order_by(Comment.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_pending(self) -> list[Comment]:
        """
        Get pending comments for moderation.
        
        Returns:
            list[Comment]: Pending comments
        """
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.user))
            .options(selectinload(Comment.book))
            .where(Comment.status == CommentStatus.PENDING)
            .order_by(Comment.created_at.asc())
        )
        return list(result.scalars().all())
    
    async def get_flagged(self) -> list[Comment]:
        """
        Get flagged comments.
        
        Returns:
            list[Comment]: Comments with flags
        """
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.user))
            .options(selectinload(Comment.book))
            .where(Comment.flag_count > 0)
            .order_by(Comment.flag_count.desc())
        )
        return list(result.scalars().all())
    
    async def get_auto_hidden(self) -> list[Comment]:
        """
        Get auto-hidden comments (exceeded flag threshold).
        
        Returns:
            list[Comment]: Auto-hidden comments
        """
        result = await self.db.execute(
            select(Comment)
            .options(selectinload(Comment.user))
            .options(selectinload(Comment.book))
            .where(Comment.status == CommentStatus.HIDDEN)
            .order_by(Comment.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def check_user_commented(self, user_id: UUID, book_id: UUID) -> bool:
        """
        Check if user already commented on book.
        
        Args:
            user_id: ID of the user
            book_id: ID of the book
            
        Returns:
            bool: True if user has already commented
        """
        result = await self.db.execute(
            select(Comment)
            .where(
                and_(
                    Comment.user_id == user_id,
                    Comment.book_id == book_id,
                )
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
