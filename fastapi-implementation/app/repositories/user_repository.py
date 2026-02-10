"""
User repository implementation.

Concrete implementation of IUserRepository using SQLAlchemy.
Handles all user data access operations.
"""

from typing import Any
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repositories import IUserRepository
from app.models import User
from app.enums import UserStatus


class UserRepository(IUserRepository):
    """
    SQLAlchemy implementation of IUserRepository.
    
    Follows Repository pattern: encapsulates data access logic.
    Domain layer depends on IUserRepository interface, not this class.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        return await self.db.get(User, user_id)
    
    async def get_by_username(self, username: str) -> User | None:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user_data: dict[str, Any]) -> User:
        """
        Create new user.
        
        Args:
            user_data: User fields (username, email, hashed_password, etc.)
            
        Returns:
            User: Created user
        """
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update(self, user_id: UUID, updates: dict[str, Any]) -> User:
        """
        Update user.
        
        Args:
            user_id: ID of user to update
            updates: Fields to update
            
        Returns:
            User: Updated user
            
        Raises:
            ValueError: If user not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        for key, value in updates.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user_id: UUID) -> None:
        """
        Delete user.
        
        Args:
            user_id: ID of user to delete
            
        Raises:
            ValueError: If user not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        await self.db.delete(user)
        await self.db.flush()
    
    async def get_all(
        self,
        status: UserStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        """
        Get all users with optional filters.
        
        Args:
            status: Filter by status
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            tuple[list[User], int]: (users, total_count)
        """
        conditions = []
        
        if status:
            conditions.append(User.status == status)
        
        # Count total
        count_query = select(func.count(User.id))
        if conditions:
            count_query = count_query.where(and_(*conditions))
        
        count_result = await self.db.execute(count_query)
        total = count_result.scalar()
        
        # Get users
        users_query = (
            select(User)
            .order_by(User.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        if conditions:
            users_query = users_query.where(and_(*conditions))
        
        users_result = await self.db.execute(users_query)
        users = list(users_result.scalars().all())
        
        return users, total
    
    async def get_suspended_users(self) -> list[User]:
        """Get all suspended users."""
        result = await self.db.execute(
            select(User)
            .where(User.status == UserStatus.SUSPENDED)
            .order_by(User.suspension_end.asc())
        )
        return list(result.scalars().all())
    
    async def check_username_exists(
        self,
        username: str,
        exclude_id: UUID | None = None,
    ) -> bool:
        """
        Check if username exists.
        
        Args:
            username: Username to check
            exclude_id: User ID to exclude (for updates)
            
        Returns:
            bool: True if exists
        """
        query = select(User).where(User.username == username)
        
        if exclude_id:
            query = query.where(User.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def check_email_exists(
        self,
        email: str,
        exclude_id: UUID | None = None,
    ) -> bool:
        """
        Check if email exists.
        
        Args:
            email: Email to check
            exclude_id: User ID to exclude (for updates)
            
        Returns:
            bool: True if exists
        """
        query = select(User).where(User.email == email)
        
        if exclude_id:
            query = query.where(User.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
