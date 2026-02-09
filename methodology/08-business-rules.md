[← Events Catalog](07-events-catalog.md) | [Index](README.md) | [Tests →](../tests/)

---

# 📏 Règles Métier et Politiques

## 🎯 Introduction

Les **règles métier (Business Rules)** définissent les **contraintes, limites et paramètres** qui régissent le fonctionnement du système de gestion de bibliothèque. Ces politiques permettent de :

- ✅ **Éviter les "magic numbers"** éparpillés dans le code
- ✅ **Centraliser les règles modifiables** dans un fichier unique
- ✅ **Faciliter la maintenance** et l'évolution du système
- ✅ **Garantir la cohérence** des règles à travers tout le code
- ✅ **Documenter les décisions métier** de manière explicite

Toutes les règles sont regroupées dans le fichier `src/policies/business-rules.ts` et exportées via des constantes typées.

---

## 📊 1. Politiques d'Emprunt (BORROWING_POLICIES)

### 🎯 Objectif
Définir les **limites quantitatives** d'emprunts et de prolongations.

```typescript
const BORROWING_POLICIES = {
  // Limites quantitatives par type d'utilisateur
  MAX_BOOKS_PER_USER: 3,              // Nombre maximum de livres simultanés (standard)
  MAX_BOOKS_STANDARD: 3,              // Limite pour utilisateurs standard
  MAX_BOOKS_PREMIUM: 5,               // Limite pour utilisateurs premium (si applicable)
  MAX_BOOKS_CHILDREN: 2,              // Limite pour comptes enfants
  
  // Limites de prolongation
  MAX_EXTENSION_COUNT: 1,             // Nombre maximum de prolongations par emprunt
  MAX_EXTENSION_DAYS: 7,              // Durée maximale d'une prolongation (en jours)
  MIN_EXTENSION_DAYS: 3,              // Durée minimale d'une prolongation
  
  // Restrictions
  MIN_DAYS_BEFORE_EXTENSION: 2,       // Délai minimum avant d'autoriser une prolongation
  MAX_ACTIVE_RESERVATIONS: 5,         // Nombre maximum de réservations actives
} as const;
```

### 📌 Cas d'usage
- Vérifier si un utilisateur peut emprunter un livre supplémentaire
- Limiter les prolongations abusives
- Adapter les limites selon le type de compte

---

## ⏱️ 2. Politiques Temporelles (TIME_POLICIES)

### 🎯 Objectif
Gérer les **durées d'emprunt, rappels, suspensions et archivage**.

```typescript
const TIME_POLICIES = {
  // Durées d'emprunt par catégorie de livre
  DEFAULT_BORROWING_PERIOD: 14,       // Durée standard d'emprunt (14 jours)
  REFERENCE_BORROWING_PERIOD: 7,      // Durée pour livres de référence (7 jours)
  NEW_RELEASE_BORROWING_PERIOD: 7,    // Durée pour nouveautés (7 jours)
  
  // Rappels et notifications automatiques
  REMINDER_DAYS_BEFORE_DUE: [3, 1],   // Rappels à J-3 et J-1 avant échéance
  OVERDUE_NOTIFICATION_DAYS: [1, 7, 14, 30], // Notifications de retard à J+1, J+7, J+14, J+30
  
  // Suspensions et sanctions
  SUSPENSION_DURATION_FIRST_OFFENSE: 7,    // 7 jours pour 1ère infraction
  SUSPENSION_DURATION_SECOND_OFFENSE: 30,  // 30 jours pour 2ème infraction
  SUSPENSION_DURATION_THIRD_OFFENSE: 90,   // 90 jours pour 3ème infraction
  ACCOUNT_INACTIVE_DAYS: 365,              // Compte considéré inactif après 1 an
  AUTO_DEACTIVATE_INACTIVE_DAYS: 730,      // Désactivation automatique après 2 ans
  
  // Rétention et archivage des données
  NOTIFICATION_RETENTION_DAYS: 30,    // Suppression des notifications lues après 30 jours
  BORROWING_ARCHIVE_DAYS: 1095,       // Archivage des emprunts après 3 ans (1095 jours)
  CLAIM_AUTO_CLOSE_DAYS: 60,          // Fermeture automatique des réclamations après 60 jours
} as const;
```

