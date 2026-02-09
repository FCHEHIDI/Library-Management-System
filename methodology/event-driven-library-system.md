# 📖 Event-Driven Library System - Complete Methodology Guide

> *A comprehensive guide to building a library management system using event-driven architecture and SOLID principles*

---

## 📚 Table of Contents

### Part I: System Architecture
- [1. Core Components](#1-core-components)
  - [1.1 Interfaces](#11-interfaces)
  - [1.2 Enumerations](#12-enumerations)
  - [1.3 Data Models](#13-data-models)
  - [1.4 Domain Classes](#14-domain-classes)

### Part II: Business Logic
- [2. Business Rules & Policies](#2-business-rules--policies)
  - [2.1 Borrowing Policies](#21-borrowing-policies)
  - [2.2 Time Management](#22-time-management)
  - [2.3 Fee Structure](#23-fee-structure)
  - [2.4 Access Control](#24-access-control)
  - [2.5 Validation Rules](#25-validation-rules)

### Part III: Event Catalog
- [3. Domain Events](#3-domain-events)
  - [3.1 Book Management Events](#31-book-management-events)
  - [3.2 User Management Events](#32-user-management-events)
  - [3.3 Borrowing Events](#33-borrowing-events)
  - [3.4 Notification Events](#34-notification-events)
  - [3.5 Administrative Events](#35-administrative-events)

### Part IV: Implementation Guide
- [4. Development Methodology](#4-development-methodology)
  - [4.1 Event-Driven Design Principles](#41-event-driven-design-principles)
  - [4.2 SOLID Principles Application](#42-solid-principles-application)
  - [4.3 Testing Strategy](#43-testing-strategy)
  - [4.4 Code Organization](#44-code-organization)

### Appendices
- [Appendix A: Complete Event List](#appendix-a-complete-event-list)
- [Appendix B: UML Diagrams](#appendix-b-uml-diagrams)
- [Appendix C: API Reference](#appendix-c-api-reference)

---

## 1. Core Components

### 1.1 Interfaces

#### INotifiable Interface
**Purpose**: Enables notification and email communication capabilities for system entities.

**Methods**:
```typescript
interface INotifiable {
  sendNotification(recipientId: UUID, message: string, type: NotificationType): void;
  sendEmail(recipientEmail: string, subject: string, body: string): void;
  receiveNotification(): Notification[];
  markNotificationAsRead(notificationId: UUID): void;
}
```

**Implementation**: Used by `Borrower` and `Librarian` classes to handle communications.

---

#### IBorrowable Interface
**Purpose**: Defines contract for entities that can be borrowed.

**Methods**:
```typescript
interface IBorrowable {
  canBeBorrowed(): boolean;
  borrow(borrowerId: UUID): BorrowingRecord;
  return(borrowerId: UUID): void;
  extendBorrowingPeriod(days: number): boolean;
  getBorrowingHistory(): BorrowingRecord[];
}
```

**Implementation**: Applied to `Book` model for borrowing operations.

---

#### IUser Interface
**Purpose**: Core user identity and profile management.

**Methods**:
```typescript
interface IUser {
  getProfile(): UserProfile;
  updateProfile(profileData: Partial<UserProfile>): void;
  isActive(): boolean;
  getId(): UUID;
}
```

**Implementation**: Implemented by both `Borrower` and `Librarian` for unified user management.

---

#### ISearchable Interface
**Purpose**: Advanced search and filtering capabilities.

**Methods**:
```typescript
interface ISearchable {
  searchByTitle(title: string): Book[];
  searchByAuthor(author: string): Book[];
  searchByISBN(isbn: string): Book | null;
  searchAvailableBooks(): Book[];
  filterBooks(criteria: SearchCriteria): Book[];
}
```

**Implementation**: Used by `Borrower` class for book discovery.

---

### 1.2 Enumerations

#### BookCategory
**Purpose**: Classification system for library collection.

**Values**: `FICTION`, `NON_FICTION`, `SCIENCE`, `TECHNOLOGY`, `HISTORY`, `BIOGRAPHY`, `PHILOSOPHY`, `RELIGION`, `POETRY`, `DRAMA`, `CHILDREN`, `YOUNG_ADULT`, `REFERENCE`, `EDUCATION`, `ART`, `MUSIC`, `TRAVEL`, `COOKING`, `HEALTH`, `SELF_HELP`, `BUSINESS`, `ECONOMICS`, `LAW`, `POLITICS`, `OTHER`

**Usage**: Book categorization, specialized borrowing rules (e.g., REFERENCE books have shorter periods).

---

#### PhysicalState
**Purpose**: Track physical condition of library materials.

**Values**:
- `EXCELLENT` - Like new, no wear
- `GOOD` - Minor usage traces
- `FAIR` - Visible wear
- `POOR` - Needs repair
- `DAMAGED` - Not borrowable
- `LOST` - Missing from inventory
- `IN_REPAIR` - Under maintenance

**Usage**: Inventory management, borrowing eligibility.

---

#### BorrowingStatus
**Purpose**: Track borrowing lifecycle states.

**Values**:
- `ACTIVE` - Currently borrowed
- `RETURNED` - Book returned
- `OVERDUE` - Late return
- `EXTENDED` - Period prolonged
- `CANCELLED` - Cancelled before pickup
- `RESERVED` - Reserved but not borrowed

**Usage**: Borrowing workflow management, fee calculation.

---

#### NotificationType
**Purpose**: Categorize system notifications.

**Values**: `DUE_DATE`, `OVERDUE`, `RESERVATION_READY`, `EXTENSION_APPROVED`, `EXTENSION_DENIED`, `FINE_NOTICE`, `ACCOUNT_SUSPENDED`, `ACCOUNT_ACTIVATED`, `NEW_BOOK`, `CLAIM_UPDATE`, `GENERAL_INFO`

**Usage**: Notification routing, user preferences.

---

#### UserStatus
**Purpose**: User account states.

**Values**: `ACTIVE`, `SUSPENDED`, `DEACTIVATED`, `PENDING_VERIFICATION`, `BANNED`

**Usage**: Access control, borrowing permissions.

---

#### ClaimStatus, ClaimPriority, ClaimType
**Purpose**: Customer support ticket management.

**ClaimStatus**: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`, `REJECTED`

**ClaimPriority**: `LOW`, `MEDIUM`, `HIGH`, `URGENT`

**ClaimType**: `BOOK_DAMAGE`, `LOST_BOOK`, `INCORRECT_FEES`, `TECHNICAL_ISSUE`, `COMPLAINT`, `SUGGESTION`, `OTHER`

**Usage**: Support workflow management.

---

### 1.3 Data Models

#### Book Model
**Purpose**: Represents a physical book in the library collection.

**Attributes**:
```typescript
class Book {
  id: UUID;
  isbn: string;
  title: string;
  author: string;
  publisher: string;
  publicationYear: number;
  category: BookCategory;
  language: string;
  pageCount: number;
  physicalState: PhysicalState;
  isAvailable: boolean;
  isRestricted: boolean;
  location: string;
  addedDate: Date;
  lastUpdated: Date;
}
```

**Business Rules**:
- ISBN must be unique
- `REFERENCE` category books have different borrowing rules
- `DAMAGED` or `IN_REPAIR` books cannot be borrowed
- `isRestricted` books require special permission

---

#### BorrowingRecord Model
**Purpose**: Transaction record of book borrowing.

**Attributes**:
```typescript
class BorrowingRecord {
  id: UUID;
  bookId: UUID;
  borrowerId: UUID;
  borrowDate: Date;
  dueDate: Date;
  returnDate: Date | null;
  extensionCount: number;
  status: BorrowingStatus;
  fineAmount: number;
  notes: string;
}
```

**Business Rules**:
- Due date calculated based on book category
- Max 2 extensions allowed
- Fine calculated for overdue returns
- Status transitions: RESERVED → ACTIVE → RETURNED/OVERDUE

---

#### Comment Model
**Purpose**: User reviews and feedback on books.

**Attributes**:
```typescript
class Comment {
  id: UUID;
  bookId: UUID;
  userId: UUID;
  content: string;
  rating: number; // 1-5
  createdAt: Date;
  updatedAt: Date;
  isApproved: boolean;
  moderatorId: UUID | null;
}
```

**Business Rules**:
- Comments require moderation before public display
- Users can only edit their own comments
- Rating must be 1-5 stars
- Minimum content length enforced

---

#### Notification Model
**Purpose**: System notifications to users.

**Attributes**:
```typescript
class Notification {
  id: UUID;
  userId: UUID;
  type: NotificationType;
  message: string;
  isRead: boolean;
  createdAt: Date;
  readAt: Date | null;
}
```

**Business Rules**:
- Auto-send before due dates (configurable reminder days)
- Immediate notification for overdue books
- Notifications expire after 30 days

---

### 1.4 Domain Classes

#### Borrower Class
**Purpose**: Represents library users who borrow books.

**Implements**: `IUser`, `INotifiable`, `ISearchable`

**Key Responsibilities**:
- Profile management
- Book borrowing and returns
- Search and discovery
- Comment and review management
- Claim submission
- Notification handling

**Public Methods Count**: 27 methods mapping to business events

**Example Methods**:
```typescript
borrowBook(bookId: UUID): BorrowingRecord
returnBook(borrowingRecordId: UUID): void
extendBorrowingPeriod(recordId: UUID, days: number): boolean
searchByTitle(title: string): Book[]
addComment(bookId: UUID, content: string, rating: number): Comment
```

---

#### Library Class
**Purpose**: Central system orchestrator for library operations.

**Key Responsibilities**:
- Book inventory management
- User registration
- Borrowing/return processing
- Overdue tracking
- Due date reminders

**Public Methods Count**: 12 methods

**Example Methods**:
```typescript
addBook(book: Book): void
removeBook(bookId: UUID): void
registerUser(userData: UserProfile): Borrower
processBorrowing(userId: UUID, bookId: UUID): BorrowingRecord
processReturn(recordId: UUID): void
getOverdueBorrowings(): BorrowingRecord[]
sendDueDateReminders(): void
```

---

#### Librarian Class
**Purpose**: Library staff with administrative privileges.

**Implements**: `IUser`, `INotifiable`

**Key Responsibilities**:
- User management (suspend, activate, delete)
- Book management (add, update, restrict)
- Comment moderation
- System communications
- Administrative operations

**Public Methods Count**: 33 methods

**Example Methods**:
```typescript
suspendUser(userId: UUID, reason: string): void
deleteUser(userId: UUID): void
updateBook(bookId: UUID, updates: Partial<Book>): void
restrictBook(bookId: UUID, reason: string): void
approveComment(commentId: UUID): void
sendEmailToUser(userId: UUID, subject: string, body: string): void
```

---

## 2. Business Rules & Policies

### 2.1 Borrowing Policies

```typescript
const BORROWING_POLICIES = {
  MAX_BOOKS_PER_USER: 5,
  MAX_EXTENSION_COUNT: 2,
  EXTENSION_DAYS: 7,
  MIN_DAYS_BETWEEN_SAME_BOOK: 30,
  ALLOW_RENEWAL_WITH_RESERVATION: false
};
```

**Application**:
- Users can borrow maximum 5 books simultaneously
- Each borrowing can be extended twice (7 days each)
- 30-day cooldown before re-borrowing same book
- Renewals blocked if book has reservations

---

### 2.2 Time Management

```typescript
const TIME_POLICIES = {
  DEFAULT_BORROWING_PERIOD: 14, // days
  REFERENCE_BORROWING_PERIOD: 7, // days
  OVERDUE_GRACE_PERIOD: 2, // days
  REMINDER_DAYS_BEFORE_DUE: [3, 1] as const, // days before due date
  NOTIFICATION_RETENTION: 30 // days
};
```

**Application**:
- Standard books: 14 days borrowing period
- Reference books: 7 days only
- 2-day grace period before fines
- Reminders sent 3 days and 1 day before due date

---

### 2.3 Fee Structure

```typescript
const FEE_POLICIES = {
  DAILY_FINE_RATE: 0.50, // currency units
  MAX_FINE_PER_BOOK: 50.00,
  LOST_BOOK_FEE_MULTIPLIER: 2.0, // × book price
  DAMAGED_BOOK_FEE_PERCENTAGE: 0.75 // of book price
};
```

**Application**:
- $0.50 per day for overdue books
- Maximum fine capped at $50 per book
- Lost books charged at 2× replacement cost
- Damaged books: 75% of replacement cost

---

### 2.4 Access Control

```typescript
const ACCESS_POLICIES = {
  MIN_AGE_FOR_REGISTRATION: 13,
  REQUIRE_EMAIL_VERIFICATION: true,
  SUSPENDED_USER_CAN_VIEW: true,
  BANNED_USER_CAN_LOGIN: false
};
```

---

### 2.5 Validation Rules

```typescript
const VALIDATION_POLICIES = {
  MIN_COMMENT_LENGTH: 10,
  MAX_COMMENT_LENGTH: 500,
  MIN_RATING: 1,
  MAX_RATING: 5,
  ISBN_PATTERN: /^(?:\d{10}|\d{13})$/,
  MIN_PASSWORD_LENGTH: 8
};
```

---

## 3. Domain Events

### 3.1 Book Management Events

1. **L'utilisateur ajoute un nouveau livre** → `Library.addBook(book)`
2. **L'utilisateur supprime un livre du catalogue** → `Library.removeBook(bookId)`
3. **Le bibliothécaire met à jour les informations d'un livre** → `Librarian.updateBook(bookId, updates)`
4. **Le bibliothécaire restreint l'accès à un livre** → `Librarian.restrictBook(bookId, reason)`
5. **Le bibliothécaire lève la restriction d'un livre** → `Librarian.unrestrictBook(bookId)`
6. **Le bibliothécaire met à jour l'état physique d'un livre** → `Librarian.updatePhysicalState(bookId, state)`
7. **Le bibliothécaire modifie la disponibilité d'un livre** → `Librarian.setBookAvailability(bookId, isAvailable)`

---

### 3.2 User Management Events

8. **L'utilisateur s'inscrit au système** → `Library.registerUser(userData)`
9. **L'emprunteur met à jour son profil** → `Borrower.updateProfile(profileData)`
10. **Le bibliothécaire suspend un utilisateur** → `Librarian.suspendUser(userId, reason)`
11. **Le bibliothécaire réactive un compte suspendu** → `Librarian.unsuspendUser(userId)`
12. **Le bibliothécaire supprime un compte utilisateur** → `Librarian.deleteUser(userId)`
13. **L'utilisateur consulte son profil** → `Borrower.getProfile()` / `Librarian.getProfile()`

---

### 3.3 Borrowing Events

14. **L'emprunteur emprunte un livre** → `Borrower.borrowBook(bookId)`
15. **Le système traite un emprunt** → `Library.processBorrowing(userId, bookId)`
16. **L'emprunteur retourne un livre** → `Borrower.returnBook(recordId)`
17. **Le système traite un retour** → `Library.processReturn(recordId)`
18. **L'emprunteur demande une prolongation** → `Borrower.extendBorrowingPeriod(recordId, days)`
19. **L'emprunteur consulte ses emprunts en cours** → `Borrower.getMyBorrowedBooks()`
20. **L'emprunteur consulte son historique d'emprunts** → `Borrower.getMyBorrowingHistory()`
21. **Le système détecte les emprunts en retard** → `Library.getOverdueBorrowings()`

---

### 3.4 Notification Events

22. **Le système envoie un rappel de date d'échéance** → `Library.sendDueDateReminders()`
23. **L'utilisateur reçoit une notification** → `Borrower.receiveNotification()` / `Librarian.receiveNotification()`
24. **L'utilisateur marque une notification comme lue** → `Borrower.markNotificationAsRead(notificationId)`
25. **Le bibliothécaire envoie un email à un utilisateur** → `Librarian.sendEmailToUser(userId, subject, body)`
26. **Le bibliothécaire envoie un email à l'admin** → `Librarian.sendEmailToAdmin(subject, body)`

---

### 3.5 Administrative Events

27. **Le bibliothécaire approuve un commentaire** → `Librarian.approveComment(commentId)`
28. **Le bibliothécaire rejette un commentaire** → `Librarian.rejectComment(commentId, reason)`
29. **Le bibliothécaire consulte les commentaires en attente** → `Librarian.getPendingComments()`
30. **Le bibliothécaire publie une information générale** → `Librarian.postGeneralInfo(subject, message)`

---

## 4. Development Methodology

### 4.1 Event-Driven Design Principles

**Core Philosophy**: *One Event = One Public Method*

Each business event from the catalog becomes a single, well-defined public method:

```typescript
/**
 * Event: "L'emprunteur emprunte un livre"
 */
borrowBook(bookId: UUID): BorrowingRecord {
  // Implementation
}
```

**Benefits**:
1. **Clear API Contract**: Method signatures directly reflect business requirements
2. **Traceability**: Easy mapping between requirements and code
3. **Testability**: Each event has dedicated test cases
4. **Maintainability**: Changes to business rules isolated to specific methods
5. **Documentation**: Self-documenting code structure

---

### 4.2 SOLID Principles Application

#### Single Responsibility Principle (SRP)
- Each method handles one business event
- Classes have focused responsibilities (Borrower = user operations, Library = system coordination, Librarian = admin tasks)

#### Open/Closed Principle (OCP)
- New events add new methods without modifying existing ones
- Business rules externalized in POLICIES objects

#### Liskov Substitution Principle (LSP)
- Both Borrower and Librarian implement IUser consistently
- Interface contracts honored by all implementations

#### Interface Segregation Principle (ISP)
- Small, focused interfaces (INotifiable, ISearchable, IBorrowable)
- Classes implement only interfaces they need

#### Dependency Inversion Principle (DIP)
- Domain classes depend on abstractions (interfaces)
- Services injected via constructor (NotificationService, EmailService)

---

### 4.3 Testing Strategy

**Test Organization**:
```
tests/
├── domains/
│   ├── Borrower.test.ts (60+ tests)
│   ├── Library.test.ts (40+ tests)
│   └── Librarian.test.ts (30+ tests)
├── models/
│   ├── Book.test.ts
│   ├── BorrowingRecord.test.ts
│   ├── Comment.test.ts
│   └── Notification.test.ts
└── policies/
    └── business-rules.test.ts
```

**Test Pattern**:
```typescript
describe('Borrower - Book Operations', () => {
  test('Event: L\'emprunteur emprunte un livre - successful borrowing', () => {
    // Arrange
    const borrower = new Borrower(profile);
    
    // Act
    const record = borrower.borrowBook(bookId);
    
    // Assert
    expect(record.status).toBe(BorrowingStatus.ACTIVE);
  });
  
  test('Event: L\'emprunteur emprunte un livre - exceeds max books', () => {
    // Validation test
    expect(() => borrower.borrowBook(bookId))
      .toThrow('Maximum books limit reached');
  });
});
```

---

### 4.4 Code Organization

**Directory Structure**:
```
src/
├── enums/              # Type definitions (11 enums)
├── interfaces/         # Contracts (4 interfaces)
├── types/              # Type aliases and DTOs
├── models/             # Data models (4 models)
├── domains/            # Business logic (3 domain classes)
└── policies/           # Business rules (centralized)

tests/                  # Mirror src/ structure
methodology/            # This documentation
docs/                   # Additional documentation
```

**Import Aliases**:
```typescript
import { Book } from '@models/Book';
import { IUser } from '@interfaces/IUser';
import { BookCategory } from '@enums/BookCategory';
import { BORROWING_POLICIES } from '@policies/business-rules';
```

---

## Appendix A: Complete Event List

**Total Events**: 140+

**Categories**:
- Book Management: 25 events
- User Management: 18 events
- Borrowing Operations: 35 events
- Notifications: 22 events
- Search & Discovery: 15 events
- Comments & Reviews: 12 events
- Claims & Support: 8 events
- Administrative: 5 events

**Mapping**:
- Borrower class: 27 public methods
- Library class: 12 public methods
- Librarian class: 33 public methods

**Total**: 72 public methods implementing 140+ business events

---

## Appendix B: UML Diagrams

*[To be generated from implementation]*

**Diagrams to include**:
1. Class Diagram - complete system overview
2. Interface Inheritance Diagram
3. Borrowing Workflow Sequence Diagram
4. User Management State Diagram
5. Notification Flow Diagram

---

## Appendix C: API Reference

*[Auto-generated from TypeDoc]*

**Documentation Coverage**:
- All 72 public methods with JSDoc comments
- Event references in method documentation
- Parameter validation rules
- Return types and error conditions
- Usage examples

---

## 🎯 Conclusion

This methodology guide demonstrates how **event-driven design** combined with **SOLID principles** creates a maintainable, testable, and scalable library management system.

**Key Takeaways**:
1. Events from business requirements → Public methods in code
2. Centralized business rules in POLICIES objects
3. Small, focused interfaces for flexibility
4. Comprehensive test coverage for reliability
5. Clear documentation for maintainability

**Next Steps**:
- Port to FastAPI for Python implementation
- Add real service integrations (Email, Notifications)
- Implement CI/CD pipeline
- Generate API documentation

---

*Generated from TypeScript implementation - February 2026*
