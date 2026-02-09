# 1. Lister les classes avec leurs attributs et leurs méthodes

## Interfaces

### Interface INotifiable
**Methods**
* send_Notification(recipient_Id: UUID, message: string, type: NotificationType): void
* send_Email(recipient_Email: string, subject: string, body: string): void
* receive_Notification(): Notification[]
* mark_Notification_As_Read(notification_Id: UUID): void

### Interface IBorrowable
**Methods**
* can_Be_Borrowed(): boolean
* borrow(borrower_Id: UUID): BorrowingRecord
* return(borrower_Id: UUID): void
* extend_Borrowing_Period(days: number): boolean
* get_Borrowing_History(): BorrowingRecord[]

### Interface IUser
**Methods**
* get_Profile(): UserProfile
* update_Profile(profile_Data: Partial<UserProfile>): void
* is_Active(): boolean
* get_Id(): UUID

### Interface ISearchable
**Methods**
* search_By_Title(title: string): Book[]
* search_By_Author(author: string): Book[]
* search_By_ISBN(isbn: string): Book | null
* search_Available_Books(): Book[]
* filter_Books(criteria: SearchCriteria): Book[]

## Enums

### Enum BookCategory
Catégories de livres pour la classification
```typescript
enum BookCategory {
  FICTION = "fiction",
  NON_FICTION = "non_fiction",
  SCIENCE = "science",
  TECHNOLOGY = "technology",
  HISTORY = "history",
  BIOGRAPHY = "biography",
  PHILOSOPHY = "philosophy",
  RELIGION = "religion",
  POETRY = "poetry",
  DRAMA = "drama",
  CHILDREN = "children",
  YOUNG_ADULT = "young_adult",
  REFERENCE = "reference",
  EDUCATION = "education",
  ART = "art",
  MUSIC = "music",
  TRAVEL = "travel",
  COOKING = "cooking",
  HEALTH = "health",
  SELF_HELP = "self_help",
  BUSINESS = "business",
  ECONOMICS = "economics",
  LAW = "law",
  POLITICS = "politics",
  OTHER = "other"
}
```

### Enum PhysicalState
État physique du livre pour le suivi de l'usure
```typescript
enum PhysicalState {
  EXCELLENT = "excellent",      // Comme neuf, aucune marque d'usure
  GOOD = "good",                 // Bon état général, légères traces d'utilisation
  FAIR = "fair",                 // État correct, signes d'usure visibles
  POOR = "poor",                 // Mauvais état, nécessite réparation
  DAMAGED = "damaged",           // Endommagé, non empruntable
  LOST = "lost",                 // Perdu par un emprunteur
  IN_REPAIR = "in_repair"        // En cours de réparation
}
```

### Enum BorrowingStatus
Statut d'un emprunt dans le système
```typescript
enum BorrowingStatus {
  ACTIVE = "active",             // Emprunt en cours
  RETURNED = "returned",         // Livre retourné
  OVERDUE = "overdue",           // En retard
  EXTENDED = "extended",         // Prolongé
  CANCELLED = "cancelled",       // Annulé avant retrait
  RESERVED = "reserved"          // Réservé mais pas encore emprunté
}
```

### Enum NotificationType
Types de notifications envoyées aux utilisateurs
```typescript
enum NotificationType {
  DUE_DATE = "due_date",                     // Rappel de date de retour
  OVERDUE = "overdue",                       // Notification de retard
  EXTENSION_APPROVED = "extension_approved", // Prolongation approuvée
  EXTENSION_DENIED = "extension_denied",     // Prolongation refusée
  AVAILABILITY = "availability",             // Livre disponible (abonnement)
  RESERVATION_READY = "reservation_ready",   // Réservation prête à retirer
  ACCOUNT_SUSPENDED = "account_suspended",   // Compte suspendu
  ACCOUNT_ACTIVATED = "account_activated",   // Compte activé
  GENERAL = "general",                       // Information générale
  COMMENT_APPROVED = "comment_approved",     // Commentaire approuvé
  COMMENT_REJECTED = "comment_rejected",     // Commentaire rejeté
  NEW_BOOK_ADDED = "new_book_added",        // Nouveau livre ajouté
  CLAIM_RECEIVED = "claim_received",         // Réclamation reçue
  CLAIM_RESOLVED = "claim_resolved"          // Réclamation résolue
}
```

