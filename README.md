<div align="center">

# Library Management System

  <img src="assets\OOP_library_Palatino.png" alt="Bibliothèque Impériale - Monte Palatino Style" width="100%" style="max-width: 900px; border-radius: 8px; opacity: 0.95; margin: 20px 0;" />
  
  <p style="margin-top: 15px;"><i>Event-Driven Library Management System built with TypeScript<br/>following <b>SOLID principles</b> and <b>Event-Driven Design</b>.</i></p>
</div>

---

## 🎯 Architecture Overview

This project implements a complete library management system using an **event-driven methodology** where each business event maps directly to a public method, providing clear API contracts and maintainable code structure.

### Core Principles
- **Event-Driven Design**: 140+ catalogued events drive the API design
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Type Safety**: Full TypeScript with strict mode
- **Test Coverage**: Comprehensive Jest test suites for all components

## 📦 Project Structure

```
src/
├── enums/           # 11 enumerations (BookCategory, BorrowingStatus, etc.)
├── interfaces/      # 4 core interfaces (IUser, INotifiable, ISearchable, IBorrowable)
├── types/           # Type definitions and DTOs
├── models/          # 4 data models (Book, BorrowingRecord, Comment, Notification)
├── domains/         # 3 domain classes (Borrower, Library, Librarian)
└── policies/        # Business rules and validation policies (100+ constants)

tests/
├── domains/         # Domain class tests
├── models/          # Model tests
└── policies/        # Business rules tests
```

## 🏗️ Domain Classes

### Borrower (27 public methods + 2 private)
Represents library users who borrow books.
- **Implements**: `IUser`, `INotifiable`, `ISearchable`
- **Key Features**: Book borrowing, comments/reviews, claims management, notifications

### Library (12 methods)
Central system orchestrator managing all library operations.
- **Key Features**: Book catalog management, user registration, borrowing transactions, overdue tracking

### Librarian (33 methods)
Library staff with administrative capabilities.
- **Implements**: `IUser`, `INotifiable`
- **Key Features**: Book/user management, comment moderation, claims processing, analytics

## 🎨 Business Policies

8 policy categories with 100+ configurable constants:
- **BORROWING_POLICIES**: Max books per user (3), extension limits
- **TIME_POLICIES**: Borrowing period (14 days), reminder schedule
- **FEE_POLICIES**: Late fees (€0.50/day), damage fees
- **ACCESS_POLICIES**: Age restrictions, role permissions
- **VALIDATION_POLICIES**: Input validation rules
- **ANALYTICS_POLICIES**: Reporting thresholds
- **WORKFLOW_POLICIES**: Automation rules
- **CATEGORIZATION_POLICIES**: Content organization

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint
```

## 🧪 Testing

Comprehensive test suites covering:
- **Domain Logic**: Borrower, Library, Librarian workflows
- **Models**: Book, BorrowingRecord, Comment, Notification
- **Policies**: Business rules validation
- **Integration**: Complete borrowing workflows

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- Borrower.test.ts

# Watch mode
npm test -- --watch
```

## 📝 Event-Driven Methodology

Each public method corresponds to a business event from the original specification:

```typescript
/**
 * Borrow a book from the library
 * Event: "le USER emprunte un livre"
 */
borrowBook(bookId: UUID): BorrowingRecord {
  // Validation using policies
  if (!bookId) throw new Error('Book ID is required.');
  if (this.borrowedBooks.length >= BORROWING_POLICIES.MAX_BOOKS_PER_USER) {
    throw new Error('Maximum books limit reached.');
  }
  // Business logic...
}
```

## 🛠️ Development

### Code Style
- **TypeScript**: Strict mode enabled
- **ESLint**: Configured for TypeScript
- **Prettier**: Code formatting
- **Path Aliases**: `@models`, `@interfaces`, `@enums`, etc.

### Adding New Features
1. Define the event in your catalog
2. Create the corresponding public method
3. Add validation using business policies
4. Write comprehensive tests
5. Update documentation

## 📊 Code Quality

- **Type Safety**: 100% TypeScript with strict checks
- **Linting**: ESLint with TypeScript rules
- **Testing**: Jest with ts-jest
- **Coverage**: Comprehensive test coverage across all layers

## 🔄 Future Enhancements

- [ ] Implement concrete service integrations (NotificationService, EmailService, SearchService)
- [ ] Add database persistence layer
- [ ] Create REST API with Express/Fastify
- [ ] Build admin dashboard
- [ ] Add real-time notifications (WebSocket)
- [ ] Implement Python/FastAPI version

## 📄 License

MIT

## 👥 Contributing

Contributions welcome! Please follow the event-driven methodology and ensure:
- All new features have corresponding events
- Comprehensive tests are included
- SOLID principles are respected
- TypeScript strict mode passes

## 🙏 Acknowledgments

Built with a "civilized" approach to software design - like writing a sonnet, where discipline within structure creates elegant, maintainable code.
