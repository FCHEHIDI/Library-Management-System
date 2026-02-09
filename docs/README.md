# Système de Gestion de Bibliothèque

Implémentation professionnelle d'un système de gestion de bibliothèque en TypeScript, suivant les principes **OOP** et **SOLID**.

## 📁 Structure du Projet

```
OOP_SOLID/
├── src/
│   ├── enums/           # Énumérations (BookCategory, PhysicalState, etc.)
│   ├── interfaces/      # Interfaces (INotifiable, IBorrowable, IUser, ISearchable)
│   ├── types/           # Types TypeScript personnalisés
│   ├── models/          # Modèles de données (Book, BorrowingRecord, Comment, Notification)
│   ├── domains/         # Classes métier (Librarian, Borrower, Library)
│   ├── policies/        # Règles métier et constantes
│   └── index.ts         # Point d'entrée
├── tests/               # Tests unitaires et d'intégration
├── docs/                # Documentation
└── dist/                # Code compilé
```

## 🚀 Installation

```bash
npm install
```

## 🛠️ Scripts Disponibles

```bash
npm run build          # Compiler le projet
npm run dev            # Lancer en mode développement
npm test               # Lancer les tests
npm run test:watch     # Tests en mode watch
npm run test:coverage  # Rapport de couverture
npm run lint           # Linter le code
npm run format         # Formatter le code
```

## 📚 Concepts Implémentés

- ✅ **Single Responsibility Principle** (SRP)
- ✅ **Open/Closed Principle** (OCP)
- ✅ **Liskov Substitution Principle** (LSP)
- ✅ **Interface Segregation Principle** (ISP)
- ✅ **Dependency Inversion Principle** (DIP)

## 🎯 Fonctionnalités

- Gestion des livres (CRUD)
- Gestion des utilisateurs (emprunteurs et bibliothécaires)
- Système d'emprunts et de retours
- Prolongations d'emprunts
- Notifications automatiques
- Commentaires et évaluations
- Réclamations
- Statistiques

## 📖 Documentation

Voir le dossier `docs/` pour la documentation complète et la spécification du système.

## 🧪 Tests

Les tests couvrent :
- Tests unitaires pour chaque classe
- Tests d'intégration pour les workflows
- Validation des règles métier

## 📝 Licence

MIT