### 📌 Cas d'usage
- Calculer la date de retour selon le type de livre
- Planifier les rappels automatiques (J-3, J-1)
- Appliquer des sanctions graduées en cas de récidive

---

## 💰 3. Politiques de Frais (FEE_POLICIES)

### 🎯 Objectif
Définir les **frais de retard, pénalités et coûts d'adhésion**.

```typescript
const FEE_POLICIES = {
  // Frais de retard
  LATE_FEE_PER_DAY: 0.50,             // 0,50€ par jour de retard
  MAX_LATE_FEE: 50.00,                // Plafond de frais de retard (50€)
  LATE_FEE_GRACE_PERIOD: 1,           // 1 jour de grâce avant application des frais
  
  // Frais de perte et dommages
  LOST_BOOK_FEE_MULTIPLIER: 1.5,      // 150% du prix d'achat si livre perdu
  DAMAGED_BOOK_FEE_LIGHT: 5.00,       // 5€ pour dommages légers
  DAMAGED_BOOK_FEE_MODERATE: 15.00,   // 15€ pour dommages modérés
  DAMAGED_BOOK_FEE_SEVERE: 30.00,     // 30€ pour dommages sévères
  
  // Frais d'adhésion annuelle (si applicable)
  ANNUAL_MEMBERSHIP_FEE: 10.00,       // 10€ par an (standard)
  STUDENT_MEMBERSHIP_FEE: 5.00,       // 5€ pour étudiants
  SENIOR_MEMBERSHIP_FEE: 5.00,        // 5€ pour seniors
  FAMILY_MEMBERSHIP_FEE: 25.00,       // 25€ pour adhésion familiale
} as const;
```

### 📌 Cas d'usage
- Calculer les frais de retard de manière progressive
- Appliquer des pénalités en cas de livre perdu/endommagé
- Gérer les cotisations annuelles selon le profil

---

## 🔒 4. Politiques d'Accès (ACCESS_POLICIES)

### 🎯 Objectif
Contrôler les **conditions d'accès, restrictions d'âge et sécurité**.

```typescript
const ACCESS_POLICIES = {
  // Restrictions d'âge
  MIN_AGE_FOR_ACCOUNT: 13,            // Âge minimum pour créer un compte
  MIN_AGE_FOR_ADULT_CONTENT: 18,      // Âge minimum pour livres adultes
  MIN_AGE_FOR_YOUNG_ADULT: 12,        // Âge minimum pour livres young adult
  
  // Sécurité et authentification
  MAX_FAILED_LOGIN_ATTEMPTS: 3,       // Blocage après 3 tentatives échouées
  ACCOUNT_LOCKOUT_DURATION: 30,       // Durée de blocage en minutes
  PASSWORD_MIN_LENGTH: 8,             // Longueur minimale du mot de passe
  PASSWORD_REQUIRE_SPECIAL_CHAR: true,// Caractère spécial obligatoire
  SESSION_TIMEOUT_MINUTES: 60,        // Timeout de session après 60 minutes
  
  // Autorisations d'emprunt
  MIN_ACCOUNT_AGE_DAYS: 1,            // Délai avant premier emprunt (1 jour)
  REQUIRE_EMAIL_VERIFICATION: true,   // Email vérifié obligatoire
  REQUIRE_PHONE_VERIFICATION: false,  // Téléphone vérifié (optionnel)
  
  // Restrictions par rôle (LIBRARIAN)
  VOLUNTEER_CAN_APPROVE_COMMENTS: false,  // Bénévole ne peut approuver commentaires
  ASSISTANT_CAN_DELETE_USERS: false,      // Assistant ne peut supprimer utilisateurs
  ADMIN_ONLY_SYSTEM_CONFIG: true,         // Seul admin peut modifier config système
} as const;
```

### 📌 Cas d'usage
- Bloquer l'accès aux contenus selon l'âge
- Sécuriser les comptes avec des mots de passe robustes
- Définir les permissions des rôles LIBRARIAN

---

## 📝 5. Politiques de Validation (VALIDATION_POLICIES)