### Enum LibrarianRole
Rôles et permissions des bibliothécaires
```typescript
enum LibrarianRole {
  ADMIN = "admin",               // Administrateur (tous les droits)
  STANDARD = "standard",         // Bibliothécaire standard
  ASSISTANT = "assistant",       // Assistant (droits limités)
  VOLUNTEER = "volunteer"        // Bénévole (lecture seule + certaines actions)
}
```

### Enum UserStatus
Statut d'un compte utilisateur
```typescript
enum UserStatus {
  ACTIVE = "active",             // Compte actif
  INACTIVE = "inactive",         // Compte inactif (pas de connexion récente)
  SUSPENDED = "suspended",       // Suspendu temporairement
  DEACTIVATED = "deactivated",   // Désactivé par admin
  PENDING = "pending",           // En attente d'approbation
  BANNED = "banned"              // Banni définitivement
}
```

### Enum ClaimStatus
Statut d'une réclamation utilisateur
```typescript
enum ClaimStatus {
  PENDING = "pending",           // En attente de traitement
  IN_PROGRESS = "in_progress",   // En cours de traitement
  RESOLVED = "resolved",         // Résolue
  REJECTED = "rejected",         // Rejetée
  CLOSED = "closed"              // Fermée
}
```

### Enum ClaimPriority
Niveau de priorité d'une réclamation
```typescript
enum ClaimPriority {
  LOW = "low",                   // Basse priorité
  MEDIUM = "medium",             // Priorité moyenne
  HIGH = "high",                 // Haute priorité
  URGENT = "urgent"              // Urgente
}
```

### Enum ClaimType
Types de réclamations possibles
```typescript
enum ClaimType {
  DAMAGED_BOOK = "damaged_book",         // Livre endommagé
  LOST_BOOK = "lost_book",               // Livre perdu
  INCORRECT_CHARGE = "incorrect_charge", // Frais incorrects
  ACCOUNT_ISSUE = "account_issue",       // Problème de compte
  SERVICE_COMPLAINT = "service_complaint", // Plainte service
  TECHNICAL_ISSUE = "technical_issue",   // Problème technique
  OTHER = "other"                        // Autre
}
```

### Enum ExtensionStatus
Statut d'une demande de prolongation
```typescript
enum ExtensionStatus {
  PENDING = "pending",           // En attente
  APPROVED = "approved",         // Approuvée
  DENIED = "denied",             // Refusée
  EXPIRED = "expired"            // Expirée
}
```

### Enum SearchFilter
Filtres de recherche disponibles
```typescript
enum SearchFilter {
  TITLE = "title",
  AUTHOR = "author",
  ISBN = "isbn",
  CATEGORY = "category",
  YEAR = "year",
  PUBLISHER = "publisher",
  AVAILABILITY = "availability",
  RATING = "rating"
}
```

## Models

### Model Book
**Constructor's attributes**
* id: UUID
* title: string
* author: string
* ISBN: string
* publisher: string
* publication_Year: number
* category: BookCategory (enum)
* is_Available: boolean 
* physical_State: PhysicalState (enum: Excellent, Good, Fair, Poor)
* borrowing_History: BorrowingRecord[]
* is_Restricted: boolean
* added_Date: datetime
* last_Modified: datetime
* description: string
* cover_Image_Url: string

### Model BorrowingRecord
**Constructor's attributes**
* id: UUID
* book_Id: UUID
* borrower_Id: UUID
* borrow_Date: datetime
* due_Date: datetime
* return_Date: datetime | null
* is_Extended: boolean
* extension_Count: number
* status: BorrowingStatus (enum: Active, Returned, Overdue, Extended)

### Model Comment
**Constructor's attributes**
* id: UUID
* book_Id: UUID
* user_Id: UUID
* content: string
* rating: number (1-5)
* created_Date: datetime
* is_Approved: boolean

### Model Notification
**Constructor's attributes**
* id: UUID
* recipient_Id: UUID
* sender_Id: UUID | null
* type: NotificationType (enum: DueDate, Extension, Availability, General)
* message: string
* created_Date: datetime
* is_Read: boolean

## Classes

### Class Librarian implements IUser, INotifiable
**Constructor's attributes**
* id: UUID
* name: string
* firstname: string
* email: string
* phone: string
* hire_Date: datetime
* role: LibrarianRole (enum: Admin, Standard)
* is_Active: boolean
* last_Login: datetime

