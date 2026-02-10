"""
Domain interfaces - Domain operation contracts.

Using Protocol for structural subtyping (duck typing).
This allows existing domain classes to be considered implementations
without explicit inheritance (more Pythonic).

Note: Protocol requires Python 3.8+
"""

from typing import Protocol
from uuid import UUID
from datetime import datetime

from app.models import User, Book, BorrowingRecord, Comment, Notification


class IBorrower(Protocol):
    """
    Borrower domain interface.
    
    Contract for user-facing library operations.
    Any class implementing these methods is considered a valid IBorrower.
    """
    
    # Borrowing operations
    async def borrow_book(self, user_id: UUID, book_id: UUID) -> BorrowingRecord:
        """Borrow a book."""
        ...
    
    async def return_book(self, borrowing_id: UUID, damage_fee: float = 0.0) -> BorrowingRecord:
        """Return a borrowed book."""
        ...
    
    async def extend_borrowing_period(self, borrowing_id: UUID, days: int = 7) -> BorrowingRecord:
        """Extend borrowing period."""
        ...
    
    async def get_borrowing_history(self, user_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """Get borrowing history."""
        ...
    
    async def get_active_borrowings(self, user_id: UUID) -> list[BorrowingRecord]:
        """Get active borrowings."""
        ...
    
    async def get_due_soon_books(self, user_id: UUID, days: int = 3) -> list[BorrowingRecord]:
        """Get books due soon."""
        ...
    
    async def can_borrow_book(self, user_id: UUID, book_id: UUID) -> tuple[bool, str]:
        """Check if user can borrow a book."""
        ...
    
    async def get_borrowing_by_id(self, borrowing_id: UUID) -> BorrowingRecord | None:
        """Get borrowing by ID."""
        ...
    
    # Search & discovery
    async def search_books_by_title(self, query: str, limit: int = 20) -> list[Book]:
        """Search books by title."""
        ...
    
    async def search_books_by_author(self, author: str, limit: int = 20) -> list[Book]:
        """Search books by author."""
        ...
    
    async def search_books_by_category(
        self,
        category: str,
        available_only: bool = False,
        limit: int = 20,
    ) -> list[Book]:
        """Search books by category."""
        ...
    
    async def get_available_books(self, limit: int = 50) -> list[Book]:
        """Get available books."""
        ...
    
    async def get_book_details(self, book_id: UUID) -> Book | None:
        """Get book details."""
        ...
    
    async def get_popular_books(self, limit: int = 10) -> list[Book]:
        """Get popular books."""
        ...
    
    # Comments & ratings
    async def add_comment(
        self,
        user_id: UUID,
        book_id: UUID,
        rating: int,
        content: str,
    ) -> Comment:
        """Add comment/review."""
        ...
    
    async def edit_comment(
        self,
        comment_id: UUID,
        user_id: UUID,
        rating: int | None = None,
        content: str | None = None,
    ) -> Comment:
        """Edit own comment."""
        ...
    
    async def delete_comment(self, comment_id: UUID, user_id: UUID) -> None:
        """Delete own comment."""
        ...
    
    async def get_book_comments(self, book_id: UUID, limit: int = 20) -> list[Comment]:
        """Get comments for a book."""
        ...
    
    async def flag_comment(self, comment_id: UUID, reason: str) -> Comment:
        """Flag inappropriate comment."""
        ...
    
    # Notifications
    async def get_unread_notifications(self, user_id: UUID, limit: int = 50) -> list[Notification]:
        """Get unread notifications."""
        ...
    
    async def mark_notification_as_read(self, notification_id: UUID, user_id: UUID) -> Notification:
        """Mark notification as read."""
        ...
    
    async def get_notification_history(self, user_id: UUID, limit: int = 100) -> list[Notification]:
        """Get notification history."""
        ...
    
    async def clear_notifications(self, user_id: UUID) -> int:
        """Clear read notifications."""
        ...
    
    # Profile management
    async def get_user_profile(self, user_id: UUID) -> User | None:
        """Get user profile."""
        ...
    
    async def update_profile(self, user_id: UUID, **updates) -> User:
        """Update user profile."""
        ...
    
    async def get_statistics(self, user_id: UUID) -> dict:
        """Get user statistics."""
        ...


class ILibrary(Protocol):
    """
    Library domain interface.
    
    Contract for catalog management operations.
    """
    
    # Catalog searches
    async def search_books(
        self,
        query: str | None = None,
        category: str | None = None,
        available_only: bool = False,
        min_rating: float = 0.0,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """Advanced book search."""
        ...
    
    async def get_book_by_isbn(self, isbn: str) -> Book | None:
        """Find book by ISBN."""
        ...
    
    async def get_books_by_category(self, category: str, limit: int = 50) -> list[Book]:
        """Get books by category."""
        ...
    
    async def get_new_arrivals(self, limit: int = 20) -> list[Book]:
        """Get recently added books."""
        ...
    
    async def get_trending_books(self, days: int = 30, limit: int = 10) -> list[Book]:
        """Get trending books."""
        ...
    
    # Availability checks
    async def check_availability(self, book_id: UUID) -> dict:
        """Check book availability."""
        ...
    
    async def get_available_copies(self, isbn: str) -> int:
        """Count available copies by ISBN."""
        ...
    
    # Statistics
    async def get_library_statistics(self) -> dict:
        """Get library-wide statistics."""
        ...
    
    async def get_category_statistics(self) -> list[dict]:
        """Get statistics per category."""
        ...
    
    async def get_popular_books(self, limit: int = 10) -> list[dict]:
        """Get most borrowed books."""
        ...
    
    # Catalog validation
    async def validate_isbn_unique(self, isbn: str, exclude_id: UUID | None = None) -> bool:
        """Validate ISBN uniqueness."""
        ...
    
    async def get_book_borrowing_history(self, book_id: UUID, limit: int = 50) -> list[BorrowingRecord]:
        """Get borrowing history for a book."""
        ...


class ILibrarian(Protocol):
    """
    Librarian domain interface.
    
    Contract for administrative operations.
    """
    
    # User management
    async def suspend_user(self, user_id: UUID, days: int, reason: str) -> User:
        """Suspend user account."""
        ...
    
    async def ban_user(self, user_id: UUID, reason: str) -> User:
        """Permanently ban user."""
        ...
    
    async def unsuspend_user(self, user_id: UUID) -> User:
        """Lift user suspension."""
        ...
    
    async def verify_user_email(self, user_id: UUID) -> User:
        """Manually verify user email."""
        ...
    
    async def get_all_users(
        self,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        """Get all users with optional filter."""
        ...
    
    async def get_suspended_users(self) -> list[User]:
        """Get all suspended users."""
        ...
    
    async def get_user_details(self, user_id: UUID) -> dict:
        """Get detailed user information."""
        ...
    
    # Book management
    async def add_book(
        self,
        isbn: str,
        title: str,
        author: str,
        category: str,
        **kwargs,
    ) -> Book:
        """Add new book to catalog."""
        ...
    
    async def update_book(self, book_id: UUID, **updates) -> Book:
        """Update book details."""
        ...
    
    async def remove_book(self, book_id: UUID) -> None:
        """Remove book from catalog."""
        ...
    
    async def mark_book_as_lost(self, book_id: UUID) -> Book:
        """Mark book as lost."""
        ...
    
    async def mark_book_as_damaged(self, book_id: UUID, damage_description: str | None = None) -> Book:
        """Mark book as damaged."""
        ...
    
    async def repair_book(self, book_id: UUID) -> Book:
        """Mark damaged book as repaired."""
        ...
    
    async def update_book_location(self, book_id: UUID, location: str) -> Book:
        """Update book physical location."""
        ...
    
    async def get_all_books(
        self,
        status: str | None = None,
        category: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """Get all books with filters."""
        ...
    
    # Borrowing management
    async def force_return(
        self,
        borrowing_id: UUID,
        damage_fee: float = 0.0,
        notes: str | None = None,
    ) -> BorrowingRecord:
        """Force return of a book."""
        ...
    
    async def waive_fees(self, borrowing_id: UUID) -> BorrowingRecord:
        """Waive fees for a borrowing."""
        ...
    
    async def get_overdue_borrowings(self) -> list[BorrowingRecord]:
        """Get all overdue borrowings."""
        ...
    
    async def get_all_active_borrowings(self) -> list[BorrowingRecord]:
        """Get all active borrowings."""
        ...
    
    async def detect_overdue_borrowings(self) -> int:
        """Detect and mark overdue borrowings."""
        ...
    
    async def send_due_soon_reminders(self, days: int = 3) -> int:
        """Send reminders for books due soon."""
        ...
    
    # Comment moderation
    async def moderate_comment(self, comment_id: UUID, status: str, reason: str | None = None) -> Comment:
        """Moderate a comment."""
        ...
    
    async def delete_comment(self, comment_id: UUID) -> None:
        """Delete a comment (admin)."""
        ...
    
    async def get_pending_comments(self) -> list[Comment]:
        """Get pending comments for moderation."""
        ...
    
    async def get_flagged_comments(self) -> list[Comment]:
        """Get flagged comments."""
        ...
    
    async def get_auto_hidden_comments(self) -> list[Comment]:
        """Get auto-hidden comments."""
        ...
    
    # Notifications
    async def send_notification_to_user(
        self,
        user_id: UUID,
        message: str,
        title: str,
        priority: str = "NORMAL",
    ) -> Notification:
        """Send notification to a user."""
        ...
    
    async def send_broadcast_notification(
        self,
        message: str,
        title: str,
        priority: str = "NORMAL",
    ) -> int:
        """Send notification to all active users."""
        ...
    
    async def clear_old_notifications(self, days: int = 30) -> int:
        """Clear read notifications older than X days."""
        ...
    
    # Statistics & reporting
    async def get_admin_dashboard_stats(self) -> dict:
        """Get comprehensive admin dashboard statistics."""
        ...
    
    async def get_top_borrowers(self, limit: int = 10) -> list[dict]:
        """Get top borrowers."""
        ...
    
    async def get_borrowing_trends(self, days: int = 30) -> dict:
        """Get borrowing trends."""
        ...
    
    async def get_category_performance(self) -> list[dict]:
        """Get performance metrics by category."""
        ...
