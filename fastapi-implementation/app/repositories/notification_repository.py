"""
Notification repository implementation.

Concrete implementation of INotificationRepository using SQLAlchemy.
Handles all notification data access operations.
"""

from typing import Any
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repositories import INotificationRepository
from app.models import Notification


class NotificationRepository(INotificationRepository):
    """
    SQLAlchemy implementation of INotificationRepository.
    
    Encapsulates all notification data access logic.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        """Get notification by ID."""
        return await self.db.get(Notification, notification_id)
    
    async def create(self, notification_data: dict[str, Any]) -> Notification:
        """
        Create new notification.
        
        Args:
            notification_data: Notification fields (user_id, message, title, etc.)
            
        Returns:
            Notification: Created notification
        """
        notification = Notification(**notification_data)
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification
    
    async def update(self, notification_id: UUID, updates: dict[str, Any]) -> Notification:
        """
        Update notification.
        
        Args:
            notification_id: ID of notification to update
            updates: Fields to update
            
        Returns:
            Notification: Updated notification
            
        Raises:
            ValueError: If notification not found
        """
        notification = await self.get_by_id(notification_id)
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")
        
        for key, value in updates.items():
            if value is not None and hasattr(notification, key):
                setattr(notification, key, value)
        
        await self.db.flush()
        await self.db.refresh(notification)
        return notification
    
    async def delete(self, notification_id: UUID) -> None:
        """
        Delete notification.
        
        Args:
            notification_id: ID of notification to delete
            
        Raises:
            ValueError: If notification not found
        """
        notification = await self.get_by_id(notification_id)
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")
        
        await self.db.delete(notification)
        await self.db.flush()
    
    async def get_user_unread(self, user_id: UUID, limit: int = 50) -> list[Notification]:
        """
        Get user's unread notifications.
        
        Args:
            user_id: ID of the user
            limit: Maximum results
            
        Returns:
            list[Notification]: Unread notifications
        """
        result = await self.db.execute(
            select(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False,
                )
            )
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_user_history(self, user_id: UUID, limit: int = 100) -> list[Notification]:
        """
        Get user's notification history.
        
        Args:
            user_id: ID of the user
            limit: Maximum results
            
        Returns:
            list[Notification]: All notifications
        """
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def mark_as_read(self, notification_id: UUID) -> Notification:
        """
        Mark notification as read.
        
        Args:
            notification_id: ID of notification
            
        Returns:
            Notification: Updated notification
        """
        notification = await self.get_by_id(notification_id)
        if not notification:
            raise ValueError(f"Notification {notification_id} not found")
        
        notification.mark_as_read()
        
        await self.db.flush()
        await self.db.refresh(notification)
        return notification
    
    async def mark_multiple_as_read(self, notification_ids: list[UUID]) -> int:
        """
        Mark multiple notifications as read.
        
        Args:
            notification_ids: List of notification IDs
            
        Returns:
            int: Number of notifications marked as read
        """
        count = 0
        
        for notification_id in notification_ids:
            try:
                await self.mark_as_read(notification_id)
                count += 1
            except ValueError:
                # Skip if notification not found
                continue
        
        return count
    
    async def clear_user_read(self, user_id: UUID) -> int:
        """
        Clear user's read notifications.
        
        Args:
            user_id: ID of the user
            
        Returns:
            int: Number of notifications cleared
        """
        result = await self.db.execute(
            select(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == True,
                )
            )
        )
        
        notifications = result.scalars().all()
        count = len(notifications)
        
        for notification in notifications:
            await self.db.delete(notification)
        
        await self.db.flush()
        
        return count
    
    async def clear_old(self, days: int = 30) -> int:
        """
        Clear old read notifications.
        
        Args:
            days: Age threshold in days
            
        Returns:
            int: Number of notifications cleared
        """
        threshold = datetime.utcnow() - timedelta(days=days)
        
        result = await self.db.execute(
            select(Notification)
            .where(
                and_(
                    Notification.is_read == True,
                    Notification.created_at < threshold,
                )
            )
        )
        
        notifications = result.scalars().all()
        count = len(notifications)
        
        for notification in notifications:
            await self.db.delete(notification)
        
        await self.db.flush()
        
        return count
