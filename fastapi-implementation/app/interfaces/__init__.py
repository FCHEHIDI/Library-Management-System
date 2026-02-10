"""
Interfaces package - Contract definitions for SOLID architecture.

Python doesn't have native interfaces like TypeScript/Java, so we use:
- ABC (Abstract Base Classes) for strict enforcement
- Protocol for structural subtyping (duck typing)
"""

from app.interfaces.repositories import (
    IUserRepository,
    IBookRepository,
    IBorrowingRepository,
    ICommentRepository,
    INotificationRepository,
)
from app.interfaces.services import (
    INotificationService,
    IFeeCalculator,
    ISearchService,
    IEmailService,
)
from app.interfaces.domains import (
    IBorrower,
    ILibrary,
    ILibrarian,
)

__all__ = [
    # Repository interfaces
    "IUserRepository",
    "IBookRepository",
    "IBorrowingRepository",
    "ICommentRepository",
    "INotificationRepository",
    # Service interfaces
    "INotificationService",
    "IFeeCalculator",
    "ISearchService",
    "IEmailService",
    # Domain interfaces
    "IBorrower",
    "ILibrary",
    "ILibrarian",
]
