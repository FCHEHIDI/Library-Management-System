# 📐 Class Diagram - Library Management System

[← Retour UML](README.md)

---

## Diagramme de Classes Complet

```mermaid
classDiagram
    %% Interfaces
    class IUser {
        <<interface>>
        +getProfile() UserProfile
        +updateProfile(profileData) void
        +isActive() boolean
        +getId() UUID
    }
    
    class INotifiable {
        <<interface>>
        +sendNotification(recipientId, message, type) void
        +sendEmail(recipientEmail, subject, body) void
        +receiveNotification() Notification[]
        +markNotificationAsRead(notificationId) void
    }
    
    class ISearchable {
        <<interface>>
        +searchByTitle(title) Book[]
        +searchByAuthor(author) Book[]
        +searchByISBN(isbn) Book|null
        +searchAvailableBooks() Book[]
        +filterBooks(criteria) Book[]
    }
    
    class IBorrowable {
        <<interface>>
        +canBeBorrowed() boolean
        +borrow(borrowerId) BorrowingRecord
        +return(borrowerId) void
        +extendBorrowingPeriod(days) boolean
        +getBorrowingHistory() BorrowingRecord[]
    }
    
    %% Enums
    class BookCategory {
        <<enumeration>>
        FICTION
        NON_FICTION
        SCIENCE
        TECHNOLOGY
        HISTORY
        REFERENCE
        +25 more...
    }
    
    class PhysicalState {
        <<enumeration>>
        EXCELLENT
        GOOD
        FAIR
        POOR
        DAMAGED
        LOST
        IN_REPAIR
    }
    
    class BorrowingStatus {
        <<enumeration>>
        ACTIVE
        RETURNED
        OVERDUE
        EXTENDED
        CANCELLED
        RESERVED
    }
    
    class NotificationType {
        <<enumeration>>
        DUE_DATE
        OVERDUE
        EXTENSION_APPROVED
        AVAILABILITY
        +10 more...
    }
    
    class UserStatus {
        <<enumeration>>
        ACTIVE
        INACTIVE
        SUSPENDED
        DEACTIVATED
        PENDING
        BANNED
    }
    
    %% Models
    class Book {
        -UUID id
        -string title
        -string author
        -string ISBN
        -string publisher
        -number publicationYear
        -BookCategory category
        -boolean isAvailable
        -PhysicalState physicalState
        -boolean isRestricted
        -Date addedDate
        -string description
        +Book(data)
    }
    
    class BorrowingRecord {
        -UUID id
        -UUID bookId
        -UUID borrowerId
        -Date borrowDate
        -Date dueDate
        -Date returnDate
        -boolean isExtended
        -number extensionCount
        -BorrowingStatus status
        +BorrowingRecord(data)
    }
    
    class Comment {
        -UUID id
        -UUID bookId
        -UUID userId
        -string content
        -number rating
        -Date createdDate
        -boolean isApproved
        +Comment(data)
    }
    
    class Notification {
        -UUID id
        -UUID recipientId
        -UUID senderId
        -NotificationType type
        -string message
        -Date createdDate
        -boolean isRead
        +Notification(data)
    }
    
    %% Domain Classes
    class Borrower {
        -UUID id
        -string name
        -string firstname
        -string email
        -string phone
        -string address
        -Date registrationDate
        -boolean isAuthorized
        -boolean isActiveStatus
        -Date suspensionEndDate
        -UUID[] borrowedBooks
        -number maxBooksAllowed
        +borrowBook(bookId) BorrowingRecord
        +returnBook(recordId) void
        +extendBorrowingPeriod(recordId, days) boolean
        +getMyBorrowedBooks() Book[]
        +getMyBorrowingHistory() BorrowingRecord[]
        +searchByTitle(title) Book[]
        +searchByAuthor(author) Book[]
        +searchByISBN(isbn) Book|null
        +addComment(bookId, content, rating) Comment
        +sendClaim(subject, description) void
        -canBorrow() boolean
    }
    
    class Librarian {
        -UUID id
        -string name
        -string firstname
        -string email
        -string phone
        -Date hireDate
        -LibrarianRole role
        -boolean isActiveStatus
        +addBook(bookData) Book
        +deleteBookById(bookId) void
        +updateBook(bookId, bookData) Book
        +restrictBook(bookId, reason) void
        +updatePhysicalState(bookId, state) void
        +addUser(userData) Borrower
        +suspendUser(userId, duration, reason) void
        +deleteUser(userId) void
        +approveComment(commentId) void
        +rejectComment(commentId, reason) void
        +sendEmailToUser(userId, subject, body) void
    }
    
    class Library {
        -UUID id
        -string name
        -string address
        -string phone
        -string email
        -OpeningHours openingHours
        -Map~UUID,Book~ books
        -Map~UUID,Borrower~ users
        -Map~UUID,Librarian~ librarians
        -Map~UUID,BorrowingRecord~ borrowingRecords
        +addBook(book) void
        +removeBook(bookId) void
        +getBook(bookId) Book
        +getAllBooks() Book[]
        +getAvailableBooks() Book[]
        +registerUser(userData) Borrower
        +processBorrowing(userId, bookId) BorrowingRecord
        +processReturn(recordId) void
        +getOverdueBorrowings() BorrowingRecord[]
        +sendDueDateReminders() void
        -calculateDueDate(borrowDate, category) Date
    }
    
    %% Relationships - Interfaces
    Borrower ..|> IUser
    Borrower ..|> INotifiable
    Borrower ..|> ISearchable
    Librarian ..|> IUser
    Librarian ..|> INotifiable
    Book ..|> IBorrowable
    
    %% Relationships - Composition/Aggregation
    Library o-- Book : contains
    Library o-- Borrower : manages
    Library o-- Librarian : employs
    Library o-- BorrowingRecord : tracks
    Library o-- Notification : stores
    
    %% Relationships - Associations
    Book "1" -- "*" BorrowingRecord : has
    Borrower "1" -- "*" BorrowingRecord : creates
    Book "1" -- "*" Comment : receives
    Borrower "1" -- "*" Comment : writes
    Borrower "1" -- "*" Notification : receives
    Librarian "1" -- "*" Notification : receives
    
    %% Relationships - Dependencies (Enums)
    Book ..> BookCategory : uses
    Book ..> PhysicalState : uses
    BorrowingRecord ..> BorrowingStatus : uses
    Notification ..> NotificationType : uses
    Borrower ..> UserStatus : uses
```