**Methods - Book Management** 
* add_Book(book_Data: BookData): Book
* delete_Book_By_Id(book_Id: UUID): void
* update_Book(book_Id: UUID, book_Data: Partial<BookData>): Book
* get_Book_By_Id(book_Id: UUID): Book
* get_All_Books(): Book[]
* check_Book_Availability(book_Id: UUID): boolean
* update_Physical_State(book_Id: UUID, state: PhysicalState): void
* set_Book_Availability(book_Id: UUID, is_Available: boolean): void
* restrict_Book(book_Id: UUID, reason: string): void
* unrestrict_Book(book_Id: UUID): void

**Methods - User Management**
* add_User(user_Data: UserData): Borrower
* get_User_By_Id(user_Id: UUID): Borrower
* get_All_Users(): Borrower[]
* delete_User(user_Id: UUID): void
* activate_User(user_Id: UUID): void
* deactivate_User(user_Id: UUID, reason: string): void
* suspend_User(user_Id: UUID, duration_Days: number, reason: string): void
* authorize_User(user_Id: UUID): void
* revoke_User_Authorization(user_Id: UUID): void

**Methods - Notification & Communication**
* send_Email_To_User(user_Id: UUID, subject: string, body: string): void
* send_Email_To_Admin(subject: string, body: string): void
* post_General_Info(message: string): void
* send_Notification(recipient_Id: UUID, message: string, type: NotificationType): void
* receive_Notification(): Notification[]
* mark_Notification_As_Read(notification_Id: UUID): void

**Methods - Profile**
* get_Profile(): UserProfile
* update_Profile(profile_Data: Partial<UserProfile>): void
* is_Active(): boolean
* get_Id(): UUID

**Methods - Comments Management**
* approve_Comment(comment_Id: UUID): void
* reject_Comment(comment_Id: UUID): void
* get_Pending_Comments(): Comment[]

### Class Borrower implements IUser, INotifiable, ISearchable
**Constructor's attributes**
* id: UUID
* name: string
* firstname: string
* email: string
* phone: string
* address: string
* registration_Date: datetime
* is_Authorized: boolean
* is_Active: boolean
* suspension_End_Date: datetime | null
* borrowed_Books: UUID[]
* borrowing_History: BorrowingRecord[]
* max_Books_Allowed: number
* notifications_Enabled: boolean
* last_Login: datetime

**Methods - Book Operations**
* get_Book_By_Title(title: string): Book[]
* get_Book_By_Id(book_Id: UUID): Book
* borrow_Book(book_Id: UUID): BorrowingRecord
* return_Book(book_Id: UUID): void
* extend_Borrowing_Period(book_Id: UUID, days: number): boolean
* get_My_Borrowed_Books(): Book[]
* get_My_Borrowing_History(): BorrowingRecord[]

**Methods - Search Implementation (ISearchable)**
* search_By_Title(title: string): Book[]
* search_By_Author(author: string): Book[]
* search_By_ISBN(isbn: string): Book | null
* search_Available_Books(): Book[]
* filter_Books(criteria: SearchCriteria): Book[]

**Methods - Comments & Reviews**
* add_Comment(book_Id: UUID, content: string, rating: number): Comment
* edit_Comment(comment_Id: UUID, content: string): void
* delete_Comment(comment_Id: UUID): void
* get_My_Comments(): Comment[]

**Methods - Notifications**
* subscribe_To_Book_Availability(book_Id: UUID): void
* unsubscribe_From_Book_Availability(book_Id: UUID): void
* send_Notification(recipient_Id: UUID, message: string, type: NotificationType): void
* receive_Notification(): Notification[]
* mark_Notification_As_Read(notification_Id: UUID): void

**Methods - Profile**
* get_Profile(): UserProfile
* update_Profile(profile_Data: Partial<UserProfile>): void
* is_Active(): boolean
* get_Id(): UUID

**Methods - Claims**
* send_Claim(subject: string, description: string): void
* get_My_Claims(): Claim[]

### Class Library (Système central)
**Constructor's attributes**
* id: UUID
* name: string
* address: string
* phone: string
* email: string
* opening_Hours: OpeningHours
* books: Map<UUID, Book>
* users: Map<UUID, Borrower>
* librarians: Map<UUID, Librarian>
* borrowing_Records: Map<UUID, BorrowingRecord>
* notifications: Map<UUID, Notification>

**Methods - Book Management**
* add_Book(book: Book): void
* remove_Book(book_Id: UUID): void
* get_Book(book_Id: UUID): Book
* get_All_Books(): Book[]
* get_Available_Books(): Book[]

**Methods - User Management**
* register_User(user_Data: UserData): Borrower
* get_User(user_Id: UUID): Borrower
* get_All_Users(): Borrower[]

