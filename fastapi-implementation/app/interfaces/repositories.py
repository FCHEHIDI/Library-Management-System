"""
Repository interfaces - Data access contracts.

Using ABC (Abstract Base Classes) for strict interface enforcement.
All repository implementations MUST inherit from these interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from app.models import User, Book, BorrowingRecord, Comment, Notification
from app.enums import UserStatus, BookStatus, BookCategory, BorrowingStatus, CommentStatus


class IUserRepository(ABC):
    """
    User repository interface.
    
    Contract for all user data access operations.
    Enforces separation of concerns (data access vs business logic).
    """
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """Get user by username."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def create(self, user_data: dict[str, Any]) -> User:
        """Create new user."""
        pass
    
    @abstractmethod
    async def update(self, user_id: UUID, updates: dict[str, Any]) -> User:
        """Update user."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete user."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        status: UserStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        """Get all users with optional filters."""
        pass
    
    @abstractmethod
    async def get_suspended_users(self) -> list[User]:
        """Get all suspended users."""
        pass
    
    @abstractmethod
    async def check_username_exists(self, username: str, exclude_id: UUID | None = None) -> bool:
        """Check if username exists."""
        pass
    
    @abstractmethod
    async def check_email_exists(self, email: str, exclude_id: UUID | None = None) -> bool:
        """Check if email exists."""
        pass


class IBookRepository(ABC):
    """
    Book repository interface.
    
    Contract for all book catalog data access operations.
    """
    
    @abstractmethod
    async def get_by_id(self, book_id: UUID) -> Book | None:
        """Get book by ID."""
        pass
    
    @abstractmethod
    async def get_by_isbn(self, isbn: str) -> Book | None:
        """Get book by ISBN."""
        pass
    
    @abstractmethod
    async def create(self, book_data: dict[str, Any]) -> Book:
        """Create new book."""
        pass
    
    @abstractmethod
    async def update(self, book_id: UUID, updates: dict[str, Any]) -> Book:
        """Update book."""
        pass
    
    @abstractmethod
    async def delete(self, book_id: UUID) -> None:
        """Delete book."""
        pass
    
    @abstractmethod
    async def search(
        self,
        query: str | None = None,
        category: BookCategory | None = None,
        available_only: bool = False,
        min_rating: float = 0.0,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """Advanced book search."""
        pass
    
    @abstractmethod
    async def get_all(
        self,
        status: BookStatus | None = None,
        category: BookCategory | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """Get all books with filters."""
        pass
    
    @abstractmethod
    async def get_available_books(self, limit: int = 50) -> list[Book]:
        """Get available books."""
        pass
    
    @abstractmethod
    async def get_by_category(self, category: BookCategory, limit: int = 50) -> list[Book]:
        """Get books by category."""
        pass
    
    @abstractmethod
    async def get_new_arrivals(self, limit: int = 20) -> list[Book]:
        """Get recently added books."""
        pass
    
    @abstractmethod
    async def get_trending(self, days: int = 30, limit: int = 10) -> list[Book]:
        """Get trending books."""
        pass
    
    @abstractmethod
    async def get_popular(self, limit: int = 10) -> list[Book]:
        """Get most borrowed books."""
        pass
    
    @abstractmethod
    async def check_isbn_exists(self, isbn: str, exclude_id: UUID | None = None) -> bool:
        """Check if ISBN exists."""
        pass


class IBorrowingRepository(ABC):
    """
    Borrowing repository interface.
    
    Contract for all borrowing transaction data access operations.
    """
    
    @abstractmethod
    async def get_by_id(self, borrowing_id: UUID) -> BorrowingRecord | None:
        """Get borrowing by ID."""
        pass
    
    @abstractmethod
    async def create(self, borrowing_data: dict[str, Any]) -> BorrowingRecord:
        """Create new borrowing."""
        pass
    
    @abstractmethod
    async def update(self, borrowing_id: UUID, updates: dict[str, Any]) -> BorrowingRecord:
        """Update borrowing."""
        pass
    
    @abstractmethod
    async def delete(self, borrowing_id: UUID) -> None:
        """Delete borrowing."""
        pass
    
    @abstractmethod
    async def get_user_history(self, user_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """Get user's borrowing history."""
        pass
    
    @abstractmethod
    async def get_active_borrowings(self, user_id: UUID) -> list[BorrowingRecord]:
        """Get user's active borrowings."""
        pass
    
    @abstractmethod
    async def get_due_soon(self, user_id: UUID, days: int = 3) -> list[BorrowingRecord]:
        """Get books due soon."""
        pass
    
    @abstractmethod
    async def get_all_active(self) -> list[BorrowingRecord]:
        """Get all active borrowings (admin)."""
        pass
    
    @abstractmethod
    async def get_overdue(self) -> list[BorrowingRecord]:
        """Get all overdue borrowings."""
        pass
    
    @abstractmethod
    async def get_book_history(self, book_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """Get borrowing history for a book."""
        pass
    
    @abstractmethod
    async def detect_overdue(self) -> list[BorrowingRecord]:
        """Detect and return borrowings that should be marked overdue."""
        pass


class ICommentRepository(ABC):
    """
    Comment repository interface.
    
    Contract for all comment/review data access operations.
    """
    
    @abstractmethod
    async def get_by_id(self, comment_id: UUID) -> Comment | None:
        """Get comment by ID."""
        pass
    
    @abstractmethod
    async def create(self, comment_data: dict[str, Any]) -> Comment:
        """Create new comment."""
        pass
    
    @abstractmethod
    async def update(self, comment_id: UUID, updates: dict[str, Any]) -> Comment:
        """Update comment."""
        pass
    
    @abstractmethod
    async def delete(self, comment_id: UUID) -> None:
        """Delete comment."""
        pass
    
    @abstractmethod
    async def get_book_comments(
        self,
        book_id: UUID,
        status: CommentStatus = CommentStatus.APPROVED,
        limit: int = 20,
    ) -> list[Comment]:
        """Get comments for a book."""
        pass
    
    @abstractmethod
    async def get_user_comments(self, user_id: UUID, limit: int = 50) -> list[Comment]:
        """Get user's comments."""
        pass
    
    @abstractmethod
    async def get_pending(self) -> list[Comment]:
        """Get pending comments for moderation."""
        pass
    
    @abstractmethod
    async def get_flagged(self) -> list[Comment]:
        """Get flagged comments."""
        pass
    
    @abstractmethod
    async def get_auto_hidden(self) -> list[Comment]:
        """Get auto-hidden comments."""
        pass
    
    @abstractmethod
    async def check_user_commented(self, user_id: UUID, book_id: UUID) -> bool:
        """Check if user already commented on book."""
        pass


class INotificationRepository(ABC):
    """
    Notification repository interface.
    
    Contract for all notification data access operations.
    """
    
    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> Notification | None:
        """Get notification by ID."""
        pass
    
    @abstractmethod
    async def create(self, notification_data: dict[str, Any]) -> Notification:
        """Create new notification."""
        pass
    
    @abstractmethod
    async def update(self, notification_id: UUID, updates: dict[str, Any]) -> Notification:
        """Update notification."""
        pass
    
    @abstractmethod
    async def delete(self, notification_id: UUID) -> None:
        """Delete notification."""
        pass
    
    @abstractmethod
    async def get_user_unread(self, user_id: UUID, limit: int = 50) -> list[Notification]:
        """Get user's unread notifications."""
        pass
    
    @abstractmethod
    async def get_user_history(self, user_id: UUID, limit: int = 100) -> list[Notification]:
        """Get user's notification history."""
        pass
    
    @abstractmethod
    async def mark_as_read(self, notification_id: UUID) -> Notification:
        """Mark notification as read."""
        pass
    
    @abstractmethod
    async def mark_multiple_as_read(self, notification_ids: list[UUID]) -> int:
        """Mark multiple notifications as read."""
        pass
    
    @abstractmethod
    async def clear_user_read(self, user_id: UUID) -> int:
        """Clear user's read notifications."""
        pass
    
    @abstractmethod
    async def clear_old(self, days: int = 30) -> int:
        """Clear old read notifications."""
        pass
