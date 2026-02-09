# 🏷️ Énumérations

[← Retour à l'index](README.md) | [← Interfaces](01-interfaces.md)

---

## BookCategory

Catégories de livres pour la classification du catalogue.

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

**Total**: 25 catégories

**Usage**: Classification des livres, règles d'emprunt spécifiques (ex: REFERENCE a une période plus courte)

---

## PhysicalState

État physique du livre pour le suivi de l'usure et la gestion d'inventaire.

```typescript
enum PhysicalState {
  EXCELLENT = "excellent",  // Comme neuf, aucune marque d'usure
  GOOD = "good",           // Bon état général, légères traces d'utilisation
  FAIR = "fair",           // État correct, signes d'usure visibles
  POOR = "poor",           // Mauvais état, nécessite réparation
  DAMAGED = "damaged",     // Endommagé, non empruntable
  LOST = "lost",           // Perdu par un emprunteur
  IN_REPAIR = "in_repair"  // En cours de réparation
}
```

**Impact sur les emprunts**:
- `DAMAGED`, `LOST`, `IN_REPAIR` → Non empruntable
- `POOR` → Emprunt possible avec avertissement
- `EXCELLENT`, `GOOD`, `FAIR` → Emprunt normal

---

## BorrowingStatus

Statut d'un enregistrement d'emprunt dans le système.

```typescript
enum BorrowingStatus {
  ACTIVE = "active",       // Emprunt en cours
  RETURNED = "returned",   // Livre retourné
  OVERDUE = "overdue",     // En retard
  EXTENDED = "extended",   // Prolongé
  CANCELLED = "cancelled", // Annulé avant retrait
  RESERVED = "reserved"    // Réservé mais pas encore emprunté
}
```

**Transitions d'état**:
```
RESERVED → ACTIVE → RETURNED
       ↘         ↘ OVERDUE → RETURNED
         CANCELLED
                ↘ EXTENDED → RETURNED/OVERDUE
```

---

## NotificationType

Types de notifications envoyées aux utilisateurs.

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

**Total**: 14 types de notifications

**Catégories**:
- **Emprunts**: DUE_DATE, OVERDUE, EXTENSION_APPROVED, EXTENSION_DENIED
- **Disponibilité**: AVAILABILITY, RESERVATION_READY
- **Compte**: ACCOUNT_SUSPENDED, ACCOUNT_ACTIVATED
- **Contenu**: COMMENT_APPROVED, COMMENT_REJECTED, NEW_BOOK_ADDED
- **Support**: CLAIM_RECEIVED, CLAIM_RESOLVED
- **Général**: GENERAL

---

## LibrarianRole

Rôles et niveaux de permissions des bibliothécaires.

```typescript
enum LibrarianRole {
  ADMIN = "admin",        // Administrateur (tous les droits)
  STANDARD = "standard",  // Bibliothécaire standard
  ASSISTANT = "assistant",// Assistant (droits limités)
  VOLUNTEER = "volunteer" // Bénévole (lecture seule + certaines actions)
}
```

**Matrice de permissions** (voir [Access Policies](08-business-rules.md#access-policies)):
- ADMIN: Toutes les opérations
- STANDARD: Gestion livres + users + emprunts
- ASSISTANT: Gestion emprunts + consultation
- VOLUNTEER: Lecture seule + aide aux emprunts

---

## UserStatus

Statut d'un compte utilisateur dans le système.

```typescript
enum UserStatus {
  ACTIVE = "active",           // Compte actif
  INACTIVE = "inactive",       // Compte inactif (pas de connexion récente)
  SUSPENDED = "suspended",     // Suspendu temporairement
  DEACTIVATED = "deactivated", // Désactivé par admin
  PENDING = "pending",         // En attente d'approbation
  BANNED = "banned"            // Banni définitivement
}
```

**Impact sur les emprunts**:
- `ACTIVE` → Peut emprunter ✅
- `INACTIVE` → Peut emprunter (mais compte à surveiller)
- `SUSPENDED` → Ne peut pas emprunter ❌
- `DEACTIVATED` → Ne peut pas emprunter ❌
- `PENDING` → Ne peut pas emprunter (en attente validation) ❌
- `BANNED` → Aucun accès ❌

---

## ClaimStatus

Statut d'une réclamation utilisateur.

```typescript
enum ClaimStatus {
  PENDING = "pending",         // En attente de traitement
  IN_PROGRESS = "in_progress", // En cours de traitement
  RESOLVED = "resolved",       // Résolue
  REJECTED = "rejected",       // Rejetée
  CLOSED = "closed"            // Fermée
}
```

**Workflow**:
```
PENDING → IN_PROGRESS → RESOLVED → CLOSED
                     ↘ REJECTED → CLOSED
```

---

## ClaimPriority

Niveau de priorité d'une réclamation.

```typescript
enum ClaimPriority {
  LOW = "low",       // Basse priorité
  MEDIUM = "medium", // Priorité moyenne
  HIGH = "high",     // Haute priorité
  URGENT = "urgent"  // Urgente
}
```

**SLA (Service Level Agreement)**:
- `URGENT`: Traitement sous 24h
- `HIGH`: Traitement sous 3 jours
- `MEDIUM`: Traitement sous 7 jours
- `LOW`: Traitement sous 14 jours

---

## ClaimType

Types de réclamations possibles.

```typescript
enum ClaimType {
  DAMAGED_BOOK = "damaged_book",         // Livre endommagé
  LOST_BOOK = "lost_book",               // Livre perdu
  INCORRECT_CHARGE = "incorrect_charge", // Frais incorrects
  ACCOUNT_ISSUE = "account_issue",       // Problème de compte
  SERVICE_COMPLAINT = "service_complaint",// Plainte service
  TECHNICAL_ISSUE = "technical_issue",   // Problème technique
  OTHER = "other"                        // Autre
}
```

---

## ExtensionStatus

Statut d'une demande de prolongation d'emprunt.

```typescript
enum ExtensionStatus {
  PENDING = "pending",   // En attente
  APPROVED = "approved", // Approuvée
  DENIED = "denied",     // Refusée
  EXPIRED = "expired"    // Expirée
}
```

---

## SearchFilter

Filtres disponibles pour la recherche de livres.

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

**Usage**: Construction dynamique de requêtes de recherche multi-critères.

---

## 📊 Récapitulatif

| Énumération | Nombre de valeurs | Usage principal |
|-------------|-------------------|-----------------|
| BookCategory | 25 | Classification catalogue |
| PhysicalState | 7 | Gestion inventaire |
| BorrowingStatus | 6 | État emprunts |
| NotificationType | 14 | Système notifications |
| LibrarianRole | 4 | Contrôle d'accès |
| UserStatus | 6 | Gestion comptes |
| ClaimStatus | 5 | Workflow réclamations |
| ClaimPriority | 4 | Priorisation support |
| ClaimType | 7 | Catégorisation réclamations |
| ExtensionStatus | 4 | Prolongations |
| SearchFilter | 8 | Recherche avancée |

**Total**: 11 énumérations | 90 valeurs possibles

---

[← Interfaces](01-interfaces.md) | [Retour à l'index](README.md) | [Modèles de Données →](03-models.md)