**Methods - Borrowing Management**
* process_Borrowing(book_Id: UUID, borrower_Id: UUID): BorrowingRecord
* process_Return(book_Id: UUID, borrower_Id: UUID): void
* get_Overdue_Borrowings(): BorrowingRecord[]
* send_Due_Date_Reminders(): void


## Liste complète des événements possibles dans le système

Cette liste permet de déterminer les attributs et les méthodes des classes ainsi que les interfaces et la visibilité (public/private) de chaque méthode.

### 🔐 ÉVÉNEMENTS D'AUTHENTIFICATION

* le LIBRARIAN se connecte au système
* le LIBRARIAN se déconnecte du système
* le USER se connecte au système
* le USER se déconnecte du système
* le SYSTEM enregistre la dernière connexion d'un utilisateur
* le SYSTEM vérifie les credentials d'un utilisateur
* le SYSTEM génère un token de session
* le SYSTEM révoque un token de session

### 👥 ÉVÉNEMENTS DE GESTION DES UTILISATEURS (LIBRARIAN)

* le LIBRARIAN enregistre un nouveau compte utilisateur
* le LIBRARIAN active un compte utilisateur
* le LIBRARIAN désactive un compte utilisateur pour non-respect du règlement
* le LIBRARIAN suspend temporairement un compte utilisateur
* le LIBRARIAN lève la suspension d'un compte utilisateur
* le LIBRARIAN autorise un utilisateur à emprunter des livres
* le LIBRARIAN révoque l'autorisation d'emprunt d'un utilisateur
* le LIBRARIAN supprime définitivement un compte utilisateur
* le LIBRARIAN consulte les informations d'un utilisateur
* le LIBRARIAN consulte la liste de tous les utilisateurs
* le LIBRARIAN filtre les utilisateurs par statut (actif, suspendu, etc.)
* le LIBRARIAN consulte l'historique d'emprunts d'un utilisateur
* le LIBRARIAN modifie les droits d'un utilisateur (nombre max de livres)
* le LIBRARIAN bannit définitivement un utilisateur

### 📚 ÉVÉNEMENTS DE GESTION DES LIVRES (LIBRARIAN)

* le LIBRARIAN ajoute un nouveau livre au catalogue
* le LIBRARIAN supprime un livre du catalogue
* le LIBRARIAN modifie les informations d'un livre (titre, auteur, description)
* le LIBRARIAN modifie l'état physique d'un livre (excellent, bon, usé, endommagé)
* le LIBRARIAN consulte les détails d'un livre par son ID
* le LIBRARIAN consulte tous les livres du catalogue
* le LIBRARIAN vérifie la disponibilité d'un ou plusieurs livres
* le LIBRARIAN modifie manuellement la disponibilité d'un livre
* le LIBRARIAN restreint un livre (non empruntable temporairement)
* le LIBRARIAN lève la restriction d'un livre
* le LIBRARIAN marque un livre comme perdu
* le LIBRARIAN marque un livre comme en réparation
* le LIBRARIAN consulte l'historique des emprunts d'un livre
* le LIBRARIAN filtre les livres par catégorie
* le LIBRARIAN filtre les livres par état physique
* le LIBRARIAN consulte les statistiques d'emprunts d'un livre

### 📖 ÉVÉNEMENTS D'EMPRUNTS (LIBRARIAN & SYSTEM)

* le SYSTEM traite une demande d'emprunt
* le SYSTEM valide les conditions d'emprunt (max livres, compte actif)
* le SYSTEM crée un enregistrement d'emprunt
* le SYSTEM calcule la date de retour
* le SYSTEM traite un retour de livre
* le SYSTEM vérifie l'état du livre au retour
* le SYSTEM clôture un enregistrement d'emprunt
* le SYSTEM détecte les emprunts en retard automatiquement
* le SYSTEM consulte tous les emprunts en retard
* le LIBRARIAN prolonge manuellement un emprunt
* le LIBRARIAN annule un emprunt

### 📧 ÉVÉNEMENTS DE COMMUNICATION (LIBRARIAN)

* le LIBRARIAN envoie un email à un utilisateur spécifique
* le LIBRARIAN envoie un email groupé à plusieurs utilisateurs
* le LIBRARIAN envoie un email à l'administrateur système
* le LIBRARIAN publie une information générale (actualité de la bibliothèque)
* le LIBRARIAN envoie une notification à un utilisateur
* le LIBRARIAN consulte ses notifications reçues
* le LIBRARIAN marque une notification comme lue

