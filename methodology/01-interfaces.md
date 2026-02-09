# 🔌 Interfaces

[← Retour à l'index](README.md)

---

## Interface INotifiable

Permet la gestion des notifications et de la communication par email pour les entités du système.

### Méthodes

```typescript
interface INotifiable {
  sendNotification(recipientId: UUID, message: string, type: NotificationType): void;
  sendEmail(recipientEmail: string, subject: string, body: string): void;
  receiveNotification(): Notification[];
  markNotificationAsRead(notificationId: UUID): void;
}
```

### Description des Méthodes

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| `sendNotification` | Envoie une notification à un destinataire | recipientId, message, type | void |
| `sendEmail` | Envoie un email | recipientEmail, subject, body | void |
| `receiveNotification` | Récupère toutes les notifications reçues | - | Notification[] |
| `markNotificationAsRead` | Marque une notification comme lue | notificationId | void |

### Implémentée par
- `Borrower` - Pour recevoir et envoyer des notifications
- `Librarian` - Pour gérer les communications administratives

---

## Interface IBorrowable

Définit le contrat pour les entités pouvant être empruntées.

### Méthodes

```typescript
interface IBorrowable {
  canBeBorrowed(): boolean;
  borrow(borrowerId: UUID): BorrowingRecord;
  return(borrowerId: UUID): void;
  extendBorrowingPeriod(days: number): boolean;
  getBorrowingHistory(): BorrowingRecord[];
}
```

### Description des Méthodes

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| `canBeBorrowed` | Vérifie si l'entité peut être empruntée | - | boolean |
| `borrow` | Crée un enregistrement d'emprunt | borrowerId | BorrowingRecord |
| `return` | Traite le retour | borrowerId | void |
| `extendBorrowingPeriod` | Prolonge la période d'emprunt | days | boolean |
| `getBorrowingHistory` | Récupère l'historique complet | - | BorrowingRecord[] |

### Implémentée par
- `Book` - Gestion des emprunts de livres

---

## Interface IUser

Interface de base pour tous les utilisateurs du système (emprunteurs et bibliothécaires).

### Méthodes

```typescript
interface IUser {
  getProfile(): UserProfile;
  updateProfile(profileData: Partial<UserProfile>): void;
  isActive(): boolean;
  getId(): UUID;
}
```

### Description des Méthodes

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| `getProfile` | Récupère le profil complet de l'utilisateur | - | UserProfile |
| `updateProfile` | Met à jour les informations du profil | profileData | void |
| `isActive` | Vérifie si le compte est actif | - | boolean |
| `getId` | Récupère l'identifiant unique | - | UUID |

### Implémentée par
- `Borrower` - Utilisateurs emprunteurs
- `Librarian` - Personnel de la bibliothèque

---

## Interface ISearchable

Définit les capacités de recherche et de filtrage dans le système.

### Méthodes

```typescript
interface ISearchable {
  searchByTitle(title: string): Book[];
  searchByAuthor(author: string): Book[];
  searchByISBN(isbn: string): Book | null;
  searchAvailableBooks(): Book[];
  filterBooks(criteria: SearchCriteria): Book[];
}
```

### Description des Méthodes

| Méthode | Description | Paramètres | Retour |
|---------|-------------|------------|--------|
| `searchByTitle` | Recherche par titre (partiel ou complet) | title | Book[] |
| `searchByAuthor` | Recherche par nom d'auteur | author | Book[] |
| `searchByISBN` | Recherche exacte par ISBN | isbn | Book \| null |
| `searchAvailableBooks` | Récupère tous les livres disponibles | - | Book[] |
| `filterBooks` | Filtre selon critères multiples | criteria | Book[] |

### Type SearchCriteria

```typescript
type SearchCriteria = {
  category?: BookCategory;
  year?: number;
  minRating?: number;
  availability?: boolean;
  physicalState?: PhysicalState;
  publisher?: string;
};
```

### Implémentée par
- `Borrower` - Recherche de livres par les utilisateurs
- `Library` (potentiel) - Recherche système

---

## 🎯 Principes de Design

### Ségrégation des Interfaces (ISP)
Chaque interface a une responsabilité unique et focalisée:
- **INotifiable** → Communication uniquement
- **IBorrowable** → Logique d'emprunt uniquement
- **IUser** → Gestion de profil uniquement
- **ISearchable** → Recherche uniquement

### Composition > Héritage
Les classes implémentent plusieurs interfaces selon leurs besoins:
```typescript
class Borrower implements IUser, INotifiable, ISearchable { }
class Librarian implements IUser, INotifiable { }
class Book implements IBorrowable { }
```

### Contract-Based Development
Les interfaces définissent des contrats clairs que toutes les implémentations doivent respecter.

---

## 📚 Exemples d'Utilisation

### Exemple INotifiable
```typescript
class Borrower implements INotifiable {
  sendNotification(recipientId: UUID, message: string, type: NotificationType): void {
    const notification = new Notification({
      recipientId,
      type,
      message,
      createdDate: new Date(),
      isRead: false
    });
    // Enregistrer et envoyer
  }
}
```

### Exemple ISearchable
```typescript
class Borrower implements ISearchable {
  searchByTitle(title: string): Book[] {
    return this.libraryService
      .getAllBooks()
      .filter(book => book.title.toLowerCase().includes(title.toLowerCase()));
  }
}
```

---

[← Retour à l'index](README.md) | [Énumérations →](02-enums.md)
