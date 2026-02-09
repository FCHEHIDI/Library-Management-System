# Contributing to Library Management System

Thank you for your interest in contributing! This project follows an **event-driven design methodology** and **SOLID principles**.

## 🎯 Core Philosophy

Every public method corresponds to a business event from our event catalog. This creates:
- **Clear API contracts**: Event names become method signatures
- **Maintainable code**: Each method has a single, well-defined responsibility
- **Testable architecture**: One event = one test
- **Self-documenting**: Method names directly reflect business requirements

## 📝 How to Contribute

### 1. Find or Create an Event

Before adding any functionality:
1. Check the event catalog in `1-bibliothèque-solution.md`
2. If your feature isn't listed, propose it as a new event
3. Get consensus on the event definition

### 2. Follow the Method Template

```typescript
/**
 * [Brief description]
 * Event: "[exact event text from catalog]"
 * 
 * @param paramName - Description
 * @returns Description
 * @throws Error description
 */
methodName(param: Type): ReturnType {
  // 1. Validate inputs using VALIDATION_POLICIES
  if (!param) throw new Error('Clear, user-friendly message');
  
  // 2. Check business rules using relevant POLICIES
  if (condition) throw new Error('Business rule violation message');
  
  // 3. Execute business logic
  // ...
  
  // 4. Return result or log placeholder
  return result;
}
```

### 3. Write Tests First

For each new method:

```typescript
describe('ClassName - Feature', () => {
  test('Event: [event text] - [what it does]', () => {
    // Arrange
    const instance = new ClassName(...);
    
    // Act & Assert
    expect(instance.methodName(validInput)).toBe(expected);
  });
  
  test('Event: [event text] - [validation rule]', () => {
    expect(() => instance.methodName(invalidInput)).toThrow('expected message');
  });
});
```

### 4. Use Business Policies

Never hardcode business rules:

```typescript
// ❌ Bad
if (books.length > 3) throw new Error('Too many books');

// ✅ Good
if (books.length >= BORROWING_POLICIES.MAX_BOOKS_PER_USER) {
  throw new Error('Maximum books limit reached.');
}
```

### 5. Follow SOLID Principles

- **S**ingle Responsibility: One event = one method = one responsibility
- **O**pen/Closed: Extend via new events, don't modify existing ones
- **L**iskov Substitution: Implementations must honor interface contracts
- **I**nterface Segregation: Use specific interfaces (IUser, INotifiable, etc.)
- **D**ependency Inversion: Depend on abstractions, use dependency injection

## 🏗️ Code Structure

### Public vs Private Methods

- **Public**: Corresponds to an event in the catalog
- **Private**: Helper methods (e.g., `canBorrow()`, `calculateDueDate()`)

### Naming Conventions

- **Classes**: PascalCase (`Borrower`, `Library`)
- **Methods**: camelCase (`borrowBook`, `sendNotification`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_BOOKS_PER_USER`)
- **Interfaces**: IPascalCase (`IUser`, `INotifiable`)
- **Enums**: PascalCase with PascalCase values (`BookCategory.FICTION`)

### File Organization

```
src/
├── enums/          # Enumerations (one per file)
├── interfaces/     # Interface definitions
├── types/          # Type aliases and DTOs
├── models/         # Data models with constructors
├── domains/        # Business logic classes
└── policies/       # Business rules (readonly objects)
```

## ✅ Checklist Before PR

- [ ] Event is documented in catalog
- [ ] Method has JSDoc with event reference
- [ ] All inputs are validated
- [ ] Business rules use POLICIES constants
- [ ] Errors have clear, user-friendly messages
- [ ] Tests cover happy path and edge cases
- [ ] TypeScript compiles without errors (`npm run build`)
- [ ] All tests pass (`npm test`)
- [ ] Code is linted (`npm run lint`)
- [ ] No sensitive data or credentials in code

## 🧪 Testing Guidelines

### Test Organization

- Group tests by feature/interface
- Use descriptive test names with event references
- Test both success and failure scenarios
- Include integration tests for workflows

### Coverage Goals

- **Domains**: >90% coverage
- **Models**: 100% coverage
- **Policies**: 100% coverage

## 🚀 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/event-name

# 2. Install dependencies
npm install

# 3. Make changes following guidelines above

# 4. Run tests
npm test

# 5. Build
npm run build

# 6. Lint
npm run lint

# 7. Commit with conventional commits
git commit -m "feat: add [event name] implementation"

# 8. Push and create PR
git push origin feature/event-name
```

## 📚 Resources

- [Event Catalog](1-bibliothèque-solution.md)
- [Business Rules](src/policies/business-rules.ts)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## ❓ Questions?

Open an issue with the label `question` and we'll help you get started!

---

**Remember**: We're writing code like a sonnet - discipline within structure creates elegance. Every event is a verse, every method a line, and together they form a maintainable, beautiful system. 🎭
