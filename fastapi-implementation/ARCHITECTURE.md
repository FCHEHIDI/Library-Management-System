# 🏗️ Architecture SOLID en Python - Défis et Solutions

## Le Problème : Python n'a pas d'interfaces natives

Contrairement à TypeScript, Java ou C#, Python n'a **pas d'interfaces au niveau langage**.

```typescript
// TypeScript: interfaces natives
interface IRepository {
    findById(id: string): Promise<User | null>;
}

class UserRepository implements IRepository {
    async findById(id: string) { /* ... */ }
}
```

```python
# Python: pas de mot-clé "interface" ou "implements"
# ❌ Ceci n'existe PAS en Python ❌
# interface IRepository:
#     def find_by_id(id: str) -> User | None
```

---

## La Solution : ABC + Protocol

Nous utilisons **deux patterns** selon le niveau d'abstraction :

### 1️⃣ ABC (Abstract Base Classes) - Pour les Contrats Stricts

Utilisé pour **repositories** et **services** où l'implémentation doit **obligatoirement** respecter le contrat.

```python
from abc import ABC, abstractmethod
from typing import UUID

class IUserRepository(ABC):
    """Interface stricte pour le repository utilisateur.
    
    Toute classe concrète DOIT implémenter toutes les méthodes.
    """
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Récupère un utilisateur par son ID."""
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Crée un nouvel utilisateur."""
        pass
    
    @abstractmethod
    async def check_username_exists(self, username: str) -> bool:
        """Vérifie si un username est déjà pris."""
        pass
```

**Implémentation concrète** :

```python
class UserRepository(IUserRepository):
    """Implémentation SQLAlchemy de IUserRepository."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def check_username_exists(self, username: str) -> bool:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none() is not None
```

**Avantages** :
- ✅ MyPy peut valider que toutes les méthodes sont implémentées
- ✅ Erreur explicite si une méthode manque
- ✅ Documentation claire du contrat

**Inconvénient** :
- ❌ Obligation d'hériter explicitement (`class UserRepository(IUserRepository)`)
- ❌ Pas de duck typing

---

### 2️⃣ Protocol (Structural Subtyping) - Pour la Flexibilité

Utilisé pour **domains** où on veut du **duck typing** (si ça ressemble à un canard et ça cancane...).

```python
from typing import Protocol

class IBorrower(Protocol):
    """Interface flexible pour les opérations d'emprunteur.
    
    Toute classe avec ces méthodes est compatible (duck typing).
    """
    
    async def borrow_book(
        self,
        user_id: UUID,
        book_id: UUID,
        requested_period: int | None = None
    ) -> BorrowingRecord:
        """Emprunte un livre."""
        ...
    
    async def return_book(
        self,
        user_id: UUID,
        borrowing_id: UUID,
        condition: BookCondition
    ) -> BorrowingRecord:
        """Retourne un livre."""
        ...
    
    async def get_borrowing_history(
        self,
        user_id: UUID,
        limit: int = 10
    ) -> list[BorrowingRecord]:
        """Historique des emprunts."""
        ...
```