### 🔔 ÉVÉNEMENTS DE NOTIFICATIONS (SYSTEM → LIBRARIAN)

* le SYSTEM notifie le LIBRARIAN de la fin imminente d'un emprunt
* le SYSTEM notifie le LIBRARIAN d'une demande de prolongation
* le SYSTEM notifie le LIBRARIAN d'un retard d'emprunt
* le SYSTEM notifie le LIBRARIAN de la publication d'un nouveau commentaire
* le SYSTEM notifie le LIBRARIAN d'une nouvelle réclamation
* le SYSTEM notifie le LIBRARIAN d'un livre retourné endommagé

### 💬 ÉVÉNEMENTS DE GESTION DES COMMENTAIRES (LIBRARIAN)

* le LIBRARIAN consulte les commentaires en attente de modération
* le LIBRARIAN approuve un commentaire
* le LIBRARIAN rejette un commentaire
* le LIBRARIAN supprime un commentaire inapproprié
* le LIBRARIAN consulte tous les commentaires d'un livre

### 📖 ÉVÉNEMENTS DE CONSULTATION DES LIVRES (USER)

* le USER consulte tous les livres du catalogue
* le USER consulte uniquement les livres disponibles
* le USER recherche un livre par titre
* le USER recherche un livre par auteur
* le USER recherche un livre par ISBN
* le USER filtre les livres par catégorie
* le USER filtre les livres par année de publication
* le USER filtre les livres par note moyenne
* le USER consulte les détails complets d'un livre
* le USER consulte les commentaires d'un livre
* le USER consulte la disponibilité d'un livre spécifique

### 📚 ÉVÉNEMENTS D'EMPRUNT (USER)

* le USER emprunte un livre
* le USER consulte ses livres actuellement empruntés
* le USER consulte son historique d'emprunts complet
* le USER demande une prolongation d'emprunt
* le USER retourne un livre
* le USER vérifie combien de livres il peut encore emprunter

### 🔔 ÉVÉNEMENTS DE NOTIFICATIONS (USER)

* le USER s'abonne aux notifications de disponibilité d'un livre
* le USER se désabonne des notifications de disponibilité d'un livre
* le USER reçoit une notification de date de retour imminente
* le USER reçoit une notification de retard
* le USER reçoit une notification de prolongation approuvée
* le USER reçoit une notification de prolongation refusée
* le USER reçoit une notification de disponibilité d'un livre souhaité
* le USER reçoit une notification de suspension de compte
* le USER reçoit une notification d'activation de compte
* le USER consulte toutes ses notifications
* le USER marque une notification comme lue
* le USER active/désactive les notifications

### 💬 ÉVÉNEMENTS DE COMMENTAIRES & AVIS (USER)

* le USER ajoute un commentaire sur un livre
* le USER ajoute une note (1-5 étoiles) à un livre
* le USER modifie son commentaire
* le USER supprime son commentaire
* le USER consulte ses propres commentaires
* le USER reçoit une notification d'approbation de commentaire
* le USER reçoit une notification de rejet de commentaire

### 👤 ÉVÉNEMENTS DE GESTION DE PROFIL (USER)

* le USER consulte son profil
* le USER modifie ses informations personnelles (nom, email, téléphone, adresse)
* le USER modifie ses préférences de notification
* le USER consulte les règles et conditions de la bibliothèque

### 🆘 ÉVÉNEMENTS DE RÉCLAMATIONS (USER)

* le USER soumet une réclamation pour livre endommagé
* le USER soumet une réclamation pour livre perdu
* le USER soumet une réclamation pour frais incorrects
* le USER soumet une réclamation pour problème de compte
* le USER soumet une réclamation pour problème de service
* le USER soumet une réclamation pour problème technique
* le USER consulte ses réclamations
* le USER reçoit une notification de réclamation reçue
* le USER reçoit une notification de réclamation en cours de traitement
* le USER reçoit une notification de réclamation résolue
* le USER reçoit une notification de réclamation rejetée

### 🔧 ÉVÉNEMENTS SYSTÈME (AUTOMATIQUES)

