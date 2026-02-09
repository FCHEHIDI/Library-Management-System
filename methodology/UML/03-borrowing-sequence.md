# 📖 Borrowing Sequence Diagram

[← Retour UML](README.md) | [← Class Diagram](01-class-diagram.md)

---

## Workflow d'Emprunt de Livre

Ce diagramme illustre le processus complet d'emprunt d'un livre par un utilisateur.

```mermaid
sequenceDiagram
    actor User as 👤 Utilisateur
    participant Borrower
    participant Library
    participant Book
    participant BorrowingRecord
    participant Notification
    
    User->>+Borrower: borrowBook(bookId)
    Note over Borrower: Validation des conditions
    Borrower->>Borrower: canBorrow()
    alt Compte inactif
        Borrower-->>User: ❌ Error: Account inactive
    else Non autorisé
        Borrower-->>User: ❌ Error: Not authorized
    else Suspendu
        Borrower-->>User: ❌ Error: Account suspended
    else Limite atteinte
        Borrower-->>User: ❌ Error: Max books limit reached
    end
    
    Borrower->>+Library: processBorrowing(userId, bookId)
    
    Library->>+Book: get(bookId)
    Book-->>-Library: book
    
    alt Livre non disponible
        Library-->>Borrower: ❌ Error: Book not available
        Borrower-->>User: ❌ Error
    else Livre endommagé
        Library-->>Borrower: ❌ Error: Book damaged
        Borrower-->>User: ❌ Error
    end
    
    Note over Library: Validation complète
    Library->>Library: validateBorrowingConditions()
    
    Note over Library: Calcul date de retour
    Library->>Library: calculateDueDate(borrowDate, category)
    Note right of Library: REFERENCE: 7 jours<br/>DEFAULT: 14 jours
    
    Library->>+BorrowingRecord: new(bookId, userId, dates)
    BorrowingRecord-->>-Library: record
    
    Note over Library: Mise à jour état
    Library->>Book: setAvailable(false)
    Library->>Borrower: addBorrowedBook(bookId)
    
    Library->>Library: saveBorrowingRecord(record)
    
    Library-->>-Borrower: ✅ BorrowingRecord
    Borrower-->>-User: ✅ BorrowingRecord
    
    Note over Library,Notification: Notification automatique
    Library->>+Notification: new(userId, "Emprunt confirmé", DUE_DATE)
    Notification-->>-Library: notification
    Library->>User: 📧 Notification envoyée
```

---

## 📋 Étapes Détaillées

### 1. Validation Utilisateur (Borrower.canBorrow())

```typescript
private canBorrow(): boolean {
  return this.isActiveStatus
    && this.isAuthorized
    && this.suspensionEndDate === null
    && this.borrowedBooks.length < BORROWING_POLICIES.MAX_BOOKS_PER_USER;
}
```

**Vérifications**:
- ✅ Compte actif (`isActiveStatus = true`)
- ✅ Autorisé à emprunter (`isAuthorized = true`)
- ✅ Non suspendu (`suspensionEndDate = null`)
- ✅ Limite de livres non atteinte (< 5 par défaut)

### 2. Validation Livre (Library.processBorrowing())

**Vérifications**:
- ✅ Livre existe
- ✅ Livre disponible (`isAvailable = true`)
- ✅ Livre non restreint (`isRestricted = false`)
- ✅ État physique acceptable (`!= DAMAGED, LOST, IN_REPAIR`)

### 3. Calcul Date de Retour

```typescript
private calculateDueDate(borrowDate: Date, category: BookCategory): Date {
  const days = category === BookCategory.REFERENCE
    ? TIME_POLICIES.REFERENCE_BORROWING_PERIOD  // 7 jours
    : TIME_POLICIES.DEFAULT_BORROWING_PERIOD;   // 14 jours
  
  return addDays(borrowDate, days);
}
```

### 4. Création BorrowingRecord

```typescript
{
  id: UUID,
  bookId: UUID,
  borrowerId: UUID,
  borrowDate: new Date(),
  dueDate: calculatedDate,
  returnDate: null,
  extensionCount: 0,
  status: BorrowingStatus.ACTIVE
}
```

### 5. Mise à Jour État

**Modifications effectuées**:
```typescript
// Livre
book.isAvailable = false;

// Utilisateur
borrower.borrowedBooks.push(bookId);

// Système
library.borrowingRecords.set(record.id, record);
```

### 6. Notification

**Notification immédiate**:
```typescript
{
  type: NotificationType.DUE_DATE,
  message: "Livre emprunté avec succès. À retourner avant le DD/MM/YYYY",
  recipientId: userId
}
```

---

## 🔄 Scénarios Alternatifs

### Échec: Compte Suspendu

```mermaid
sequenceDiagram
    actor User
    participant Borrower
    
    User->>Borrower: borrowBook(bookId)
    Borrower->>Borrower: canBorrow()
    Note over Borrower: suspensionEndDate = 2026-03-15
    Borrower-->>User: ❌ Error: Account suspended until 15/03/2026
```

### Échec: Limite de Livres Atteinte

```mermaid
sequenceDiagram
    actor User
    participant Borrower
    
    User->>Borrower: borrowBook(bookId)
    Borrower->>Borrower: canBorrow()
    Note over Borrower: borrowedBooks.length = 5<br/>MAX_BOOKS_PER_USER = 5
    Borrower-->>User: ❌ Error: Maximum books limit reached (5/5)
```

### Échec: Livre Non Disponible

```mermaid
sequenceDiagram
    actor User
    participant Borrower
    participant Library
    participant Book
    
    User->>Borrower: borrowBook(bookId)
    Borrower->>Borrower: canBorrow() ✅
    Borrower->>Library: processBorrowing(userId, bookId)
    Library->>Book: get(bookId)
    Book-->>Library: book { isAvailable: false }
    Library-->>Borrower: ❌ Error: Book not available
    Borrower-->>User: ❌ Book currently borrowed
```

---

## ⏱️ Timing et Performance

| Étape | Temps estimé | Criticité |
|-------|--------------|-----------|
| Validation utilisateur | < 1ms | Haute |
| Récupération livre | < 5ms | Haute |
| Validation livre | < 1ms | Haute |
| Calcul date | < 1ms | Moyenne |
| Création record | < 5ms | Haute |
| Mise à jour état | < 10ms | Critique |
| Notification | Async | Basse |
| **TOTAL** | **< 25ms** | |

---

## 🎯 Business Rules Appliquées

```typescript
// Règles utilisées dans ce workflow
BORROWING_POLICIES.MAX_BOOKS_PER_USER = 5
TIME_POLICIES.DEFAULT_BORROWING_PERIOD = 14  // jours
TIME_POLICIES.REFERENCE_BORROWING_PERIOD = 7 // jours
ACCESS_POLICIES.MIN_ACCOUNT_AGE_DAYS = 1
```

---

## 📊 États Modifiés

### Avant l'Emprunt
```
Book:
  isAvailable: true

Borrower:
  borrowedBooks: [book1, book2]  // 2 livres

BorrowingRecord:
  N/A
```

### Après l'Emprunt
```
Book:
  isAvailable: false

Borrower:
  borrowedBooks: [book1, book2, book3]  // 3 livres

BorrowingRecord:
  {
    status: ACTIVE,
    dueDate: borrowDate + 14 jours,
    extensionCount: 0
  }
```

---

[← Class Diagram](01-class-diagram.md) | [Retour UML](README.md) | [Return Sequence →](04-return-sequence.md)
