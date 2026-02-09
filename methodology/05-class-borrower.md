# 📖 Classe Borrower

[← Retour à l'index](README.md) | [← Librarian](04-class-librarian.md)

---

## Vue d'Ensemble

**Implémente**: `IUser`, `INotifiable`, `ISearchable`

**Responsabilité**: Représente un utilisateur emprunteur de la bibliothèque avec capacités de recherche, emprunt, commentaires et gestion de profil.

**Nombre total de méthodes publiques**: 27

---

## Attributs du Constructeur

```typescript
class Borrower implements IUser, INotifiable, ISearchable {
  id: UUID;
  name: string;
  firstname: string;
  email: string;
  phone: string;
  address: string;
  registrationDate: Date;
  isAuthorized: boolean;
  isActiveStatus: boolean;
  suspensionEndDate: Date | null;
  borrowedBooks: UUID[];
  borrowingHistory: BorrowingRecord[];
  maxBooksAllowed: number;
  notificationsEnabled: boolean;
  lastLogin: Date;
}
```

### Description des Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `id` | UUID | Identifiant unique |
| `name` | string | Nom de famille |
| `firstname` | string | Prénom |
| `email` | string | Email de contact |
| `phone` | string | Téléphone |
| `address` | string | Adresse postale |
| `registrationDate` | Date | Date d'inscription |
| `isAuthorized` | boolean | Autorisé à emprunter |
| `isActiveStatus` | boolean | Compte actif |
| `suspensionEndDate` | Date \| null | Date de fin de suspension (si suspendu) |
| `borrowedBooks` | UUID[] | IDs des livres actuellement empruntés |
| `borrowingHistory` | BorrowingRecord[] | Historique complet des emprunts |
| `maxBooksAllowed` | number | Limite d'emprunts simultanés (défaut: 5) |
| `notificationsEnabled` | boolean | Préférence de notifications |
| `lastLogin` | Date | Dernière connexion |

---

## Méthodes - Opérations sur les Livres (7 méthodes)

### borrowBook
```typescript
borrowBook(bookId: UUID): BorrowingRecord
```
**Événement**: *L'emprunteur emprunte un livre*

Emprunte un livre si toutes les conditions sont remplies.

**Validation** (méthode privée `canBorrow`):
```typescript
private canBorrow(): boolean {
  return this.isActiveStatus
    && this.isAuthorized
    && this.suspensionEndDate === null
    && this.borrowedBooks.length < BORROWING_POLICIES.MAX_BOOKS_PER_USER;
}
```

**Conditions**:
- ✅ Compte actif
- ✅ Autorisé à emprunter
- ✅ Non suspendu
- ✅ Limite de livres non atteinte (< 5)
- ✅ Livre disponible

**Retour**: Enregistrement d'emprunt créé

**Erreurs**:
- `"Account suspended"` - Compte suspendu
- `"Not authorized to borrow"` - Non autorisé
- `"Maximum books limit reached"` - Limite atteinte
- `"Book not available"` - Livre non disponible

---

### returnBook
```typescript
returnBook(borrowingRecordId: UUID): void
```
**Événement**: *L'emprunteur retourne un livre*

Traite le retour d'un livre emprunté.

**Effet**:
- Met à jour `returnDate` dans BorrowingRecord
- Change le statut à `RETURNED`
- Libère le livre (`isAvailable = true`)
- Calcule les frais de retard si applicable

---

### extendBorrowingPeriod
```typescript
extendBorrowingPeriod(recordId: UUID, days: number): boolean
```
**Événement**: *L'emprunteur demande une prolongation d'emprunt*

Demande une prolongation de la période d'emprunt.

**Paramètres**:
- `recordId`: ID de l'enregistrement d'emprunt
- `days`: Nombre de jours de prolongation demandés

**Validation**:
- Maximum 2 prolongations (`extensionCount < 2`)
- Pas de retard en cours
- Pas de réservation en attente sur le livre
- Durée max: 7 jours par prolongation

**Retour**: `true` si approuvé, `false` si refusé

---

### getMyBorrowedBooks
```typescript
getMyBorrowedBooks(): Book[]
```
**Événement**: *L'emprunteur consulte ses livres actuellement empruntés*

Retourne la liste des livres actuellement empruntés.

**Filtre**: `borrowingRecords.filter(r => r.status === ACTIVE)`

---

### getMyBorrowingHistory
```typescript
getMyBorrowingHistory(): BorrowingRecord[]
```
**Événement**: *L'emprunteur consulte son historique d'emprunts complet*

Retourne l'historique complet de tous les emprunts (passés et présents).

---

### getBookByTitle / getBookById
```typescript
getBookByTitle(title: string): Book[]
getBookById(bookId: UUID): Book
```
**Événements**: 
- *L'emprunteur consulte un livre par titre*
- *L'emprunteur consulte les détails d'un livre*

Récupère des informations sur les livres.

---

## Méthodes - Recherche (ISearchable - 5 méthodes)

### searchByTitle
```typescript
searchByTitle(title: string): Book[]
```
**Événement**: *L'utilisateur recherche un livre par titre*

Recherche de livres par titre (correspondance partielle, insensible à la casse).

**Exemple**:
```typescript
searchByTitle("Harry") → ["Harry Potter...", "Dirty Harry", ...]
```

---

### searchByAuthor
```typescript
searchByAuthor(author: string): Book[]
```
**Événement**: *L'utilisateur recherche un livre par auteur*

Recherche par nom d'auteur (partiel).

---

### searchByISBN
```typescript
searchByISBN(isbn: string): Book | null
```
**Événement**: *L'utilisateur recherche un livre par ISBN*

Recherche exacte par numéro ISBN (unique).

**Retour**: Un seul livre ou `null` si non trouvé

---

### searchAvailableBooks
```typescript
searchAvailableBooks(): Book[]
```
**Événement**: *L'utilisateur consulte uniquement les livres disponibles*

Retourne tous les livres disponibles pour emprunt immédiat.

**Filtre**:
```typescript
books.filter(b => b.isAvailable 
  && !b.isRestricted
  && b.physicalState ∉ [DAMAGED, LOST, IN_REPAIR])
```

---

### filterBooks
```typescript
filterBooks(criteria: SearchCriteria): Book[]
```
**Événement**: *L'utilisateur filtre les livres par catégorie/année/note*

Recherche multi-critères avancée.

**SearchCriteria**:
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

**Exemple**:
```typescript
filterBooks({
  category: BookCategory.SCIENCE,
  minRating: 4.0,
  availability: true
})
```

---

## Méthodes - Commentaires et Avis (4 méthodes)

### addComment
```typescript
addComment(bookId: UUID, content: string, rating: number): Comment
```
**Événement**: *L'emprunteur ajoute un commentaire sur un livre*

Publie un commentaire et une note sur un livre.

**Validation**:
- Contenu: 10-500 caractères
- Rating: 1-5 étoiles
- Utilisateur a emprunté le livre (recommandé)

**Effet**:
- Commentaire créé avec `isApproved = false`
- En attente de modération par bibliothécaire

---

### editComment
```typescript
editComment(commentId: UUID, content: string): void
```
**Événement**: *L'emprunteur modifie son commentaire*

Modifie un commentaire existant.

**Validation**:
- Commentaire appartient à l'utilisateur
- Nouvelles contraintes de longueur respectées

**Effet**:
- Si déjà approuvé → Repasse en modération

---

### deleteComment
```typescript
deleteComment(commentId: UUID): void
```
**Événement**: *L'emprunteur supprime son commentaire*

Supprime un de ses commentaires.

**Validation**: Seul l'auteur peut supprimer son commentaire

---

### getMyComments
```typescript
getMyComments(): Comment[]
```
**Événement**: *L'emprunteur consulte ses propres commentaires*

Retourne tous les commentaires publiés par l'utilisateur.

---

## Méthodes - Notifications (INotifiable - 5 méthodes)

### subscribeToBookAvailability
```typescript
subscribeToBookAvailability(bookId: UUID): void
```
**Événement**: *L'emprunteur s'abonne aux notifications de disponibilité d'un livre*

S'abonne pour recevoir une notification quand un livre devient disponible.

**Usage**: Livre actuellement emprunté, utilisateur veut être notifié du retour

---

### unsubscribeFromBookAvailability
```typescript
unsubscribeFromBookAvailability(bookId: UUID): void
```
**Événement**: *L'emprunteur se désabonne des notifications de disponibilité*

Retire l'abonnement aux notifications pour un livre.

---

### sendNotification
```typescript
sendNotification(recipientId: UUID, message: string, type: NotificationType): void
```
Envoie une notification (hérité de INotifiable).

---

### receiveNotification
```typescript
receiveNotification(): Notification[]
```
**Événement**: *L'utilisateur reçoit une notification*

Récupère toutes les notifications de l'utilisateur.

**Types de notifications reçues**:
- Rappel de date de retour (J-3, J-1)
- Notification de retard
- Prolongation approuvée/refusée
- Disponibilité de livre abonné
- Commentaire approuvé/rejeté
- Information générale de la bibliothèque

---

### markNotificationAsRead
```typescript
markNotificationAsRead(notificationId: UUID): void
```
**Événement**: *L'utilisateur marque une notification comme lue*

Marque une notification comme lue.

**Effet**: `notification.isRead = true`, `readAt = now()`

---

## Méthodes - Gestion de Profil (IUser - 4 méthodes)

### getProfile
```typescript
getProfile(): UserProfile
```
**Événement**: *L'utilisateur consulte son profil*

Récupère le profil complet de l'utilisateur.

**Retour**:
```typescript
{
  id, name, firstname, email, phone, address,
  registrationDate, isActive, isAuthorized,
  borrowedBooksCount, lastLogin
}
```

---

### updateProfile
```typescript
updateProfile(profileData: Partial<UserProfile>): void
```
**Événement**: *L'emprunteur modifie ses informations personnelles*

Met à jour les informations du profil.

**Champs modifiables**:
- name, firstname, email, phone, address
- notificationsEnabled

**Champs protégés** (non modifiables par l'utilisateur):
- id, registrationDate, isAuthorized, suspensionEndDate

---

### isActive
```typescript
isActive(): boolean
```
Vérifie si le compte est actif.

---

### getId
```typescript
getId(): UUID
```
Retourne l'identifiant unique.

---

## Méthodes - Réclamations (2 méthodes)

### sendClaim
```typescript
sendClaim(subject: string, description: string): void
```
**Événement**: *L'emprunteur soumet une réclamation*

Soumet une réclamation au service client.

**Types de réclamations**:
- Livre endommagé au moment de l'emprunt
- Livre perdu
- Frais incorrects
- Problème de compte
- Plainte sur le service
- Problème technique

**Validation**:
- Description: 20-1000 caractères
- Maximum 5 réclamations ouvertes simultanément

---

### getMyClaims
```typescript
getMyClaims(): Claim[]
```
**Événement**: *L'emprunteur consulte ses réclamations*

Récupère toutes les réclamations de l'utilisateur.

---

## 📊 Récapitulatif des Méthodes

| Catégorie | Nombre | Méthodes |
|-----------|--------|----------|
| **Opérations Livres** | 7 | borrow, return, extend, getMyBorrowed, getMyHistory, getByTitle, getById |
| **Recherche** | 5 | searchByTitle, searchByAuthor, searchByISBN, searchAvailable, filterBooks |
| **Commentaires** | 4 | add, edit, delete, getMy |
| **Notifications** | 5 | subscribe, unsubscribe, send, receive, markAsRead |
| **Profil** | 4 | get, update, isActive, getId |
| **Réclamations** | 2 | send, getMy |
| **TOTAL** | **27** | |

---

## 🔒 Méthodes Privées

### canBorrow (private)
```typescript
private canBorrow(): boolean {
  return this.isActiveStatus
    && this.isAuthorized
    && this.suspensionEndDate === null
    && this.borrowedBooks.length < BORROWING_POLICIES.MAX_BOOKS_PER_USER;
}
```

Validation interne pour vérifier si l'utilisateur peut emprunter.

---

[← Librarian](04-class-librarian.md) | [Retour à l'index](README.md) | [Classe Library →](06-class-library.md)