* le SYSTEM exécute le processus de vérification des retards (tâche planifiée quotidienne)
* le SYSTEM envoie des rappels automatiques de date de retour (J-3, J-1)
* le SYSTEM envoie des notifications de retard (J+1, J+7, J+14)
* le SYSTEM met à jour automatiquement le statut des emprunts (active → overdue)
* le SYSTEM génère des statistiques d'utilisation
* le SYSTEM archive les anciens emprunts
* le SYSTEM nettoie les notifications lues de plus de 30 jours
* le SYSTEM sauvegarde les données
* le SYSTEM détecte les comptes inactifs (pas de connexion depuis 1 an)
* le SYSTEM notifie les administrateurs des livres perdus depuis plus de 60 jours
* le SYSTEM calcule les notes moyennes des livres
* le SYSTEM met à jour le nombre total d'emprunts par livre


## Règles Métier (Business Rules / Policies)

Les règles métier définissent les contraintes, limites et paramètres qui régissent le fonctionnement du système. Ces constantes évitent les "magic numbers" dans le code et centralisent les règles modifiables.

### 📊 Limites d'Emprunts

```typescript
const BORROWING_POLICIES = {
  // Limites quantitatives
  MAX_BOOKS_PER_USER: 3,              // Nombre maximum de livres empruntables simultanément
  MAX_BOOKS_STANDARD: 3,              // Limite pour utilisateurs standard
  MAX_BOOKS_PREMIUM: 5,               // Limite pour utilisateurs premium (si applicable)
  MAX_BOOKS_CHILDREN: 2,              // Limite pour comptes enfants
  
  // Limites de prolongation
  MAX_EXTENSION_COUNT: 1,             // Nombre maximum de prolongations par emprunt
  MAX_EXTENSION_DAYS: 7,              // Durée maximale d'une prolongation (en jours)
  MIN_EXTENSION_DAYS: 3,              // Durée minimale d'une prolongation
  
  // Restrictions
  MIN_DAYS_BEFORE_EXTENSION: 2,       // Délai minimum avant d'autoriser une prolongation
  MAX_ACTIVE_RESERVATIONS: 5          // Nombre maximum de réservations actives
}
```

### ⏱️ Durées et Délais

```typescript
const TIME_POLICIES = {
  // Durées d'emprunt
  DEFAULT_BORROWING_PERIOD: 14,       // Durée standard d'emprunt (14 jours)
  REFERENCE_BORROWING_PERIOD: 7,      // Durée pour livres de référence (7 jours)
  NEW_RELEASE_BORROWING_PERIOD: 7,    // Durée pour nouveautés (7 jours)
  
  // Rappels et notifications
  REMINDER_DAYS_BEFORE_DUE: [3, 1],   // Rappels à J-3 et J-1 avant échéance
  OVERDUE_NOTIFICATION_DAYS: [1, 7, 14, 30], // Notifications de retard à J+1, J+7, J+14, J+30
  
  // Suspensions et inactivité
  SUSPENSION_DURATION_FIRST_OFFENSE: 7,    // 7 jours pour 1ère infraction
  SUSPENSION_DURATION_SECOND_OFFENSE: 30,  // 30 jours pour 2ème infraction
  SUSPENSION_DURATION_THIRD_OFFENSE: 90,   // 90 jours pour 3ème infraction
  ACCOUNT_INACTIVE_DAYS: 365,              // Compte considéré inactif après 1 an
  AUTO_DEACTIVATE_INACTIVE_DAYS: 730,      // Désactivation automatique après 2 ans
  
  // Rétention des données
  NOTIFICATION_RETENTION_DAYS: 30,    // Suppression des notifications lues après 30 jours
  BORROWING_ARCHIVE_DAYS: 1095,       // Archivage des emprunts après 3 ans (1095 jours)
  CLAIM_AUTO_CLOSE_DAYS: 60           // Fermeture automatique des réclamations après 60 jours
}
```

### 💰 Frais et Pénalités

```typescript
const FEE_POLICIES = {
  // Frais de retard
  LATE_FEE_PER_DAY: 0.50,             // 0,50€ par jour de retard
  MAX_LATE_FEE: 50.00,                // Plafond de frais de retard (50€)
  LATE_FEE_GRACE_PERIOD: 1,           // 1 jour de grâce avant application des frais
  
  // Frais de perte/dommage
  LOST_BOOK_FEE_MULTIPLIER: 1.5,      // 150% du prix d'achat si livre perdu
  DAMAGED_BOOK_FEE_LIGHT: 5.00,       // 5€ pour dommages légers
  DAMAGED_BOOK_FEE_MODERATE: 15.00,   // 15€ pour dommages modérés
  DAMAGED_BOOK_FEE_SEVERE: 30.00,     // 30€ pour dommages sévères
  
  // Frais d'adhésion (si applicable)
  ANNUAL_MEMBERSHIP_FEE: 10.00,       // 10€ par an
  STUDENT_MEMBERSHIP_FEE: 5.00,       // 5€ pour étudiants
  SENIOR_MEMBERSHIP_FEE: 5.00,        // 5€ pour seniors
  FAMILY_MEMBERSHIP_FEE: 25.00        // 25€ pour adhésion familiale
}
```

