"""
Service interfaces - Business service contracts.

Using ABC (Abstract Base Classes) for service layer abstraction.
Services encapsulate complex business logic across multiple entities.
"""

from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

from app.enums import NotificationType, NotificationPriority


class INotificationService(ABC):
    """
    Notification service interface.
    
    Contract for multi-channel notification delivery.
    Handles in-app, email, SMS routing based on priority.
    """
    
    @abstractmethod
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
        
        Routing logic:
        - NORMAL: In-app only
        - IMPORTANT: In-app + Email
        - URGENT: In-app + Email + SMS
        """
        pass
    
    @abstractmethod
    async def send_email_notification(
        self,
        user_id: UUID,
        subject: str,
        body: str,
    ) -> bool:
        """Send email notification."""
        pass
    
    @abstractmethod
    async def send_sms_notification(
        self,
        user_id: UUID,
        message: str,
    ) -> bool:
        """Send SMS notification."""
        pass
    
    @abstractmethod
    async def send_broadcast(
        self,
        message: str,
        title: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> int:
        """Send notification to all active users."""
        pass
    
    @abstractmethod
    async def send_due_soon_reminders(self, days: int = 3) -> int:
        """Send reminders for books due soon."""
        pass
    
    @abstractmethod
    async def send_overdue_notifications(self) -> int:
        """Send notifications for overdue books."""
        pass


class IFeeCalculator(ABC):
    """
    Fee calculator service interface.
    
    Contract for all fee calculation operations.
    Centralizes fee logic for consistency.
    """
    
    @abstractmethod
    def calculate_late_fee(
        self,
        borrow_date: datetime,
        due_date: datetime,
        return_date: datetime | None = None,
    ) -> float:
        """
        Calculate late fee for a borrowing.
        
        Formula:
        - Grace period: No fees
        - After grace: (days - grace) × daily_rate
        - Maximum: cap amount
        """
        pass
    
    @abstractmethod
    def calculate_damage_fee(
        self,
        base_price: float,
        damage_level: str,
    ) -> float:
        """
        Calculate damage fee based on book price and damage level.
        
        Damage levels:
        - MINOR: 10% of base price
        - MODERATE: 50% of base price
        - SEVERE: 100% of base price
        """
        pass
    
    @abstractmethod
    def calculate_replacement_cost(
        self,
        base_price: float,
    ) -> float:
        """Calculate replacement cost for lost book."""
        pass
    
    @abstractmethod
    def can_waive_fee(
        self,
        fee_amount: float,
        reason: str,
    ) -> bool:
        """Check if fee can be waived (business rules)."""
        pass


class ISearchService(ABC):
    """
    Search service interface.
    
    Contract for advanced search operations.
    Can be implemented with Elasticsearch, PostgreSQL FTS, etc.
    """
    
    @abstractmethod
    async def search_books(
        self,
        query: str,
        filters: dict[str, any] | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict], int]:
        """
        Full-text search for books.
        
        Args:
            query: Search query
            filters: Optional filters (category, rating, etc.)
            limit: Results limit
            offset: Pagination offset
            
        Returns:
            tuple[list[dict], int]: (results, total_count)
        """
        pass
    
    @abstractmethod
    async def search_by_author(
        self,
        author: str,
        limit: int = 20,
    ) -> list[dict]:
        """Search books by author."""
        pass
    
    @abstractmethod
    async def search_by_isbn(
        self,
        isbn: str,
    ) -> dict | None:
        """Search book by ISBN."""
        pass
    
    @abstractmethod
    async def get_recommendations(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[dict]:
        """
        Get book recommendations for user.
        
        Based on:
        - User's borrowing history
        - User's ratings
        - Popular books in same categories
        """
        pass
    
    @abstractmethod
    async def get_similar_books(
        self,
        book_id: UUID,
        limit: int = 5,
    ) -> list[dict]:
        """Get similar books (same author, category, etc.)."""
        pass


class IEmailService(ABC):
    """
    Email service interface.
    
    Contract for email operations.
    Can be implemented with SMTP, SendGrid, SES, etc.
    """
    
    @abstractmethod
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> bool:
        """Send email."""
        pass
    
    @abstractmethod
    async def send_verification_email(
        self,
        to: str,
        token: str,
    ) -> bool:
        """Send email verification."""
        pass
    
    @abstractmethod
    async def send_password_reset_email(
        self,
        to: str,
        token: str,
    ) -> bool:
        """Send password reset email."""
        pass
    
    @abstractmethod
    async def send_welcome_email(
        self,
        to: str,
        username: str,
    ) -> bool:
        """Send welcome email to new user."""
        pass
    
    @abstractmethod
    async def send_suspension_email(
        self,
        to: str,
        reason: str,
        until: datetime,
    ) -> bool:
        """Send account suspension notification."""
        pass
