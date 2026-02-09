# 👤 Classe Librarian

[← Retour à l'index](README.md) | [← Modèles](03-models.md)

---

## Vue d'Ensemble

**Implémente**: `IUser`, `INotifiable`

**Responsabilité**: Représente le personnel de la bibliothèque avec des privilèges administratifs pour gérer les livres, les utilisateurs, et modérer le contenu.

**Nombre total de méthodes publiques**: 33

---

## Attributs du Constructeur

```typescript
class Librarian implements IUser, INotifiable {
  id: UUID;
  name: string;
  firstname: string;
  email: string;
  phone: string;
  hireDate: Date;
  role: LibrarianRole;
  isActiveStatus: boolean;
  lastLogin: Date;
}
```

### Description des Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `id` | UUID | Identifiant unique du bibliothécaire |
| `name` | string | Nom de famille |
| `firstname` | string | Prénom |
| `email` | string | Email professionnel |
| `phone` | string | Téléphone |
| `hireDate` | Date | Date d'embauche |
| `role` | LibrarianRole | Rôle (ADMIN, STANDARD, ASSISTANT, VOLUNTEER) |
| `isActiveStatus` | boolean | Statut actif/inactif |
| `lastLogin` | Date | Dernière connexion |

---

## Méthodes - Gestion des Livres (10 méthodes)

### addBook
```typescript
addBook(bookData: BookData): Book
```
**Événement**: *Le bibliothécaire ajoute un nouveau livre au catalogue*

Ajoute un nouveau livre au système. Vérifie l'unicité de l'ISBN.

**Paramètres**:
- `bookData`: Données du livre (titre, auteur, ISBN, etc.)

**Retour**: Instance du livre créé

**Validation**:
- ISBN unique dans le système
- Titre non vide (1-255 caractères)
- Catégorie valide

---

### deleteBookById
```typescript
deleteBookById(bookId: UUID): void
```
**Événement**: *Le bibliothécaire supprime un livre du catalogue*

Supprime définitivement un livre. Impossible si le livre a des emprunts actifs.

**Paramètres**:
- `bookId`: Identifiant du livre

**Validation**:
- Livre existe
- Aucun emprunt actif
- Confirmation requise (sécurité)

---

### updateBook
```typescript
updateBook(bookId: UUID, bookData: Partial<BookData>): Book
```
**Événement**: *Le bibliothécaire met à jour les informations d'un livre*

Met à jour les informations d'un livre existant.

**Paramètres**:
- `bookId`: Identifiant du livre
- `bookData`: Données partielles à mettre à jour

**Retour**: Livre mis à jour

---

### getBookById
```typescript
getBookById(bookId: UUID): Book
```
**Événement**: *Le bibliothécaire consulte les détails d'un livre*

Récupère les informations complètes d'un livre par son ID.

---

### getAllBooks
```typescript
getAllBooks(): Book[]
```
**Événement**: *Le bibliothécaire consulte tous les livres du catalogue*

Retourne la liste complète de tous les livres.

---

### checkBookAvailability
```typescript
checkBookAvailability(bookId: UUID): boolean
```
**Événement**: *Le bibliothécaire vérifie la disponibilité d'un livre*

Vérifie si un livre est disponible pour emprunt.

**Logique**:
```typescript
return book.isAvailable 
  && !book.isRestricted
  && book.physicalState ∉ [DAMAGED, LOST, IN_REPAIR];
```

---

### updatePhysicalState
```typescript
updatePhysicalState(bookId: UUID, state: PhysicalState): void
```
**Événement**: *Le bibliothécaire met à jour l'état physique d'un livre*

Change l'état physique d'un livre (excellent, bon, usé, endommagé, etc.).

**Impact**:
- État DAMAGED/LOST/IN_REPAIR → Livre devient non disponible

---

### setBookAvailability
```typescript
setBookAvailability(bookId: UUID, isAvailable: boolean): void
```
**Événement**: *Le bibliothécaire modifie la disponibilité d'un livre*

Modifie manuellement la disponibilité d'un livre.

**Usage**: Mise en réserve temporaire, inventaire, etc.

---

### restrictBook
```typescript
restrictBook(bookId: UUID, reason: string): void
```
**Événement**: *Le bibliothécaire restreint l'accès à un livre*

Marque un livre comme restreint (nécessite autorisation spéciale).

**Paramètres**:
- `bookId`: Identifiant du livre
- `reason`: Raison de la restriction (archivage, log)

**Usage**: Livres rares, contenu sensible, etc.

---

### unrestrictBook
```typescript
unrestrictBook(bookId: UUID): void
```
**Événement**: *Le bibliothécaire lève la restriction d'un livre*

Retire la restriction d'un livre.

---

## Méthodes - Gestion des Utilisateurs (9 méthodes)

### addUser
```typescript
addUser(userData: UserData): Borrower
```
**Événement**: *Le bibliothécaire enregistre un nouveau compte utilisateur*

Crée un nouveau compte emprunteur.

**Validation**:
- Email unique
- Âge minimum (13 ans par défaut)
- Données complètes (nom, prénom, adresse)

---

### getUserById
```typescript
getUserById(userId: UUID): Borrower
```
**Événement**: *Le bibliothécaire consulte les informations d'un utilisateur*

Récupère le profil complet d'un utilisateur.

---

### getAllUsers
```typescript
getAllUsers(): Borrower[]
```
**Événement**: *Le bibliothécaire consulte la liste de tous les utilisateurs*

Retourne tous les utilisateurs du système.

---

### deleteUser
```typescript
deleteUser(userId: UUID): void
```
**Événement**: *Le bibliothécaire supprime définitivement un compte utilisateur*

Suppression définitive d'un compte. Impossible si emprunts actifs.

**Validation**:
- Aucun emprunt actif
- Aucune dette en cours
- Confirmation requise

---

### activateUser / deactivateUser
```typescript
activateUser(userId: UUID): void
deactivateUser(userId: UUID, reason: string): void
```
**Événements**: 
- *Le bibliothécaire active un compte utilisateur*
- *Le bibliothécaire désactive un compte utilisateur*

Active ou désactive un compte utilisateur.

---

### suspendUser
```typescript
suspendUser(userId: UUID, durationDays: number, reason: string): void
```
**Événement**: *Le bibliothécaire suspend temporairement un utilisateur*

Suspend un compte pour une durée déterminée.

**Paramètres**:
- `userId`: Identifiant de l'utilisateur
- `durationDays`: Durée de suspension en jours
- `reason`: Raison (retards répétés, dommages, etc.)

**Effet**:
- Utilisateur ne peut plus emprunter
- Emprunts en cours restent valides
- Notification envoyée automatiquement

---

### unsuspendUser
```typescript
unsuspendUser(userId: UUID): void
```
**Événement**: *Le bibliothécaire lève la suspension d'un utilisateur*

Réactive un compte suspendu avant la fin de la période.

---

### authorizeUser / revokeUserAuthorization
```typescript
authorizeUser(userId: UUID): void
revokeUserAuthorization(userId: UUID): void
```
**Événements**:
- *Le bibliothécaire autorise un utilisateur à emprunter*
- *Le bibliothécaire révoque l'autorisation d'emprunt*

Gère les autorisations spéciales d'emprunt.

---

## Méthodes - Communication (6 méthodes)

### sendEmailToUser
```typescript
sendEmailToUser(userId: UUID, subject: string, body: string): void
```
**Événement**: *Le bibliothécaire envoie un email à un utilisateur*

Envoie un email personnalisé à un utilisateur spécifique.

---

### sendEmailToAdmin
```typescript
sendEmailToAdmin(subject: string, body: string): void
```
**Événement**: *Le bibliothécaire envoie un email à l'administrateur système*

Communication interne vers l'administration.

---

### postGeneralInfo
```typescript
postGeneralInfo(message: string): void
```
**Événement**: *Le bibliothécaire publie une information générale*

Publie une annonce/actualité visible par tous les utilisateurs.

**Usage**: Fermeture exceptionnelle, nouveautés, événements

---

### sendNotification (INotifiable)
```typescript
sendNotification(recipientId: UUID, message: string, type: NotificationType): void
```
Envoie une notification in-app à un utilisateur.

---

### receiveNotification (INotifiable)
```typescript
receiveNotification(): Notification[]
```
Récupère les notifications du bibliothécaire.

---

### markNotificationAsRead (INotifiable)
```typescript
markNotificationAsRead(notificationId: UUID): void
```
Marque une notification comme lue.

---

## Méthodes - Gestion du Profil (4 méthodes IUser)

### getProfile
```typescript
getProfile(): UserProfile
```
Récupère le profil complet du bibliothécaire.

---

### updateProfile
```typescript
updateProfile(profileData: Partial<UserProfile>): void
```
Met à jour les informations personnelles.

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

## Méthodes - Modération des Commentaires (3 méthodes)

### approveComment
```typescript
approveComment(commentId: UUID): void
```
**Événement**: *Le bibliothécaire approuve un commentaire*

Approuve un commentaire pour publication publique.

**Effet**:
- `comment.isApproved = true`
- Commentaire visible publiquement
- Notification à l'auteur

---

### rejectComment
```typescript
rejectComment(commentId: UUID, reason: string): void
```
**Événement**: *Le bibliothécaire rejette un commentaire*

Rejette un commentaire (contenu inapproprié, spam, etc.).

**Effet**:
- Commentaire supprimé ou caché
- Notification à l'auteur avec raison

---

### getPendingComments
```typescript
getPendingComments(): Comment[]
```
**Événement**: *Le bibliothécaire consulte les commentaires en attente de modération*

Récupère tous les commentaires non modérés.

**Filtre**: `comment.isApproved === false`

---

## 📊 Récapitulatif des Méthodes

| Catégorie | Nombre | Méthodes |
|-----------|--------|----------|
| **Gestion Livres** | 10 | add, delete, update, get, getAll, checkAvailability, updatePhysicalState, setAvailability, restrict, unrestrict |
| **Gestion Users** | 9 | add, get, getAll, delete, activate, deactivate, suspend, unsuspend, authorize, revokeAuth |
| **Communication** | 6 | sendEmailToUser, sendEmailToAdmin, postGeneralInfo, sendNotification, receiveNotification, markAsRead |
| **Profil** | 4 | getProfile, updateProfile, isActive, getId |
| **Modération** | 3 | approveComment, rejectComment, getPendingComments |
| **TOTAL** | **33** | |

---

[← Modèles](03-models.md) | [Retour à l'index](README.md) | [Classe Borrower →](05-class-borrower.md)