### 🔒 Conditions d'Accès et Autorisations

```typescript
const ACCESS_POLICIES = {
  // Âge minimum
  MIN_AGE_FOR_ACCOUNT: 13,            // Âge minimum pour créer un compte
  MIN_AGE_FOR_ADULT_CONTENT: 18,      // Âge minimum pour livres adultes
  MIN_AGE_FOR_YOUNG_ADULT: 12,        // Âge minimum pour livres young adult
  
  // Sécurité
  MAX_FAILED_LOGIN_ATTEMPTS: 3,       // Blocage après 3 tentatives échouées
  ACCOUNT_LOCKOUT_DURATION: 30,       // Durée de blocage en minutes
  PASSWORD_MIN_LENGTH: 8,             // Longueur minimale du mot de passe
  PASSWORD_REQUIRE_SPECIAL_CHAR: true,// Caractère spécial obligatoire
  SESSION_TIMEOUT_MINUTES: 60,        // Timeout de session après 60 minutes
  
  // Autorisations d'emprunt
  MIN_ACCOUNT_AGE_DAYS: 1,            // Délai avant premier emprunt (1 jour)
  REQUIRE_EMAIL_VERIFICATION: true,   // Email vérifié obligatoire
  REQUIRE_PHONE_VERIFICATION: false,  // Téléphone vérifié (optionnel)
  
  // Restrictions par rôle
  VOLUNTEER_CAN_APPROVE_COMMENTS: false,  // Bénévole ne peut approuver commentaires
  ASSISTANT_CAN_DELETE_USERS: false,      // Assistant ne peut supprimer users
  ADMIN_ONLY_SYSTEM_CONFIG: true          // Seul admin peut modifier config système
}
```

### 📝 Validation de Données

```typescript
const VALIDATION_POLICIES = {
  // Commentaires
  MIN_COMMENT_LENGTH: 10,             // Minimum 10 caractères
  MAX_COMMENT_LENGTH: 500,            // Maximum 500 caractères
  MIN_RATING: 1,                      // Note minimale
  MAX_RATING: 5,                      // Note maximale
  REQUIRE_COMMENT_MODERATION: true,   // Modération obligatoire
  
  // ISBN
  ISBN_10_LENGTH: 10,                 // Format ISBN-10
  ISBN_13_LENGTH: 13,                 // Format ISBN-13
  ISBN_FORMAT_REGEX: /^(?:\d{9}[\dX]|\d{13})$/, // Validation format ISBN
  
  // Textes
  MIN_BOOK_TITLE_LENGTH: 1,           // Minimum 1 caractère
  MAX_BOOK_TITLE_LENGTH: 255,         // Maximum 255 caractères
  MIN_BOOK_DESCRIPTION_LENGTH: 0,     // Description optionnelle
  MAX_BOOK_DESCRIPTION_LENGTH: 2000,  // Maximum 2000 caractères
  
  // Utilisateurs
  MIN_NAME_LENGTH: 2,                 // Minimum 2 caractères
  MAX_NAME_LENGTH: 50,                // Maximum 50 caractères
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // Validation email
  PHONE_REGEX: /^[\d\s\-\+\(\)]{10,20}$/,    // Validation téléphone
  
  // Réclamations
  MIN_CLAIM_DESCRIPTION_LENGTH: 20,   // Minimum 20 caractères
  MAX_CLAIM_DESCRIPTION_LENGTH: 1000, // Maximum 1000 caractères
  MAX_CLAIM_ATTACHMENTS: 5            // Maximum 5 pièces jointes
}
```

### 📈 Statistiques et Seuils