### 🎯 Objectif
Valider les **formats de données, longueurs et expressions régulières**.

```typescript
const VALIDATION_POLICIES = {
  // Commentaires et notes
  MIN_COMMENT_LENGTH: 10,             // Minimum 10 caractères
  MAX_COMMENT_LENGTH: 500,            // Maximum 500 caractères
  MIN_RATING: 1,                      // Note minimale (étoiles)
  MAX_RATING: 5,                      // Note maximale (étoiles)
  REQUIRE_COMMENT_MODERATION: true,   // Modération obligatoire
  
  // ISBN (International Standard Book Number)
  ISBN_10_LENGTH: 10,                 // Format ISBN-10
  ISBN_13_LENGTH: 13,                 // Format ISBN-13
  ISBN_FORMAT_REGEX: /^(?:\d{9}[\dX]|\d{13})$/, // Validation format ISBN
  
  // Textes de livres
  MIN_BOOK_TITLE_LENGTH: 1,           // Minimum 1 caractère
  MAX_BOOK_TITLE_LENGTH: 255,         // Maximum 255 caractères
  MIN_BOOK_DESCRIPTION_LENGTH: 0,     // Description optionnelle
  MAX_BOOK_DESCRIPTION_LENGTH: 2000,  // Maximum 2000 caractères
  
  // Utilisateurs
  MIN_NAME_LENGTH: 2,                 // Minimum 2 caractères
  MAX_NAME_LENGTH: 50,                // Maximum 50 caractères
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // Validation email
  PHONE_REGEX: /^[\d\s\-\+\(\)]{10,20}$/,    // Validation téléphone (international)
  
  // Réclamations
  MIN_CLAIM_DESCRIPTION_LENGTH: 20,   // Minimum 20 caractères
  MAX_CLAIM_DESCRIPTION_LENGTH: 1000, // Maximum 1000 caractères
  MAX_CLAIM_ATTACHMENTS: 5,           // Maximum 5 pièces jointes
} as const;
```

### 📌 Cas d'usage
- Valider les commentaires avant soumission
- Vérifier le format ISBN lors de l'ajout d'un livre
- Contrôler les longueurs de champs utilisateur

---

## 📈 6. Politiques d'Analyse (ANALYTICS_POLICIES)

### 🎯 Objectif
Définir les **seuils statistiques, tendances et alertes**.

```typescript
const ANALYTICS_POLICIES = {
  // Popularité et tendances
  POPULAR_BOOK_MIN_BORROWS: 10,       // Livre "populaire" si emprunté 10+ fois
  TRENDING_BOOK_PERIOD_DAYS: 30,      // Tendances calculées sur 30 derniers jours
  TRENDING_MIN_BORROWS: 5,            // Minimum 5 emprunts pour être "tendance"
  
  // Qualité de service (KPI)
  TARGET_AVAILABILITY_RATE: 0.95,     // Objectif: 95% des livres disponibles
  MAX_ACCEPTABLE_OVERDUE_RATE: 0.05,  // Maximum acceptable: 5% de retards
  GOOD_RATING_THRESHOLD: 4.0,         // Note >= 4.0 = bon livre
  
  // Alertes automatiques
  LOW_STOCK_THRESHOLD: 1,             // Alerte si < 1 exemplaire disponible
  HIGH_DEMAND_THRESHOLD: 5,           // Alerte si 5+ réservations en attente
  DAMAGED_BOOK_THRESHOLD_PERCENT: 0.10, // Alerte si 10%+ des livres endommagés
  
  // Recommandations
  RECOMMEND_BASED_ON_HISTORY: 10,     // Recommandations basées sur 10 derniers emprunts
  SIMILAR_BOOKS_COUNT: 5,             // Afficher 5 livres similaires
  NEW_RELEASES_DAYS: 90,              // Nouveautés = livres ajoutés < 90 jours
} as const;
```

### 📌 Cas d'usage
- Détecter les livres populaires et en tendance
- Générer des alertes pour l'équipe de gestion
- Recommander des livres similaires aux utilisateurs

---

## 🔄 7. Politiques de Workflow (WORKFLOW_POLICIES)