**Implémentation** (pas besoin d'hériter !) :

```python
class Borrower:
    """Domaine métier pour les opérations d'emprunteur.
    
    Compatible avec IBorrower SANS héritage explicite.
    """
    
    def __init__(
        self,
        user_repo: IUserRepository,
        book_repo: IBookRepository,
        borrowing_repo: IBorrowingRepository,
        notification_service: INotificationService,
        fee_calculator: IFeeCalculator
    ):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.borrowing_repo = borrowing_repo
        self.notification_service = notification_service
        self.fee_calculator = fee_calculator
    
    async def borrow_book(
        self,
        user_id: UUID,
        book_id: UUID,
        requested_period: int | None = None
    ) -> BorrowingRecord:
        # 1. Récupérer les entités
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")
        
        # 2. Validation métier
        if not user.can_borrow:
            raise ValueError(
                f"User cannot borrow: status={user.status}, "
                f"email_verified={user.email_verified}, "
                f"active_borrowings={user.active_borrowings_count}"
            )
        
        if not book.can_be_borrowed:
            raise ValueError(
                f"Book unavailable: category={book.category}, "
                f"status={book.status}, available={book.is_available}"
            )
        
        # 3. Déterminer la durée d'emprunt
        period_days = requested_period or BORROWING_POLICIES[book.category]["duration_days"]
        
        # 4. Créer l'emprunt
        borrowing = BorrowingRecord(
            id=uuid4(),
            user_id=user_id,
            book_id=book_id,
            borrow_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=period_days),
            status=BorrowingStatus.ACTIVE
        )
        
        # 5. Mettre à jour le livre
        book.is_available = False
        book.total_borrows += 1
        
        # 6. Mettre à jour le compteur utilisateur
        user.active_borrowings_count += 1
        
        # 7. Persister
        await self.borrowing_repo.create(borrowing)
        await self.book_repo.update(book)
        await self.user_repo.update(user)
        
        # 8. Notification
        await self.notification_service.send_notification(
            user_id=user_id,
            type=NotificationType.BORROWING_CREATED,
            title="Emprunt confirmé",
            message=f"Vous avez emprunté '{book.title}'. À retourner avant le {borrowing.due_date.strftime('%d/%m/%Y')}.",
            priority=NotificationPriority.NORMAL
        )
        
        return borrowing
    
    # ... autres méthodes ...
```

**Avantages** :
- ✅ Pas besoin d'hériter (duck typing)
- ✅ Plus Pythonique
- ✅ Testable avec des mocks simples

**Inconvénient** :
- ❌ MyPy validation moins stricte

---

## 📊 Choix d'Architecture

| Couche | Pattern Utilisé | Raison |
|--------|-----------------|--------|
| **Repositories** | ABC | Contrats stricts avec la DB |
| **Services** | ABC | Logique métier réutilisable |
| **Domains** | Protocol | Flexibilité + duck typing |

### Repositories (ABC)

```python
# app/interfaces/repositories.py
class IUserRepository(ABC):          # 10 méthodes abstraites
class IBookRepository(ABC):          # 13 méthodes abstraites
class IBorrowingRepository(ABC):     # 11 méthodes abstraites
class ICommentRepository(ABC):       # 10 méthodes abstraites
class INotificationRepository(ABC):  # 10 méthodes abstraites
```

**Total : 54 méthodes abstraites**

### Services (ABC)

```python
# app/interfaces/services.py
class INotificationService(ABC):     # 6 méthodes
class IFeeCalculator(ABC):           # 4 méthodes
class ISearchService(ABC):           # 5 méthodes
class IEmailService(ABC):            # 5 méthodes
```

**Total : 20 méthodes abstraites**

### Domains (Protocol)

```python
# app/interfaces/domains.py
class IBorrower(Protocol):           # 27 méthodes
class ILibrary(Protocol):            # 12 méthodes
class ILibrarian(Protocol):          # 33 méthodes
```

**Total : 72 méthodes (duck typing)**

---

## 🔄 Dependency Inversion Principle

Grâce aux interfaces, on peut **inverser les dépendances** :

```python
# ❌ MAUVAIS : Dépendance directe sur la DB
class Borrower:
    def __init__(self, db: AsyncSession):
        self.db = db  # Couplé à SQLAlchemy !

# ✅ BON : Dépendance sur l'abstraction
class Borrower:
    def __init__(
        self,
        user_repo: IUserRepository,      # Abstraction
        book_repo: IBookRepository,      # Abstraction
        borrowing_repo: IBorrowingRepository  # Abstraction
    ):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.borrowing_repo = borrowing_repo
```

**Bénéfices** :
- ✅ Testable avec des mocks
- ✅ On peut changer SQLAlchemy pour MongoDB sans toucher au domain
- ✅ Respect du SOLID (Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion)

---

## 🧪 Testabilité

Avec les interfaces, les tests deviennent triviaux :

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_borrow_book_success():
    # GIVEN: Mock repositories
    user_repo = Mock(spec=IUserRepository)
    book_repo = Mock(spec=IBookRepository)
    borrowing_repo = Mock(spec=IBorrowingRepository)
    notification_service = Mock(spec=INotificationService)
    fee_calculator = Mock(spec=IFeeCalculator)
    
    # Mock data
    user = User(id=uuid4(), status=UserStatus.ACTIVE, email_verified=True, active_borrowings_count=2)
    book = Book(id=uuid4(), category=BookCategory.GENERAL, status=BookStatus.AVAILABLE, is_available=True)
    
    user_repo.get_by_id = AsyncMock(return_value=user)
    book_repo.get_by_id = AsyncMock(return_value=book)
    borrowing_repo.create = AsyncMock()
    
    # WHEN: Borrow book
    borrower = Borrower(user_repo, book_repo, borrowing_repo, notification_service, fee_calculator)
    result = await borrower.borrow_book(user.id, book.id)
    
    # THEN: Assertions
    assert result.user_id == user.id
    assert result.book_id == book.id
    assert result.status == BorrowingStatus.ACTIVE
    assert book.is_available == False
    borrowing_repo.create.assert_called_once()
    notification_service.send_notification.assert_called_once()
```

---

## 📈 Métriques du Projet

```
Interfaces    : 146 méthodes abstraites
Repositories  : 1257 lignes (54 méthodes concrètes)
Services      : 1169 lignes (20 méthodes concrètes)
Domains       : 2776 lignes (72 méthodes concrètes)
Total Code    : ~6000 lignes

Placeholders  : 0
Tests Coverage: TODO (target >90%)
```

---

## 🎯 Conclusion

Python manque d'interfaces natives, **MAIS** :

1. **ABC** nous donne des contrats stricts (repositories, services)
2. **Protocol** nous donne du duck typing élégant (domains)
3. Les deux combinés = **SOLID** en Python !

**Next Steps** :
- [ ] Security layer (JWT, bcrypt)
- [ ] API endpoints (FastAPI routes)
- [ ] Tests (pytest avec mocks)
- [ ] CI/CD (GitHub Actions)