```typescript
const ANALYTICS_POLICIES = {
  // Popularité
  POPULAR_BOOK_MIN_BORROWS: 10,       // Livre "populaire" si emprunté 10+ fois
  TRENDING_BOOK_PERIOD_DAYS: 30,      // Tendances calculées sur 30 derniers jours
  TRENDING_MIN_BORROWS: 5,            // Minimum 5 emprunts pour être "tendance"
  
  // Qualité de service
  TARGET_AVAILABILITY_RATE: 0.95,     // Objectif: 95% des livres disponibles
  MAX_ACCEPTABLE_OVERDUE_RATE: 0.05,  // Maximum acceptable: 5% de retards
  GOOD_RATING_THRESHOLD: 4.0,         // Note >= 4.0 = bon livre
  
  // Alertes
  LOW_STOCK_THRESHOLD: 1,             // Alerte si < 1 exemplaire disponible
  HIGH_DEMAND_THRESHOLD: 5,           // Alerte si 5+ réservations en attente
  DAMAGED_BOOK_THRESHOLD_PERCENT: 0.10, // Alerte si 10%+ des livres endommagés
  
  // Recommandations
  RECOMMEND_BASED_ON_HISTORY: 10,     // Recommandations basées sur 10 derniers emprunts
  SIMILAR_BOOKS_COUNT: 5,             // Afficher 5 livres similaires
  NEW_RELEASES_DAYS: 90               // Nouveautés = livres ajoutés < 90 jours
}
```

### 🔄 Règles de Workflow

```typescript
const WORKFLOW_POLICIES = {
  // Traitement des demandes
  AUTO_APPROVE_EXTENSION_IF_NO_RESERVATION: true,  // Auto-approuver si pas de réservation
  AUTO_REJECT_EXTENSION_IF_OVERDUE: true,          // Auto-rejeter si déjà en retard
  AUTO_SUSPEND_ON_THIRD_OVERDUE: true,             // Auto-suspendre à la 3ème infraction
  
  // Priorités
  CLAIM_AUTO_PRIORITY_URGENT_KEYWORDS: ['urgent', 'perdu', 'vol'], // Mots-clés urgence
  CLAIM_DEFAULT_PRIORITY: 'MEDIUM',    // Priorité par défaut
  
  // Notifications
  BATCH_NOTIFICATIONS: true,           // Grouper les notifications
  BATCH_NOTIFICATION_INTERVAL_HOURS: 24, // Envoi quotidien
  SEND_EMAIL_NOTIFICATIONS: true,      // Activer emails
  SEND_SMS_NOTIFICATIONS: false,       // SMS désactivé par défaut
  
  // Modération
  AUTO_APPROVE_COMMENTS_FROM_VERIFIED_USERS: false, // Toujours modérer
  FLAG_COMMENT_IF_CONTAINS_PROFANITY: true,         // Signaler contenus inappropriés
  MAX_COMMENTS_PER_USER_PER_DAY: 10    // Limite anti-spam
}
```

### 🏷️ Catégorisation et Tags

```typescript
const CATEGORIZATION_POLICIES = {
  // Limites
  MAX_CATEGORIES_PER_BOOK: 3,         // Maximum 3 catégories par livre
  MAX_TAGS_PER_BOOK: 10,              // Maximum 10 tags par livre
  MIN_TAG_LENGTH: 2,                  // Tag minimum 2 caractères
  MAX_TAG_LENGTH: 30,                 // Tag maximum 30 caractères
  
  // Classification automatique
  AUTO_TAG_ENABLED: true,             // Tagging automatique activé
  AUTO_CATEGORIZE_BY_ISBN: true,      // Catégorisation via ISBN
  
  // Recherche
  SEARCH_MIN_QUERY_LENGTH: 2,         // Recherche min 2 caractères
  SEARCH_MAX_RESULTS: 100,            // Maximum 100 résultats
  SEARCH_FUZZY_MATCH_THRESHOLD: 0.8   // Seuil de correspondance floue (80%)
}
```

### 🎯 Utilisation dans le Code

```typescript
// ✅ EXEMPLE D'UTILISATION CORRECTE
class BorrowerService {
  canBorrowBook(borrower: Borrower): boolean {
    return borrower.borrowed_Books.length < BORROWING_POLICIES.MAX_BOOKS_PER_USER;
  }
  
  calculateDueDate(borrowDate: Date, bookCategory: BookCategory): Date {
    const days = bookCategory === BookCategory.REFERENCE 
      ? TIME_POLICIES.REFERENCE_BORROWING_PERIOD 
      : TIME_POLICIES.DEFAULT_BORROWING_PERIOD;
    
    return addDays(borrowDate, days);
  }
  
  canExtend(record: BorrowingRecord): boolean {
    return record.extension_Count < BORROWING_POLICIES.MAX_EXTENSION_COUNT
      && !this.isOverdue(record)
      && WORKFLOW_POLICIES.AUTO_APPROVE_EXTENSION_IF_NO_RESERVATION;
  }
}
```


``` typescript 


