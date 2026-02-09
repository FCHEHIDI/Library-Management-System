# 📦 Modèles de Données

[← Retour à l'index](README.md) | [← Énumérations](02-enums.md)

---

## Book

Représente un livre physique dans le catalogue de la bibliothèque.

### Attributs du Constructeur

```typescript
class Book {
  id: UUID;
  title: string;
  author: string;
  ISBN: string;
  publisher: string;
  publicationYear: number;
  category: BookCategory;
  isAvailable: boolean;
  physicalState: PhysicalState;
  borrowingHistory: BorrowingRecord[];
  isRestricted: boolean;
  addedDate: Date;
  lastModified: Date;
  description: string;
  coverImageUrl: string;
}
```

### Description des Attributs

| Attribut | Type | Description | Contraintes |
|----------|------|-------------|-------------|
| `id` | UUID | Identifiant unique | Généré automatiquement |
| `title` | string | Titre du livre | 1-255 caractères |
| `author` | string | Nom de l'auteur | Requis |
| `ISBN` | string | Numéro ISBN | 10 ou 13 chiffres, unique |
| `publisher` | string | Maison d'édition | Optionnel |
| `publicationYear` | number | Année de publication | > 0 |
| `category` | BookCategory | Catégorie du livre | Enum BookCategory |
| `isAvailable` | boolean | Disponibilité pour emprunt | true/false |
| `physicalState` | PhysicalState | État physique | Enum PhysicalState |
| `borrowingHistory` | BorrowingRecord[] | Historique complet | Lecture seule |
| `isRestricted` | boolean | Accès restreint | Nécessite autorisation |
| `addedDate` | Date | Date d'ajout au catalogue | Auto |
| `lastModified` | Date | Dernière modification | Auto |
| `description` | string | Description/résumé | 0-2000 caractères |
| `coverImageUrl` | string | URL de la couverture | Optionnel |

### Règles Métier

**Empruntabilité**:
- `isAvailable = true` ET
- `physicalState ∉ [DAMAGED, LOST, IN_REPAIR]` ET
- `isRestricted = false` (ou utilisateur autorisé)

**Durée d'emprunt**:
- Catégorie `REFERENCE`: 7 jours
- Autres catégories: 14 jours

**Validation ISBN**:
```typescript
// ISBN-10: 10 chiffres (dernier peut être X)
// ISBN-13: 13 chiffres
const isValidISBN = /^(?:\d{9}[\dX]|\d{13})$/.test(isbn);
```

---

## BorrowingRecord

Enregistrement d'un emprunt de livre par un utilisateur.

### Attributs du Constructeur

```typescript
class BorrowingRecord {
  id: UUID;
  bookId: UUID;
  borrowerId: UUID;
  borrowDate: Date;
  dueDate: Date;
  returnDate: Date | null;
  isExtended: boolean;
  extensionCount: number;
  status: BorrowingStatus;
}
```

### Description des Attributs

| Attribut | Type | Description | Contraintes |
|----------|------|-------------|-------------|
| `id` | UUID | Identifiant unique | Généré automatiquement |
| `bookId` | UUID | Référence au livre | FK → Book.id |
| `borrowerId` | UUID | Référence à l'emprunteur | FK → Borrower.id |
| `borrowDate` | Date | Date de début d'emprunt | Date courante |
| `dueDate` | Date | Date de retour prévue | borrowDate + période |
| `returnDate` | Date \| null | Date de retour effectif | null si en cours |
| `isExtended` | boolean | A été prolongé | true/false |
| `extensionCount` | number | Nombre de prolongations | Max 2 |
| `status` | BorrowingStatus | Statut de l'emprunt | Enum |

### Règles Métier

**Calcul de la date de retour**:
```typescript
dueDate = borrowDate + {
  REFERENCE: 7 jours
  DEFAULT: 14 jours
}
```

**Prolongation**:
- Maximum 2 prolongations (`extensionCount < 2`)
- +7 jours par prolongation
- Non autorisée si en retard
- Non autorisée si réservation en attente

**États**:
```typescript
if (returnDate !== null) → RETURNED
else if (now > dueDate) → OVERDUE
else if (isExtended) → EXTENDED
else → ACTIVE
```

**Frais de retard**:
```typescript
if (status === OVERDUE) {
  lateDays = now - dueDate;
  fee = min(lateDays * 0.50€, 50€); // Plafonné à 50€
}
```

---

## Comment

Commentaire et évaluation d'un livre par un utilisateur.

### Attributs du Constructeur

```typescript
class Comment {
  id: UUID;
  bookId: UUID;
  userId: UUID;
  content: string;
  rating: number;
  createdDate: Date;
  isApproved: boolean;
}
```

### Description des Attributs

| Attribut | Type | Description | Contraintes |
|----------|------|-------------|-------------|
| `id` | UUID | Identifiant unique | Généré automatiquement |
| `bookId` | UUID | Référence au livre | FK → Book.id |
| `userId` | UUID | Auteur du commentaire | FK → User.id |
| `content` | string | Texte du commentaire | 10-500 caractères |
| `rating` | number | Note du livre | 1-5 étoiles |
| `createdDate` | Date | Date de création | Auto |
| `isApproved` | boolean | Modération | false par défaut |

### Règles Métier

**Validation du contenu**:
```typescript
MIN_COMMENT_LENGTH = 10;
MAX_COMMENT_LENGTH = 500;
MIN_RATING = 1;
MAX_RATING = 5;
```

**Workflow de modération**:
1. Utilisateur crée commentaire → `isApproved = false`
2. Bibliothécaire examine → Approuve ou rejette
3. Si approuvé → `isApproved = true` → Visible publiquement
4. Si rejeté → Notification à l'utilisateur

**Restrictions**:
- Un utilisateur peut commenter uniquement les livres qu'il a empruntés
- Maximum 10 commentaires par jour par utilisateur (anti-spam)
- Détection automatique de contenu inapproprié

**Calcul de la note moyenne d'un livre**:
```typescript
averageRating = sum(approvedComments.rating) / count(approvedComments);
```

---

## Notification

Message système envoyé à un utilisateur.

### Attributs du Constructeur

```typescript
class Notification {
  id: UUID;
  recipientId: UUID;
  senderId: UUID | null;
  type: NotificationType;
  message: string;
  createdDate: Date;
  isRead: boolean;
}
```

### Description des Attributs

| Attribut | Type | Description | Contraintes |
|----------|------|-------------|-------------|
| `id` | UUID | Identifiant unique | Généré automatiquement |
| `recipientId` | UUID | Destinataire | FK → User.id |
| `senderId` | UUID \| null | Expéditeur | null si système |
| `type` | NotificationType | Type de notification | Enum |
| `message` | string | Contenu du message | 1-1000 caractères |
| `createdDate` | Date | Date de création | Auto |
| `isRead` | boolean | Lu ou non | false par défaut |

### Règles Métier

**Notifications automatiques**:
```typescript
// Rappels de retour (J-3, J-1)
if (dueDate - now === 3 || dueDate - now === 1) {
  send(DUE_DATE, "Rappel: livre à retourner dans X jours");
}

// Retard (J+1, J+7, J+14, J+30)
if (now - dueDate === 1 || 7 || 14 || 30) {
  send(OVERDUE, "Votre livre est en retard de X jours");
}
```

**Rétention**:
- Notifications lues: Supprimées après 30 jours
- Notifications non lues: Conservées indéfiniment

**Groupement (batching)**:
```typescript
BATCH_NOTIFICATIONS = true;
BATCH_INTERVAL = 24 heures;
// Les notifications sont groupées et envoyées 1 fois/jour
```

**Canaux de notification**:
- In-app (toujours)
- Email (configurable par utilisateur)
- SMS (désactivé par défaut)

---

## 🔗 Relations entre Modèles

```
Book (1) ←→ (N) BorrowingRecord (N) ←→ (1) Borrower
Book (1) ←→ (N) Comment (N) ←→ (1) User
User (1) ←→ (N) Notification
```

### Diagramme des Relations

```
┌──────────┐
│   Book   │
│          │ 1
└────┬─────┘
     │
     │ N
     │
┌────▼──────────────┐      N  ┌──────────┐
│ BorrowingRecord   ├─────────►│ Borrower │
│                   │          │          │
└───────────────────┘          └────┬─────┘
                                    │
     ┌──────────┐                   │
     │ Comment  │◄──────────────────┘
     │          │ N              1
     └──────────┘
     
     ┌──────────────┐
     │ Notification │
     │              │
     └──────────────┘
```

---

## 📊 Statistiques des Modèles

| Modèle | Attributs | Relations | Validations |
|--------|-----------|-----------|-------------|
| Book | 15 | 1 (BorrowingRecord) | ISBN unique, titre requis |
| BorrowingRecord | 9 | 2 (Book, Borrower) | Dates cohérentes, max extensions |
| Comment | 7 | 2 (Book, User) | Longueur, rating 1-5 |
| Notification | 7 | 1 (User) | Message non vide |

**Total**: 4 modèles | 38 attributs | 6 relations

---

[← Énumérations](02-enums.md) | [Retour à l'index](README.md) | [Classe Librarian →](04-class-librarian.md)