### 🎯 Objectif
Automatiser les **décisions métier, modération et priorités**.

```typescript
const WORKFLOW_POLICIES = {
  // Traitement automatique des demandes
  AUTO_APPROVE_EXTENSION_IF_NO_RESERVATION: true,  // Auto-approuver si pas de réservation
  AUTO_REJECT_EXTENSION_IF_OVERDUE: true,          // Auto-rejeter si déjà en retard
  AUTO_SUSPEND_ON_THIRD_OVERDUE: true,             // Auto-suspendre à la 3ème infraction
  
  // Priorités des réclamations
  CLAIM_AUTO_PRIORITY_URGENT_KEYWORDS: ['urgent', 'perdu', 'vol'], // Mots-clés urgence
  CLAIM_DEFAULT_PRIORITY: 'MEDIUM' as const,       // Priorité par défaut
  
  // Notifications groupées
  BATCH_NOTIFICATIONS: true,           // Grouper les notifications
  BATCH_NOTIFICATION_INTERVAL_HOURS: 24, // Envoi quotidien (toutes les 24h)
  SEND_EMAIL_NOTIFICATIONS: true,      // Activer les emails
  SEND_SMS_NOTIFICATIONS: false,       // SMS désactivé par défaut
  
  // Modération des commentaires
  AUTO_APPROVE_COMMENTS_FROM_VERIFIED_USERS: false, // Toujours modérer (sécurité)
  FLAG_COMMENT_IF_CONTAINS_PROFANITY: true,         // Signaler contenus inappropriés
  MAX_COMMENTS_PER_USER_PER_DAY: 10,   // Limite anti-spam (10 commentaires/jour)
} as const;
```

### 📌 Cas d'usage
- Automatiser l'approbation des prolongations
- Détecter et prioriser les réclamations urgentes
- Modérer les commentaires et prévenir le spam

---

## 🏷️ 8. Politiques de Catégorisation (CATEGORIZATION_POLICIES)

### 🎯 Objectif
Gérer les **tags, catégories et recherches**.

```typescript
const CATEGORIZATION_POLICIES = {
  // Limites de tags et catégories
  MAX_CATEGORIES_PER_BOOK: 3,         // Maximum 3 catégories par livre
  MAX_TAGS_PER_BOOK: 10,              // Maximum 10 tags par livre
  MIN_TAG_LENGTH: 2,                  // Tag minimum 2 caractères
  MAX_TAG_LENGTH: 30,                 // Tag maximum 30 caractères
  
  // Classification automatique
  AUTO_TAG_ENABLED: true,             // Tagging automatique activé
  AUTO_CATEGORIZE_BY_ISBN: true,      // Catégorisation automatique via ISBN
  
  // Recherche
  SEARCH_MIN_QUERY_LENGTH: 2,         // Recherche minimum 2 caractères
  SEARCH_MAX_RESULTS: 100,            // Maximum 100 résultats
  SEARCH_FUZZY_MATCH_THRESHOLD: 0.8,  // Seuil de correspondance floue (80%)
} as const;
```

### 📌 Cas d'usage
- Limiter le nombre de catégories et tags par livre
- Activer la recherche floue (tolérance aux fautes)
- Catégoriser automatiquement via API ISBN

---

## 🎯 Exemple d'Utilisation dans le Code

### ✅ Cas 1: Vérifier si un utilisateur peut emprunter

```typescript
import { BORROWING_POLICIES } from '@/policies/business-rules';

class BorrowerService {
  canBorrowBook(borrower: Borrower): boolean {
    return borrower.borrowed_Books.length < BORROWING_POLICIES.MAX_BOOKS_PER_USER;
  }
}
```

### ✅ Cas 2: Calculer la date de retour selon la catégorie

```typescript
import { TIME_POLICIES } from '@/policies/business-rules';
import { addDays } from 'date-fns';

class BorrowingService {
  calculateDueDate(borrowDate: Date, bookCategory: BookCategory): Date {
    const days = bookCategory === BookCategory.REFERENCE 
      ? TIME_POLICIES.REFERENCE_BORROWING_PERIOD 
      : TIME_POLICIES.DEFAULT_BORROWING_PERIOD;
    
    return addDays(borrowDate, days);
  }
}
```

