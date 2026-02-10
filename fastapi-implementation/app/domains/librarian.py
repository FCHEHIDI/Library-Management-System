"""
Librarian domain class - ADMINISTRATION OPERATIONS (33 methods).
REAL implementations with database interactions.
All administrative and moderation capabilities.
"""

from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select, func, and_, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User, Book, BorrowingRecord, Comment, Notification
from app.enums import (
    UserStatus,
    BookStatus,
    BookCategory,
    BorrowingStatus,
    CommentStatus,
    NotificationType,
    NotificationPriority,
    PhysicalState,
    LibrarianRole,
)
from app.policies import (
    BORROWING_POLICIES,
    FEE_POLICIES,
    FLAG_POLICIES,
)


class Librarian:
    """
    Librarian domain operations (Administrator perspective).
    
    Implements all administrative operations:
    - User management (suspend, ban, unsuspend)
    - Book management (add, update, remove)
    - Borrowing oversight (manual actions)
    - Comment moderation
    - System notifications
    - Statistics and reporting
    """
    
    def __init__(self, db: AsyncSession, librarian_id: UUID):
        """
        Initialize Librarian domain.
        
        Args:
            db: Database session
            librarian_id: ID of the librarian performing actions
        """
        self.db = db
        self.librarian_id = librarian_id
    
    # ========== USER MANAGEMENT (7 methods) ==========
    
    async def suspend_user(
        self,
        user_id: UUID,
        days: int,
        reason: str,
    ) -> User:
        """
        Suspend user account - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user to suspend
            days: Duration of suspension
            reason: Reason for suspension
            
        Returns:
            User: Updated user
            
        Raises:
            ValueError: If validation fails
        """
        user = await self.db.get(User, user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if user.status == UserStatus.BANNED:
            raise ValueError("Cannot suspend banned users")
        
        # Suspend user
        user.status = UserStatus.SUSPENDED
        user.suspension_start = datetime.utcnow()
        user.suspension_end = datetime.utcnow() + timedelta(days=days)
        user.suspension_reason = reason
        user.updated_at = datetime.utcnow()
        
        # Send notification
        notification = Notification(
            user_id=user_id,
            message=f"Your account has been suspended for {days} days. Reason: {reason}",
            title="Account Suspended",
            type=NotificationType.GENERAL,
            priority=NotificationPriority.URGENT,
        )
        self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def ban_user(
        self,
        user_id: UUID,
        reason: str,
    ) -> User:
        """
        Permanently ban user - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user to ban
            reason: Reason for ban
            
        Returns:
            User: Updated user
        """
        user = await self.db.get(User, user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.status = UserStatus.BANNED
        user.suspension_reason = f"PERMANENT BAN: {reason}"
        user.updated_at = datetime.utcnow()
        
        # Send notification
        notification = Notification(
            user_id=user_id,
            message=f"Your account has been permanently banned. Reason: {reason}",
            title="Account Banned",
            type=NotificationType.GENERAL,
            priority=NotificationPriority.URGENT,
        )
        self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def unsuspend_user(
        self,
        user_id: UUID,
    ) -> User:
        """
        Lift user suspension - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user
            
        Returns:
            User: Updated user
        """
        user = await self.db.get(User, user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if user.status != UserStatus.SUSPENDED:
            raise ValueError("User is not suspended")
        
        user.status = UserStatus.ACTIVE
        user.suspension_start = None
        user.suspension_end = None
        user.suspension_reason = None
        user.updated_at = datetime.utcnow()
        
        # Send notification
        notification = Notification(
            user_id=user_id,
            message="Your account suspension has been lifted. Welcome back!",
            title="Account Reactivated",
            type=NotificationType.GENERAL,
            priority=NotificationPriority.IMPORTANT,
        )
        self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def verify_user_email(
        self,
        user_id: UUID,
    ) -> User:
        """
        Manually verify user email - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user
            
        Returns:
            User: Updated user
        """
        user = await self.db.get(User, user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.email_verified = True
        user.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_all_users(
        self,
        status: UserStatus | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        """
        Get all users with optional filter - REAL IMPLEMENTATION.
        
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
        """
        Get all suspended users - REAL IMPLEMENTATION.
        
        Returns:
            list[User]: Suspended users
        """
        result = await self.db.execute(
            select(User)
            .where(User.status == UserStatus.SUSPENDED)
            .order_by(User.suspension_end.asc())
        )
        
        return list(result.scalars().all())
    
    async def get_user_details(
        self,
        user_id: UUID,
    ) -> dict:
        """
        Get detailed user information - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user
            
        Returns:
            dict: User details with statistics
        """
        user = await self.db.get(User, user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get active borrowings
        active_result = await self.db.execute(
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
        )
        active_borrowings = list(active_result.scalars().all())
        
        # Get overdue count
        overdue_result = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(
                and_(
                    BorrowingRecord.user_id == user_id,
                    BorrowingRecord.status == BorrowingStatus.OVERDUE,
                )
            )
        )
        current_overdue = overdue_result.scalar()
        
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "status": user.status.value,
            "email_verified": user.email_verified,
            "total_borrowings": user.total_borrowings,
            "active_borrowings": user.active_borrowings_count,
            "current_overdue": current_overdue,
            "total_overdue_count": user.overdue_count,
            "total_fees_paid": user.total_fees_paid,
            "suspension_end": user.suspension_end.isoformat() if user.suspension_end else None,
            "suspension_reason": user.suspension_reason,
            "member_since": user.created_at.isoformat(),
            "active_borrowings_details": [
                {
                    "book_title": b.book.title,
                    "due_date": b.due_date.isoformat(),
                    "is_overdue": b.is_overdue,
                    "days_overdue": b.days_overdue,
                }
                for b in active_borrowings
            ],
        }
    
    # ========== BOOK MANAGEMENT (8 methods) ==========
    
    async def add_book(
        self,
        isbn: str,
        title: str,
        author: str,
        category: BookCategory,
        publisher: str | None = None,
        year_published: int | None = None,
        location: str | None = None,
        **kwargs,
    ) -> Book:
        """
        Add new book to catalog - REAL IMPLEMENTATION.
        
        Args:
            isbn: ISBN number
            title: Book title
            author: Author name
            category: Book category
            publisher: Publisher name
            year_published: Publication year
            location: Physical location
            **kwargs: Additional fields
            
        Returns:
            Book: Created book
            
        Raises:
            ValueError: If ISBN already exists
        """
        # Check ISBN uniqueness
        existing = await self.db.execute(
            select(Book).where(Book.isbn == isbn)
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Book with ISBN {isbn} already exists")
        
        # Create book
        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            category=category,
            publisher=publisher,
            year_published=year_published,
            location=location,
            status=BookStatus.AVAILABLE,
            is_available=True,
            physical_state=PhysicalState.EXCELLENT,
            **kwargs,
        )
        
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def update_book(
        self,
        book_id: UUID,
        **updates,
    ) -> Book:
        """
        Update book details - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            **updates: Fields to update
            
        Returns:
            Book: Updated book
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # Update fields
        allowed_fields = {
            'title', 'author', 'category', 'publisher', 'year_published',
            'location', 'physical_state', 'description', 'language',
            'page_count', 'base_price', 'purchase_date',
        }
        
        for key, value in updates.items():
            if key in allowed_fields and value is not None:
                setattr(book, key, value)
        
        book.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def remove_book(
        self,
        book_id: UUID,
    ) -> None:
        """
        Remove book from catalog - REAL IMPLEMENTATION.
        
        Only allowed if book is not currently borrowed.
        
        Args:
            book_id: ID of the book
            
        Raises:
            ValueError: If book is borrowed
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        if not book.is_available:
            raise ValueError("Cannot remove borrowed book")
        
        await self.db.delete(book)
        await self.db.commit()
    
    async def mark_book_as_lost(
        self,
        book_id: UUID,
    ) -> Book:
        """
        Mark book as lost - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            
        Returns:
            Book: Updated book
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        book.status = BookStatus.LOST
        book.is_available = False
        book.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def mark_book_as_damaged(
        self,
        book_id: UUID,
        damage_description: str | None = None,
    ) -> Book:
        """
        Mark book as damaged - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            damage_description: Description of damage
            
        Returns:
            Book: Updated book
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        book.status = BookStatus.DAMAGED
        book.is_available = False
        book.physical_state = PhysicalState.DAMAGED
        book.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def repair_book(
        self,
        book_id: UUID,
    ) -> Book:
        """
        Mark damaged book as repaired - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            
        Returns:
            Book: Updated book
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        book.status = BookStatus.AVAILABLE
        book.is_available = True
        book.physical_state = PhysicalState.GOOD
        book.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def update_book_location(
        self,
        book_id: UUID,
        location: str,
    ) -> Book:
        """
        Update book physical location - REAL IMPLEMENTATION.
        
        Args:
            book_id: ID of the book
            location: New location
            
        Returns:
            Book: Updated book
        """
        book = await self.db.get(Book, book_id)
        
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        book.location = location
        book.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    async def get_all_books(
        self,
        status: BookStatus | None = None,
        category: BookCategory | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[Book], int]:
        """
        Get all books with filters - REAL IMPLEMENTATION.
        
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
    
    # ========== BORROWING MANAGEMENT (6 methods) ==========
    
    async def force_return(
        self,
        borrowing_id: UUID,
        damage_fee: float = 0.0,
        notes: str | None = None,
    ) -> BorrowingRecord:
        """
        Force return of a book - REAL IMPLEMENTATION.
        
        Used when librarian manually processes return.
        
        Args:
            borrowing_id: ID of the borrowing
            damage_fee: Damage fee if applicable
            notes: Admin notes
            
        Returns:
            BorrowingRecord: Updated borrowing
        """
        borrowing = await self.db.get(BorrowingRecord, borrowing_id)
        
        if not borrowing:
            raise ValueError(f"Borrowing {borrowing_id} not found")
        
        if borrowing.status == BorrowingStatus.RETURNED:
            raise ValueError("Book already returned")
        
        # Calculate fees
        late_fee = borrowing.calculate_late_fee()
        
        # Update borrowing
        borrowing.return_date = datetime.utcnow()
        borrowing.status = BorrowingStatus.RETURNED
        borrowing.late_fee = late_fee
        borrowing.damage_fee = damage_fee
        borrowing.total_fee = late_fee + damage_fee
        
        # Update book
        book = await self.db.get(Book, borrowing.book_id)
        if book:
            book.is_available = True
            book.status = BookStatus.AVAILABLE
            book.current_borrowing_count -= 1
        
        # Update user
        user = await self.db.get(User, borrowing.user_id)
        if user:
            user.active_borrowings_count -= 1
            if borrowing.is_overdue:
                user.overdue_count += 1
        
        # Send notification
        notification = Notification(
            user_id=borrowing.user_id,
            message=f"Book return processed by librarian. Total fees: €{borrowing.total_fee:.2f}",
            title="Return Processed",
            type=NotificationType.GENERAL,
            priority=NotificationPriority.IMPORTANT,
        )
        self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(borrowing)
        
        return borrowing
    
    async def waive_fees(
        self,
        borrowing_id: UUID,
    ) -> BorrowingRecord:
        """
        Waive fees for a borrowing - REAL IMPLEMENTATION.
        
        Args:
            borrowing_id: ID of the borrowing
            
        Returns:
            BorrowingRecord: Updated borrowing
        """
        borrowing = await self.db.get(BorrowingRecord, borrowing_id)
        
        if not borrowing:
            raise ValueError(f"Borrowing {borrowing_id} not found")
        
        borrowing.late_fee = 0.0
        borrowing.damage_fee = 0.0
        borrowing.total_fee = 0.0
        
        # Send notification
        notification = Notification(
            user_id=borrowing.user_id,
            message="Your fees have been waived by a librarian.",
            title="Fees Waived",
            type=NotificationType.GENERAL,
            priority=NotificationPriority.NORMAL,
        )
        self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(borrowing)
        
        return borrowing
    
    async def get_overdue_borrowings(self) -> list[BorrowingRecord]:
        """
        Get all overdue borrowings - REAL IMPLEMENTATION.
        
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
    
    async def get_all_active_borrowings(self) -> list[BorrowingRecord]:
        """
        Get all active borrowings - REAL IMPLEMENTATION.
        
        Returns:
            list[BorrowingRecord]: Active borrowings
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
    
    async def detect_overdue_borrowings(self) -> int:
        """
        Detect and mark overdue borrowings - REAL IMPLEMENTATION.
        
        Background task that runs daily.
        
        Returns:
            int: Number of borrowings marked as overdue
        """
        now = datetime.utcnow()
        
        # Find borrowings that are now overdue
        result = await self.db.execute(
            select(BorrowingRecord)
            .options(selectinload(BorrowingRecord.user))
            .where(
                and_(
                    BorrowingRecord.status.in_([BorrowingStatus.ACTIVE, BorrowingStatus.EXTENDED]),
                    BorrowingRecord.due_date < now,
                )
            )
        )
        
        overdue_borrowings = list(result.scalars().all())
        count = 0
        
        for borrowing in overdue_borrowings:
            borrowing.status = BorrowingStatus.OVERDUE
            
            # Send notification
            notification = Notification(
                user_id=borrowing.user_id,
                message=f"Your borrowed book is overdue! Late fees are accruing at €{FEE_POLICIES.LATE_FEE_PER_DAY}/day.",
                title="Book Overdue",
                type=NotificationType.OVERDUE_REMINDER,
                priority=NotificationPriority.URGENT,
                related_entity_type="borrowing",
                related_entity_id=str(borrowing.id),
            )
            self.db.add(notification)
            
            count += 1
        
        if count > 0:
            await self.db.commit()
        
        return count
    
    async def send_due_soon_reminders(self, days: int = 3) -> int:
        """
        Send reminders for books due soon - REAL IMPLEMENTATION.
        
        Args:
            days: Days threshold
            
        Returns:
            int: Number of reminders sent
        """
        threshold = datetime.utcnow() + timedelta(days=days)
        
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
            
            notification = Notification(
                user_id=borrowing.user_id,
                message=f"Your book '{borrowing.book.title}' is due in {days_left} days!",
                title="Book Due Soon",
                type=NotificationType.DUE_SOON_REMINDER,
                priority=NotificationPriority.IMPORTANT,
                related_entity_type="borrowing",
                related_entity_id=str(borrowing.id),
            )
            self.db.add(notification)
            
            count += 1
        
        if count > 0:
            await self.db.commit()
        
        return count
    
    # ========== COMMENT MODERATION (5 methods) ==========
    
    async def moderate_comment(
        self,
        comment_id: UUID,
        status: CommentStatus,
        reason: str | None = None,
    ) -> Comment:
        """
        Moderate a comment - REAL IMPLEMENTATION.
        
        Args:
            comment_id: ID of the comment
            status: New status (APPROVED or REJECTED)
            reason: Moderation reason
            
        Returns:
            Comment: Updated comment
        """
        comment = await self.db.get(Comment, comment_id)
        
        if not comment:
            raise ValueError(f"Comment {comment_id} not found")
        
        comment.status = status
        comment.moderated_at = datetime.utcnow()
        comment.moderated_by = self.librarian_id
        
        # Update book rating if approved
        if status == CommentStatus.APPROVED and comment.status != CommentStatus.APPROVED:
            book = await self.db.get(Book, comment.book_id)
            if book:
                book.total_ratings += 1
                total = (book.average_rating * (book.total_ratings - 1)) + comment.rating
                book.average_rating = total / book.total_ratings
        
        # Send notification
        if status == CommentStatus.REJECTED:
            notification = Notification(
                user_id=comment.user_id,
                message=f"Your comment was rejected. Reason: {reason or 'Violates community guidelines'}",
                title="Comment Rejected",
                type=NotificationType.GENERAL,
                priority=NotificationPriority.NORMAL,
            )
            self.db.add(notification)
        
        await self.db.commit()
        await self.db.refresh(comment)
        
        return comment
    
    async def delete_comment(
        self,
        comment_id: UUID,
    ) -> None:
        """
        Delete a comment (admin) - REAL IMPLEMENTATION.
        
        Args:
            comment_id: ID of the comment
        """
        comment = await self.db.get(Comment, comment_id)
        
        if not comment:
            raise ValueError(f"Comment {comment_id} not found")
        
        await self.db.delete(comment)
        await self.db.commit()
    
    async def get_pending_comments(self) -> list[Comment]:
        """
        Get pending comments for moderation - REAL IMPLEMENTATION.
        
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
    
    async def get_flagged_comments(self) -> list[Comment]:
        """
        Get flagged comments - REAL IMPLEMENTATION.
        
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
    
    async def get_auto_hidden_comments(self) -> list[Comment]:
        """
        Get auto-hidden comments (exceeded flag threshold) - REAL IMPLEMENTATION.
        
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
    
    # ========== NOTIFICATIONS (3 methods) ==========
    
    async def send_notification_to_user(
        self,
        user_id: UUID,
        message: str,
        title: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> Notification:
        """
        Send notification to a user - REAL IMPLEMENTATION.
        
        Args:
            user_id: ID of the user
            message: Notification message
            title: Notification title
            priority: Priority level
            
        Returns:
            Notification: Created notification
        """
        notification = Notification(
            user_id=user_id,
            message=message,
            title=title,
            type=NotificationType.GENERAL,
            priority=priority,
        )
        
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        
        return notification
    
    async def send_broadcast_notification(
        self,
        message: str,
        title: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> int:
        """
        Send notification to all active users - REAL IMPLEMENTATION.
        
        Args:
            message: Notification message
            title: Notification title
            priority: Priority level
            
        Returns:
            int: Number of notifications sent
        """
        # Get all active users
        result = await self.db.execute(
            select(User).where(User.status == UserStatus.ACTIVE)
        )
        
        users = list(result.scalars().all())
        count = 0
        
        for user in users:
            notification = Notification(
                user_id=user.id,
                message=message,
                title=title,
                type=NotificationType.GENERAL,
                priority=priority,
            )
            self.db.add(notification)
            count += 1
        
        if count > 0:
            await self.db.commit()
        
        return count
    
    async def clear_old_notifications(self, days: int = 30) -> int:
        """
        Clear read notifications older than X days - REAL IMPLEMENTATION.
        
        Args:
            days: Age threshold
            
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
        
        if count > 0:
            await self.db.commit()
        
        return count
    
    # ========== STATISTICS & REPORTING (4 methods) ==========
    
    async def get_admin_dashboard_stats(self) -> dict:
        """
        Get comprehensive admin dashboard statistics - REAL IMPLEMENTATION.
        
        Returns:
            dict: Dashboard statistics
        """
        # Total books
        total_books = await self.db.execute(select(func.count(Book.id)))
        
        # Available books
        available_books = await self.db.execute(
            select(func.count(Book.id)).where(Book.is_available == True)
        )
        
        # Total users
        total_users = await self.db.execute(select(func.count(User.id)))
        
        # Active users
        active_users = await self.db.execute(
            select(func.count(User.id)).where(User.status == UserStatus.ACTIVE)
        )
        
        # Active borrowings
        active_borrowings = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(
                BorrowingRecord.status.in_([
                    BorrowingStatus.ACTIVE,
                    BorrowingStatus.EXTENDED,
                    BorrowingStatus.OVERDUE,
                ])
            )
        )
        
        # Overdue borrowings
        overdue_borrowings = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(BorrowingRecord.status == BorrowingStatus.OVERDUE)
        )
        
        # Pending comments
        pending_comments = await self.db.execute(
            select(func.count(Comment.id))
            .where(Comment.status == CommentStatus.PENDING)
        )
        
        # Flagged comments
        flagged_comments = await self.db.execute(
            select(func.count(Comment.id))
            .where(Comment.flag_count > 0)
        )
        
        return {
            "total_books": total_books.scalar(),
            "available_books": available_books.scalar(),
            "borrowed_books": total_books.scalar() - available_books.scalar(),
            "total_users": total_users.scalar(),
            "active_users": active_users.scalar(),
            "active_borrowings": active_borrowings.scalar(),
            "overdue_borrowings": overdue_borrowings.scalar(),
            "pending_comments": pending_comments.scalar(),
            "flagged_comments": flagged_comments.scalar(),
        }
    
    async def get_top_borrowers(self, limit: int = 10) -> list[dict]:
        """
        Get top borrowers - REAL IMPLEMENTATION.
        
        Args:
            limit: Maximum results
            
        Returns:
            list[dict]: Top borrowers with stats
        """
        result = await self.db.execute(
            select(User)
            .order_by(User.total_borrowings.desc())
            .limit(limit)
        )
        
        users = result.scalars().all()
        
        top_borrowers = []
        for user in users:
            top_borrowers.append({
                "id": str(user.id),
                "username": user.username,
                "full_name": user.full_name,
                "total_borrowings": user.total_borrowings,
                "active_borrowings": user.active_borrowings_count,
                "overdue_count": user.overdue_count,
            })
        
        return top_borrowers
    
    async def get_borrowing_trends(self, days: int = 30) -> dict:
        """
        Get borrowing trends - REAL IMPLEMENTATION.
        
        Args:
            days: Time window
            
        Returns:
            dict: Borrowing trends
        """
        since = datetime.utcnow() - timedelta(days=days)
        
        # Total borrowings in period
        total_result = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(BorrowingRecord.created_at >= since)
        )
        
        # Returns in period
        returns_result = await self.db.execute(
            select(func.count(BorrowingRecord.id))
            .where(
                and_(
                    BorrowingRecord.return_date >= since,
                    BorrowingRecord.return_date != None,
                )
            )
        )
        
        return {
            "period_days": days,
            "total_borrowings": total_result.scalar(),
            "total_returns": returns_result.scalar(),
            "average_per_day": round(total_result.scalar() / days, 2),
        }
    
    async def get_category_performance(self) -> list[dict]:
        """
        Get performance metrics by category - REAL IMPLEMENTATION.
        
        Returns:
            list[dict]: Category performance
        """
        result = await self.db.execute(
            select(
                Book.category,
                func.count(Book.id).label('total_books'),
                func.avg(Book.total_borrowings).label('avg_borrowings'),
                func.avg(Book.average_rating).label('avg_rating'),
            )
            .group_by(Book.category)
        )
        
        performance = []
        for row in result.all():
            category, total, avg_borr, avg_rat = row
            performance.append({
                "category": category.value,
                "total_books": total,
                "average_borrowings": round(avg_borr or 0, 2),
                "average_rating": round(avg_rat or 0, 2),
            })
        
        return performance
