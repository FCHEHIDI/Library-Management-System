# 📚 Système de Gestion de Bibliothèque - Documentation Technique

> Guide complet pour l'implémentation d'un système de gestion de bibliothèque avec architecture événementielle et principes SOLID

---

## 📖 Table des Matières

### 🏗️ Architecture du Système

1. **[Interfaces](01-interfaces.md)**
   - INotifiable - Gestion des notifications
   - IBorrowable - Gestion des emprunts
   - IUser - Interface utilisateur de base
   - ISearchable - Capacités de recherche

2. **[Énumérations](02-enums.md)**
   - BookCategory (25 catégories)
   - PhysicalState (7 états)
   - BorrowingStatus (6 statuts)
   - NotificationType (14 types)
   - UserStatus, ClaimStatus, LibrarianRole
   - ExtensionStatus, SearchFilter

3. **[Modèles de Données](03-models.md)**
   - Book - Représentation d'un livre
   - BorrowingRecord - Enregistrement d'emprunt
   - Comment - Commentaires utilisateurs
   - Notification - Notifications système

### 👥 Classes du Domaine

4. **[Classe Librarian](04-class-librarian.md)**
   - Gestion des livres (10 méthodes)
   - Gestion des utilisateurs (9 méthodes)
   - Communication (6 méthodes)
   - Modération des commentaires (3 méthodes)
   - Total: 33 méthodes publiques

5. **[Classe Borrower](05-class-borrower.md)**
   - Opérations sur les livres (7 méthodes)
   - Recherche et filtrage (5 méthodes)
   - Commentaires et avis (4 méthodes)
   - Gestion des notifications (5 méthodes)
   - Gestion de profil (4 méthodes)
   - Réclamations (2 méthodes)
   - Total: 27 méthodes publiques

6. **[Classe Library](06-class-library.md)**
   - Gestion des livres (5 méthodes)
   - Gestion des utilisateurs (3 méthodes)
   - Gestion des emprunts (4 méthodes)
   - Total: 12 méthodes publiques

### 📋 Événements et Règles Métier

7. **[Catalogue d'Événements Complet](07-events-catalog.md)**
   - Authentification (8 événements)
   - Gestion utilisateurs (14 événements)
   - Gestion livres (16 événements)
   - Emprunts (11 événements)
   - Communications (7 événements)
   - Notifications (18 événements)
   - Commentaires (5 événements)
   - Consultation (11 événements)
   - Réclamations (11 événements)
   - Système automatique (12 événements)
   - **Total: 140+ événements métier**

8. **[Règles Métier et Politiques](08-business-rules.md)**
   - Limites d'emprunts (BORROWING_POLICIES)
   - Durées et délais (TIME_POLICIES)
   - Frais et pénalités (FEE_POLICIES)
   - Conditions d'accès (ACCESS_POLICIES)
   - Validation de données (VALIDATION_POLICIES)
   - Statistiques et seuils (ANALYTICS_POLICIES)
   - Règles de workflow (WORKFLOW_POLICIES)
   - Catégorisation (CATEGORIZATION_POLICIES)
   - **Total: 100+ règles métier**

---

## 🎯 Comment Utiliser Cette Documentation

### Pour les Développeurs
1. Commencez par [Interfaces](01-interfaces.md) pour comprendre les contrats
2. Consultez [Énumérations](02-enums.md) pour les types de données
3. Étudiez [Modèles de Données](03-models.md) pour la structure des données
4. Implémentez les classes domaine : [Librarian](04-class-librarian.md), [Borrower](05-class-borrower.md), [Library](06-class-library.md)
5. Référez-vous au [Catalogue d'Événements](07-events-catalog.md) pour mapper les événements métier aux méthodes
6. Utilisez [Règles Métier](08-business-rules.md) pour valider la logique business

### Pour les Architectes
1. [Catalogue d'Événements](07-events-catalog.md) → Vue complète des capacités système
2. [Règles Métier](08-business-rules.md) → Contraintes et limites du système
3. Classes domaine → Distribution des responsabilités

### Pour les Product Owners
1. [Catalogue d'Événements](07-events-catalog.md) → Fonctionnalités disponibles
2. [Règles Métier](08-business-rules.md) → Paramètres configurables

---

## 📊 Statistiques du Système

| Composant | Quantité | Détails |
|-----------|----------|---------|
| **Interfaces** | 4 | IUser, INotifiable, ISearchable, IBorrowable |
| **Énumérations** | 11 | 25 catégories de livres, 14 types de notifications, etc. |
| **Modèles** | 4 | Book, BorrowingRecord, Comment, Notification |
| **Classes Domaine** | 3 | Librarian (33 méthodes), Borrower (27 méthodes), Library (12 méthodes) |
| **Événements** | 140+ | Événements métier catalogués |
| **Règles Métier** | 100+ | Politiques et contraintes business |
| **Méthodes Publiques** | 72 | Total des méthodes publiques dans les 3 classes |

---

## 🏛️ Principes Architecturaux

### Event-Driven Design
Chaque événement métier → Une méthode publique
- ✅ Traçabilité requirements → code
- ✅ API auto-documentée
- ✅ Tests ciblés (1 événement = 1 test)

### SOLID Principles
- **S**ingle Responsibility: Une méthode = Un événement = Une responsabilité
- **O**pen/Closed: Nouveaux événements = Nouvelles méthodes (pas de modification)
- **L**iskov Substitution: Les implémentations respectent les contrats d'interface
- **I**nterface Segregation: Interfaces petites et focalisées
- **D**ependency Inversion: Dépendances sur abstractions (interfaces)

### Business Rules Centralization
- Toutes les règles dans `POLICIES` objects
- Pas de "magic numbers" dans le code
- Configuration centralisée et modifiable

---

## 🚀 Implémentation

Cette documentation supporte l'implémentation en:
- **TypeScript** ✅ (Implémentation de référence)
- **Python/FastAPI** 🔄 (Prochaine étape)
- **Java/Spring Boot** 📋 (Planifié)
- **.NET/C#** 📋 (Planifié)

---

## 📝 Conventions de Nommage

### TypeScript/JavaScript
```typescript
// Classes: PascalCase
class Borrower, Library, Librarian

// Méthodes: camelCase
borrowBook(), sendNotification()

// Constantes: UPPER_SNAKE_CASE
MAX_BOOKS_PER_USER, DEFAULT_BORROWING_PERIOD

// Interfaces: IPascalCase
IUser, INotifiable

// Enums: PascalCase
BookCategory.FICTION, UserStatus.ACTIVE
```

### Python
```python
# Classes: PascalCase
class Borrower, Library, Librarian

# Méthodes: snake_case
borrow_book(), send_notification()

# Constantes: UPPER_SNAKE_CASE
MAX_BOOKS_PER_USER, DEFAULT_BORROWING_PERIOD
```

---

## 🔗 Liens Rapides

- [📘 Guide Méthodologique Complet](event-driven-library-system.md)
- [🏗️ Structure du Projet TypeScript](../README.md)
- [🤝 Guide de Contribution](../CONTRIBUTING.md)

---

*Documentation générée pour le projet Library Management System - Février 2026*
