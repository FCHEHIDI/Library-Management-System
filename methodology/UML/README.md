# 🎨 Diagrammes UML - Library Management System

[← Retour à l'index](../README.md)

---

## 📊 Index des Diagrammes

### Diagrammes de Structure
1. **[Class Diagram](01-class-diagram.md)** - Diagramme de classes complet
2. **[Entity-Relationship Diagram](02-er-diagram.md)** - Relations entre entités

### Diagrammes de Comportement
3. **[Borrowing Sequence](03-borrowing-sequence.md)** - Workflow d'emprunt
4. **[Return Sequence](04-return-sequence.md)** - Workflow de retour
5. **[Notification Flow](05-notification-flow.md)** - Système de notifications

### Diagrammes d'État
6. **[Borrowing State Diagram](06-borrowing-states.md)** - États d'un emprunt
7. **[User Status State Diagram](07-user-status-states.md)** - États d'un utilisateur

### Diagrammes d'Architecture
8. **[System Architecture](08-architecture.md)** - Vue d'ensemble système

---

## 🔧 Technologies

Tous les diagrammes utilisent **Mermaid** pour :
- ✅ Rendu natif dans GitHub/GitLab
- ✅ Versioning avec Git
- ✅ Édition en texte simple
- ✅ Intégration VS Code

---

## 📖 Comment Lire les Diagrammes

### Légende Générale

#### Diagrammes de Classes
```
┌─────────────┐
│  ClassName  │  ← Nom de la classe
├─────────────┤
│ -attribute  │  ← - = private, + = public, # = protected
├─────────────┤
│ +method()   │  ← Méthodes
└─────────────┘
```

**Relations**:
- `──────>` : Association
- `──────▷` : Héritage / Implémentation
- `- - - ->` : Dépendance
- `◇──────` : Agrégation
- `◆──────` : Composition

#### Diagrammes de Séquence
```
Actor → Object: message    ← Appel synchrone
Actor -->> Object: message ← Retour
Actor ->> Object: message  ← Appel asynchrone
```

#### Diagrammes d'État
```
[*] → State1     ← État initial
State1 → State2  ← Transition
State2 → [*]     ← État final
```

---

## 🎯 Guide de Navigation

### Pour Comprendre la Structure
1. Commencez par [Class Diagram](01-class-diagram.md)
2. Consultez [ER Diagram](02-er-diagram.md) pour les relations

### Pour Comprendre les Workflows
1. [Borrowing Sequence](03-borrowing-sequence.md) - Comment emprunter
2. [Return Sequence](04-return-sequence.md) - Comment retourner
3. [Notification Flow](05-notification-flow.md) - Communication

### Pour Comprendre les États
1. [Borrowing States](06-borrowing-states.md) - Lifecycle d'un emprunt
2. [User Status States](07-user-status-states.md) - Lifecycle utilisateur

### Pour Comprendre l'Architecture
1. [System Architecture](08-architecture.md) - Vue globale
2. [Component Diagram](09-components.md) - Découpage technique

---

## 📊 Statistiques

| Type de Diagramme | Quantité | Complexité |
|-------------------|----------|------------|
| Structure | 2 | ⭐⭐⭐ |
| Comportement | 3 | ⭐⭐⭐⭐ |
| État | 2 | ⭐⭐ |
| Architecture | 2 | ⭐⭐⭐ |
| **TOTAL** | **9** | |

---

## 🔗 Liens Rapides

- [Documentation Technique](../README.md)
- [Guide Méthodologique](../event-driven-library-system.md)
- [Projet TypeScript](../../README.md)

---

*Diagrammes générés avec Mermaid - Library Management System - Février 2026*
