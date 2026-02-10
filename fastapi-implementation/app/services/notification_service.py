"""
Notification service implementation.

Concrete implementation of INotificationService.
Handles multi-channel notification delivery (in-app, email, SMS).
"""

from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.interfaces.services import INotificationService
from app.interfaces.repositories import INotificationRepository, IUserRepository, IBorrowingRepository
from app.models import Notification, User, BorrowingRecord
from app.enums import NotificationType, NotificationPriority, UserStatus, BorrowingStatus
from app.policies import FEE_POLICIES


class NotificationService(INotificationService):
    """
    Multi-channel notification service.
    
    Routes notifications based on priority:
    - NORMAL: In-app only
    - IMPORTANT: In-app + Email
    - URGENT: In-app + Email + SMS
    """
    
    def __init__(
        self,
        db: AsyncSession,
        notification_repo: INotificationRepository,
        user_repo: IUserRepository,
        borrowing_repo: IBorrowingRepository,
    ):
        """
        Initialize notification service.
        
        Args:
            db: Database session
            notification_repo: Notification repository
            user_repo: User repository
            borrowing_repo: Borrowing repository
        """
        self.db = db
        self.notification_repo = notification_repo
        self.user_repo = user_repo
        self.borrowing_repo = borrowing_repo
    
    async def send_notification(
        self,
        user_id: UUID,
        message: str,
        title: str,
        notification_type: NotificationType,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        related_entity_type: str | None = None,
        related_entity_id: str | None = None,
    ) -> None:
        """
        Send notification with automatic channel selection.
        
        Args:
            user_id: ID of recipient user
            message: Notification message
            title: Notification title
            notification_type: Type of notification
            priority: Priority level (determines channels)
            related_entity_type: Related entity type (book, borrowing, etc.)
            related_entity_id: Related entity ID
        """
        # Create in-app notification (always)
        notification_data = {
            "user_id": user_id,
            "message": message,
            "title": title,
            "type": notification_type,
            "priority": priority,
            "related_entity_type": related_entity_type,
            "related_entity_id": related_entity_id,
        }
        
        notification = await self.notification_repo.create(notification_data)
        
        # Get user for email/SMS
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return
        
        # Send email for IMPORTANT and URGENT
        if priority in [NotificationPriority.IMPORTANT, NotificationPriority.URGENT]:
            if notification.should_send_email:
                await self._send_email(user, title, message)
                notification.email_sent_at = datetime.utcnow()
        
        # Send SMS for URGENT only
        if priority == NotificationPriority.URGENT:
            if notification.should_send_sms:
                await self._send_sms(user, message)
                notification.sms_sent_at = datetime.utcnow()
        
        await self.db.commit()
    
    async def send_email_notification(
        self,
        user_id: UUID,
        subject: str,
        body: str,
    ) -> bool:
        """
        Send email notification directly.
        
        Args:
            user_id: ID of recipient user
            subject: Email subject
            body: Email body
            
        Returns:
            bool: True if sent successfully
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        return await self._send_email(user, subject, body)
    
    async def send_sms_notification(
        self,
        user_id: UUID,
        message: str,
    ) -> bool:
        """
        Send SMS notification directly.
        
        Args:
            user_id: ID of recipient user
            message: SMS message
            
        Returns:
            bool: True if sent successfully
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        return await self._send_sms(user, message)
    
    async def send_broadcast(
        self,
        message: str,
        title: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> int:
        """
        Send notification to all active users.
        
        Args:
            message: Notification message
            title: Notification title
            priority: Priority level
            
        Returns:
            int: Number of notifications sent
        """
        # Get all active users
        users, _ = await self.user_repo.get_all(status=UserStatus.ACTIVE)
        
        count = 0
        for user in users:
            await self.send_notification(
                user_id=user.id,
                message=message,
                title=title,
                notification_type=NotificationType.GENERAL,
                priority=priority,
            )
            count += 1
        
        return count
    
    async def send_due_soon_reminders(self, days: int = 3) -> int:
        """
        Send reminders for books due soon.
        
        Args:
            days: Days threshold (books due within this period)
            
        Returns:
            int: Number of reminders sent
        """
        threshold = datetime.utcnow() + timedelta(days=days)
        
        # Find borrowings due soon
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.book))
            .where(
                and_(
                    BorrowingRecord.status.in_([BorrowingStatus.ACTIVE, BorrowingStatus.EXTENDED]),
                    BorrowingRecord.due_date <= threshold,
                    BorrowingRecord.due_date >= datetime.utcnow(),
                )
            )
        )
        
        due_soon = list(result.scalars().all())
        count = 0
        
        for borrowing in due_soon:
            days_left = (borrowing.due_date - datetime.utcnow()).days
            
            await self.send_notification(
                user_id=borrowing.user_id,
                message=f"Your book '{borrowing.book.title}' is due in {days_left} days! Please return it to avoid late fees.",
                title="Book Due Soon",
                notification_type=NotificationType.DUE_SOON_REMINDER,
                priority=NotificationPriority.IMPORTANT,
                related_entity_type="borrowing",
                related_entity_id=str(borrowing.id),
            )
            count += 1
        
        return count
    
    async def send_overdue_notifications(self) -> int:
        """
        Send notifications for overdue books.
        
        Returns:
            int: Number of notifications sent
        """
        overdue_borrowings = await self.borrowing_repo.get_overdue()
        count = 0
        
        for borrowing in overdue_borrowings:
            days_overdue = borrowing.days_overdue
            late_fee = borrowing.calculate_late_fee()
            
            await self.send_notification(
                user_id=borrowing.user_id,
                message=f"Your book is {days_overdue} days overdue! Current late fee: €{late_fee:.2f}. Please return immediately.",
                title="Book Overdue - Action Required",
                notification_type=NotificationType.OVERDUE_REMINDER,
                priority=NotificationPriority.URGENT,
                related_entity_type="borrowing",
                related_entity_id=str(borrowing.id),
            )
            count += 1
        
        return count
    
    async def _send_email(self, user: User, subject: str, body: str) -> bool:
        """
        Internal method to send email.
        
        In production, this would use an email service (SMTP, SendGrid, SES).
        For now, just log the email.
        
        Args:
            user: Recipient user
            subject: Email subject
            body: Email body
            
        Returns:
            bool: True if sent
        """
        # TODO: Integrate with actual email service
        print(f"[EMAIL] To: {user.email}, Subject: {subject}")
        print(f"[EMAIL] Body: {body}")
        return True
    
    async def _send_sms(self, user: User, message: str) -> bool:
        """
        Internal method to send SMS.
        
        In production, this would use an SMS service (Twilio, AWS SNS).
        For now, just log the SMS.
        
        Args:
            user: Recipient user
            message: SMS message
            
        Returns:
            bool: True if sent
        """
        if not user.phone:
            return False
        
        # TODO: Integrate with actual SMS service
        print(f"[SMS] To: {user.phone}, Message: {message}")
        return True
