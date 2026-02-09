# 🏛️ Classe Library

[← Retour à l'index](README.md) | [← Borrower](05-class-borrower.md)

---

## Vue d'Ensemble

**Responsabilité**: Système central orchestrant toutes les opérations de la bibliothèque. Gère les collections de livres, utilisateurs, emprunts et notifications.

**Pattern**: Singleton / Central Coordinator

**Nombre total de méthodes publiques**: 12

---

## Attributs du Constructeur

```typescript
class Library {
  id: UUID;
  name: string;
  address: string;
  phone: string;
  email: string;
  openingHours: OpeningHours;
  books: Map<UUID, Book>;
  users: Map<UUID, Borrower>;
  librarians: Map<UUID, Librarian>;
  borrowingRecords: Map<UUID, BorrowingRecord>;
  notifications: Map<UUID, Notification>;
}
```

### Description des Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `id` | UUID | Identifiant unique de la bibliothèque |
| `name` | string | Nom de la bibliothèque |
| `address` | string | Adresse physique |
| `phone` | string | Téléphone de contact |
| `email` | string | Email de contact |
| `openingHours` | OpeningHours | Horaires d'ouverture |
| `books` | Map<UUID, Book> | Collection de tous les livres |
| `users` | Map<UUID, Borrower> | Tous les emprunteurs enregistrés |
| `librarians` | Map<UUID, Librarian> | Personnel de la bibliothèque |
| `borrowingRecords` | Map<UUID, BorrowingRecord> | Tous les enregistrements d'emprunt |
| `notifications` | Map<UUID, Notification> | Toutes les notifications système |

### Type OpeningHours

```typescript
type OpeningHours = {
  monday: { open: string; close: string } | null;
  tuesday: { open: string; close: string } | null;
  wednesday: { open: string; close: string } | null;
  thursday: { open: string; close: string } | null;
  friday: { open: string; close: string } | null;
  saturday: { open: string; close: string } | null;
  sunday: { open: string; close: string } | null;
};
```

**Exemple**:
```typescript
{
  monday: { open: "09:00", close: "18:00" },
  saturday: { open: "10:00", close: "16:00" },
  sunday: null // Fermé
}
```

---

## Méthodes - Gestion des Livres (5 méthodes)

### addBook
```typescript
addBook(book: Book): void
```
**Événement**: *Le système ajoute un livre au catalogue*

Ajoute un nouveau livre à la collection.

**Paramètres**:
- `book`: Instance complète du livre

**Validation**:
- ISBN unique dans `books` Map
- Toutes les propriétés requises présentes

**Effet**:
```typescript
this.books.set(book.id, book);
```

---

### removeBook
```typescript
removeBook(bookId: UUID): void
```
**Événement**: *Le système supprime un livre du catalogue*

Retire un livre de la collection.

**Validation**:
- Livre existe
- Aucun emprunt actif (`borrowingRecords` ne contient d'ACTIVE pour ce livre)

**Effet**:
```typescript
this.books.delete(bookId);
```

---

### getBook
```typescript
getBook(bookId: UUID): Book
```
**Événement**: *Le système récupère un livre par ID*

Récupère un livre spécifique.

**Retour**: Instance du livre

**Erreur**: Si livre non trouvé

---

### getAllBooks
```typescript
getAllBooks(): Book[]
```
**Événement**: *Le système récupère tous les livres*

Retourne la liste complète de tous les livres du catalogue.

**Retour**: Array de tous les livres

**Implémentation**:
```typescript
return Array.from(this.books.values());
```

---

### getAvailableBooks
```typescript
getAvailableBooks(): Book[]
```
**Événement**: *Le système récupère les livres disponibles*

Retourne uniquement les livres disponibles pour emprunt.

**Filtre**:
```typescript
return this.getAllBooks().filter(book => 
  book.isAvailable 
  && !book.isRestricted
  && book.physicalState !== PhysicalState.DAMAGED
  && book.physicalState !== PhysicalState.LOST
  && book.physicalState !== PhysicalState.IN_REPAIR
);
```

---

## Méthodes - Gestion des Utilisateurs (3 méthodes)

### registerUser
```typescript
registerUser(userData: UserData): Borrower
```
**Événement**: *L'utilisateur s'inscrit au système*

Enregistre un nouvel utilisateur emprunteur.

**Paramètres**:
- `userData`: Données d'inscription (nom, prénom, email, téléphone, adresse)

**Validation**:
- Email unique
- Âge minimum respecté (13 ans par défaut)
- Champs requis présents

**Effet**:
```typescript
const borrower = new Borrower(userData);
this.users.set(borrower.id, borrower);
return borrower;
```

**Retour**: Instance du Borrower créé

---

### getUser
```typescript
getUser(userId: UUID): Borrower
```
**Événement**: *Le système récupère un utilisateur par ID*

Récupère un utilisateur spécifique.

**Retour**: Instance du Borrower

---

### getAllUsers
```typescript
getAllUsers(): Borrower[]
```
**Événement**: *Le système récupère tous les utilisateurs*

Retourne la liste de tous les utilisateurs enregistrés.

**Implémentation**:
```typescript
return Array.from(this.users.values());
```

---

## Méthodes - Gestion des Emprunts (4 méthodes)

### processBorrowing
```typescript
processBorrowing(userId: UUID, bookId: UUID): BorrowingRecord
```
**Événement**: *Le système traite une demande d'emprunt*

Traite et valide un emprunt de livre.

**Paramètres**:
- `userId`: ID de l'emprunteur
- `bookId`: ID du livre

**Validation**:
1. Utilisateur existe et est actif
2. Utilisateur autorisé à emprunter
3. Utilisateur n'a pas atteint la limite de livres
4. Livre existe et est disponible
5. Livre n'est pas restreint
6. Livre en bon état physique

**Traitement**:
```typescript
const dueDate = this.calculateDueDate(new Date(), book.category);
const record = new BorrowingRecord({
  bookId,
  borrowerId: userId,
  borrowDate: new Date(),
  dueDate,
  status: BorrowingStatus.ACTIVE,
  extensionCount: 0
});

book.isAvailable = false;
user.borrowedBooks.push(bookId);
this.borrowingRecords.set(record.id, record);

return record;
```

**Retour**: Enregistrement d'emprunt créé

---

### processReturn
```typescript
processReturn(recordId: UUID): void
```
**Événement**: *Le système traite un retour de livre*

Traite le retour d'un livre emprunté.

**Paramètres**:
- `recordId`: ID de l'enregistrement d'emprunt

**Traitement**:
```typescript
const record = this.borrowingRecords.get(recordId);
const book = this.books.get(record.bookId);
const user = this.users.get(record.borrowerId);

record.returnDate = new Date();
record.status = BorrowingStatus.RETURNED;
book.isAvailable = true;

// Retirer du tableau des livres empruntés
user.borrowedBooks = user.borrowedBooks.filter(id => id !== book.id);

// Calculer frais de retard si applicable
if (record.returnDate > record.dueDate) {
  const lateDays = calculateLateDays(record.returnDate, record.dueDate);
  const fee = Math.min(
    lateDays * FEE_POLICIES.LATE_FEE_PER_DAY,
    FEE_POLICIES.MAX_LATE_FEE
  );
  // Enregistrer frais...
}
```

---

### getOverdueBorrowings
```typescript
getOverdueBorrowings(): BorrowingRecord[]
```
**Événement**: *Le système détecte les emprunts en retard*

Retourne tous les emprunts en retard.

**Filtre**:
```typescript
const now = new Date();
return Array.from(this.borrowingRecords.values()).filter(record =>
  record.status === BorrowingStatus.ACTIVE
  && record.dueDate < now
);
```

**Usage**: Tâche planifiée quotidienne, envoi de notifications

---

### sendDueDateReminders
```typescript
sendDueDateReminders(): void
```
**Événement**: *Le système envoie des rappels de date de retour*

Envoie des rappels automatiques avant les dates d'échéance.

**Logique**:
```typescript
const now = new Date();
const reminderDays = TIME_POLICIES.REMINDER_DAYS_BEFORE_DUE; // [3, 1]

const activeRecords = Array.from(this.borrowingRecords.values())
  .filter(r => r.status === BorrowingStatus.ACTIVE);

for (const record of activeRecords) {
  const daysUntilDue = calculateDaysDifference(record.dueDate, now);
  
  if (reminderDays.includes(daysUntilDue)) {
    const user = this.users.get(record.borrowerId);
    const book = this.books.get(record.bookId);
    
    this.sendNotification(
      user.id,
      `Rappel: "${book.title}" à retourner dans ${daysUntilDue} jour(s)`,
      NotificationType.DUE_DATE
    );
  }
}
```

**Fréquence**: Exécuté quotidiennement (tâche CRON)

**Rappels envoyés**:
- J-3: "Rappel: livre à retourner dans 3 jours"
- J-1: "Rappel: livre à retourner demain"

---

## Méthode Privée

### calculateDueDate (private)
```typescript
private calculateDueDate(borrowDate: Date, category: BookCategory): Date {
  const days = category === BookCategory.REFERENCE
    ? TIME_POLICIES.REFERENCE_BORROWING_PERIOD
    : TIME_POLICIES.DEFAULT_BORROWING_PERIOD;
  
  return addDays(borrowDate, days);
}
```

Calcule la date de retour en fonction de la catégorie du livre:
- **REFERENCE**: 7 jours
- **Autres**: 14 jours

---

## 📊 Récapitulatif des Méthodes

| Catégorie | Nombre | Méthodes |
|-----------|--------|----------|
| **Gestion Livres** | 5 | add, remove, get, getAll, getAvailable |
| **Gestion Users** | 3 | register, get, getAll |
| **Gestion Emprunts** | 4 | processBorrowing, processReturn, getOverdue, sendReminders |
| **TOTAL PUBLIC** | **12** | |
| **TOTAL PRIVÉ** | **1** | calculateDueDate |

---

## 🔄 Flux de Travail Principal

### Workflow d'Emprunt

```
1. User → borrowBook(bookId)
2. Borrower → Appelle Library.processBorrowing(userId, bookId)
3. Library → Valide toutes les conditions
4. Library → Crée BorrowingRecord
5. Library → Met à jour Book.isAvailable = false
6. Library → Met à jour User.borrowedBooks.push(bookId)
7. Library → Retourne BorrowingRecord
```

### Workflow de Retour

```
1. User → returnBook(recordId)
2. Borrower → Appelle Library.processReturn(recordId)
3. Library → Récupère BorrowingRecord
4. Library → Met à jour record.returnDate = now
5. Library → Met à jour record.status = RETURNED
6. Library → Met à jour Book.isAvailable = true
7. Library → Retire bookId de User.borrowedBooks
8. Library → Calcule frais de retard si applicable
```

### Tâches Planifiées

```
Quotidiennement (CRON):
  - sendDueDateReminders() → Rappels J-3 et J-1
  - getOverdueBorrowings() → Détection retards
  - Envoi notifications de retard (J+1, J+7, J+14, J+30)
  - Nettoyage notifications lues > 30 jours
```

---

## 🎯 Rôle dans l'Architecture

La classe **Library** agit comme le **coordinateur central** du système:

- **Point d'entrée unique** pour les opérations d'emprunt/retour
- **Source de vérité** pour l'état du système (collections Map)
- **Orchestrateur** des workflows complexes
- **Gestionnaire** des tâches automatisées (rappels, détection retards)

**Pattern**: Façade + Repository + Service Layer

---

[← Borrower](05-class-borrower.md) | [Retour à l'index](README.md) | [Catalogue d'Événements →](07-events-catalog.md)