---

## 📊 Analyse du Diagramme

### Interfaces (4)
- **IUser**: Contrat de base pour tous les utilisateurs
- **INotifiable**: Capacités de communication
- **ISearchable**: Capacités de recherche
- **IBorrowable**: Gestion des emprunts

### Enums (5 principales)
- **BookCategory**: 25 catégories de livres
- **PhysicalState**: 7 états physiques
- **BorrowingStatus**: 6 statuts d'emprunt
- **NotificationType**: 14 types de notifications
- **UserStatus**: 6 statuts utilisateur

### Models (4)
- **Book**: 15 attributs, représente un livre physique
- **BorrowingRecord**: 9 attributs, enregistrement d'emprunt
- **Comment**: 7 attributs, avis utilisateur
- **Notification**: 7 attributs, message système

### Domain Classes (3)
- **Borrower**: 27 méthodes publiques, implémente 3 interfaces
- **Librarian**: 33 méthodes publiques, implémente 2 interfaces
- **Library**: 12 méthodes publiques, coordinateur central

---

## 🔗 Relations Clés

### Implémentation d'Interfaces
```
Borrower → IUser + INotifiable + ISearchable
Librarian → IUser + INotifiable
Book → IBorrowable
```

### Associations
```
Book 1 ─── * BorrowingRecord
Borrower 1 ─── * BorrowingRecord
Book 1 ─── * Comment
Borrower 1 ─── * Comment
```

### Composition (Library est le conteneur)
```
Library ◆─── Book
Library ◆─── Borrower
Library ◆─── Librarian
Library ◆─── BorrowingRecord
```

---

## 🎯 Principes SOLID Illustrés

### Single Responsibility
Chaque classe a une responsabilité unique:
- Book: Représente un livre
- Borrower: Gère les emprunts utilisateur
- Library: Orchestre le système

### Interface Segregation
Interfaces petites et focalisées:
- IUser: 4 méthodes (profil de base)
- INotifiable: 4 méthodes (communication)
- ISearchable: 5 méthodes (recherche)

### Dependency Inversion
Les classes dépendent d'abstractions (interfaces), pas de concrétions.

---

[← Retour UML](README.md) | [ER Diagram →](02-er-diagram.md)