### ✅ Cas 3: Valider une demande de prolongation

```typescript
import { BORROWING_POLICIES, WORKFLOW_POLICIES } from '@/policies/business-rules';

class ExtensionService {
  canExtend(record: BorrowingRecord): boolean {
    const hasReachedMaxExtensions = 
      record.extension_Count >= BORROWING_POLICIES.MAX_EXTENSION_COUNT;
    
    const isOverdue = this.isOverdue(record);
    
    const autoReject = 
      WORKFLOW_POLICIES.AUTO_REJECT_EXTENSION_IF_OVERDUE && isOverdue;
    
    return !hasReachedMaxExtensions && !autoReject;
  }
}
```

### ✅ Cas 4: Calculer les frais de retard

```typescript
import { FEE_POLICIES } from '@/policies/business-rules';

class FeeCalculator {
  calculateLateFee(daysOverdue: number): number {
    if (daysOverdue <= FEE_POLICIES.LATE_FEE_GRACE_PERIOD) {
      return 0; // Période de grâce
    }
    
    const fee = (daysOverdue - FEE_POLICIES.LATE_FEE_GRACE_PERIOD) 
                * FEE_POLICIES.LATE_FEE_PER_DAY;
    
    return Math.min(fee, FEE_POLICIES.MAX_LATE_FEE); // Plafonner
  }
}
```

---

## 📊 Tableau Récapitulatif

| Catégorie | Nombre de Règles | Fichier Source |
|-----------|------------------|----------------|
| 📊 Emprunts | 9 | `BORROWING_POLICIES` |
| ⏱️ Temps et délais | 13 | `TIME_POLICIES` |
| 💰 Frais et pénalités | 11 | `FEE_POLICIES` |
| 🔒 Accès et sécurité | 13 | `ACCESS_POLICIES` |
| 📝 Validation | 18 | `VALIDATION_POLICIES` |
| 📈 Analyse et KPI | 11 | `ANALYTICS_POLICIES` |
| 🔄 Workflow | 11 | `WORKFLOW_POLICIES` |
| 🏷️ Catégorisation | 9 | `CATEGORIZATION_POLICIES` |
| **TOTAL** | **~95 règles** | `src/policies/business-rules.ts` |

---

## 🎓 Avantages de cette Approche

### ✅ 1. Maintenabilité
- Toutes les règles dans **un seul fichier**
- Modifications centralisées (pas de recherche dans tout le code)

### ✅ 2. Lisibilité
- Noms de constantes **explicites** (`MAX_BOOKS_PER_USER` plutôt que `3`)
- Documentation intégrée (commentaires)

### ✅ 3. Testabilité
- Règles **mockables** facilement dans les tests unitaires
- Pas de dépendances externes

### ✅ 4. Évolutivité
- Ajout de nouvelles règles sans toucher au code métier
- Possibilité de passer à une **configuration dynamique** (BDD, API)

### ✅ 5. Type Safety (TypeScript)
- Utilisation de `as const` pour éviter les modifications accidentelles
- Autocomplétion dans l'IDE

---

## 🔗 Fichier Source

📁 **Fichier**: [`src/policies/business-rules.ts`](../src/policies/business-rules.ts)

```typescript
// Export centralisé de toutes les politiques
export {
  BORROWING_POLICIES,
  TIME_POLICIES,
  FEE_POLICIES,
  ACCESS_POLICIES,
  VALIDATION_POLICIES,
  ANALYTICS_POLICIES,
  WORKFLOW_POLICIES,
  CATEGORIZATION_POLICIES,
} as const;
```

---

## 🎯 Conclusion

Les **règles métier centralisées** constituent le **cerveau du système**. Elles garantissent la cohérence, facilitent la maintenance et permettent une évolution rapide des politiques sans refactorisation massive du code.

**Bonne pratique**: Toujours référencer les politiques via les constantes, **jamais de valeurs en dur** (magic numbers) dans le code métier.

---

[← Events Catalog](07-events-catalog.md) | [Index](README.md) | [Tests →](../tests/)
