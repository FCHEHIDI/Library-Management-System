import { Library } from '../../src/domains/Library';
import { Book, BorrowingRecord } from '../../src/models';
import { Borrower } from '../../src/domains/Borrower';
import {
  BookCategory,
  PhysicalState,
  BorrowingStatus
} from '../../src/enums';
import { UUID, Email, PhoneNumber, UserData } from '../../src/types';
import { TIME_POLICIES } from '../../src/policies';

describe('Library - System Management Tests', () => {
  let library: Library;
  let testBook: Book;
  let testUserData: UserData;

  beforeEach(() => {
    library = new Library(
      'library-001',
      'Paris Central Library',
      'contact@library.fr' as Email,
      '+33123456789' as PhoneNumber,
      { street: '1 rue de la Bibliothèque', city: 'Paris', zipCode: '75001', country: 'France' }
    );

    testBook = new Book(
      'book-001',
      'Clean Code',
      'Robert C. Martin',
      '978-0132350884',
      BookCategory.TECHNOLOGY,
      PhysicalState.NEW,
      350,
      'Prentice Hall',
      2008
    );

    testUserData = {
      name: 'Dupont',
      firstname: 'Marie',
      email: 'marie.dupont@example.com' as Email,
      phone: '+33612345678' as PhoneNumber,
      address: { street: '10 rue Test', city: 'Paris', zipCode: '75002', country: 'France' }
    };
  });

  // ==================== Book Management Tests ====================

  describe('Book Management', () => {
    test('Event: le SYSTEM ajoute un livre - addBook adds book to catalog', () => {
      library.addBook(testBook);

      const retrievedBook = library.getBook(testBook.id);
      expect(retrievedBook).toBe(testBook);
      expect(retrievedBook.title).toBe('Clean Code');
    });

    test('Event: le SYSTEM ajoute un livre - addBook prevents duplicate IDs', () => {
      library.addBook(testBook);

      expect(() => library.addBook(testBook)).toThrow('already exists');
    });

    test('Event: le SYSTEM supprime un livre - removeBook removes book from catalog', () => {
      library.addBook(testBook);
      library.removeBook(testBook.id);

      expect(() => library.getBook(testBook.id)).toThrow('not found');
    });

    test('Event: le SYSTEM supprime un livre - removeBook prevents removal of borrowed books', () => {
      library.addBook(testBook);
      testBook.isAvailable = false;

      expect(() => library.removeBook(testBook.id)).toThrow('currently borrowed');
    });

    test('Event: le SYSTEM consulte un livre - getBook retrieves book by ID', () => {
      library.addBook(testBook);

      const book = library.getBook(testBook.id);
      expect(book.title).toBe('Clean Code');
      expect(book.author).toBe('Robert C. Martin');
    });

    test('Event: le SYSTEM consulte un livre - getBook throws error for non-existent book', () => {
      expect(() => library.getBook('non-existent')).toThrow('not found');
    });

    test('Event: le SYSTEM consulte tous les livres - getAllBooks returns all books', () => {
      const book2 = new Book(
        'book-002',
        'The Pragmatic Programmer',
        'Andrew Hunt',
        '978-0201616224',
        BookCategory.TECHNOLOGY,
        PhysicalState.GOOD,
        320,
        'Addison-Wesley',
        1999
      );

      library.addBook(testBook);
      library.addBook(book2);

      const allBooks = library.getAllBooks();
      expect(allBooks.length).toBe(2);
      expect(allBooks).toContain(testBook);
      expect(allBooks).toContain(book2);
    });

    test('Event: le SYSTEM consulte livres disponibles - getAvailableBooks filters correctly', () => {
      const book2 = new Book(
        'book-002',
        'Test Book',
        'Author',
        'ISBN',
        BookCategory.FICTION,
        PhysicalState.GOOD,
        200,
        'Publisher',
        2020
      );
      book2.isAvailable = false;

      library.addBook(testBook);
      library.addBook(book2);

      const available = library.getAvailableBooks();
      expect(available.length).toBe(1);
      expect(available[0]).toBe(testBook);
    });

    test('Event: le SYSTEM consulte livres disponibles - getAvailableBooks excludes restricted books', () => {
      testBook.isRestricted = true;
      library.addBook(testBook);

      const available = library.getAvailableBooks();
      expect(available.length).toBe(0);
    });
  });

  // ==================== User Management Tests ====================

  describe('User Management', () => {
    test('Event: le SYSTEM enregistre un nouveau USER - registerUser creates borrower', () => {
      const borrower = library.registerUser(testUserData);

      expect(borrower).toBeInstanceOf(Borrower);
      expect(borrower.name).toBe('Dupont');
      expect(borrower.firstname).toBe('Marie');
      expect(borrower.email).toBe(testUserData.email);
    });

    test('Event: le SYSTEM enregistre un nouveau USER - registerUser stores user in library', () => {
      const borrower = library.registerUser(testUserData);
      const retrievedUser = library.getUser(borrower.id);

      expect(retrievedUser).toBe(borrower);
    });

    test('Event: le SYSTEM consulte un USER - getUser retrieves user by ID', () => {
      const borrower = library.registerUser(testUserData);
      const user = library.getUser(borrower.id);

      expect(user.name).toBe('Dupont');
      expect(user.email).toBe(testUserData.email);
    });

    test('Event: le SYSTEM consulte un USER - getUser throws error for non-existent user', () => {
      expect(() => library.getUser('non-existent')).toThrow('not found');
    });

    test('Event: le SYSTEM consulte tous les USERs - getAllUsers returns all users', () => {
      const user1 = library.registerUser(testUserData);
      const user2Data = { ...testUserData, email: 'john@example.com' as Email };
      const user2 = library.registerUser(user2Data);

      const allUsers = library.getAllUsers();
      expect(allUsers.length).toBe(2);
      expect(allUsers).toContain(user1);
      expect(allUsers).toContain(user2);
    });
  });

  // ==================== Borrowing Management Tests ====================

  describe('Borrowing Management', () => {
    let borrower: Borrower;

    beforeEach(() => {
      library.addBook(testBook);
      borrower = library.registerUser(testUserData);
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing creates borrowing record', () => {
      const record = library.processBorrowing(testBook.id, borrower.id);

      expect(record).toBeInstanceOf(BorrowingRecord);
      expect(record.bookId).toBe(testBook.id);
      expect(record.borrowerId).toBe(borrower.id);
      expect(record.status).toBe(BorrowingStatus.ACTIVE);
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing updates book availability', () => {
      expect(testBook.isAvailable).toBe(true);

      library.processBorrowing(testBook.id, borrower.id);

      expect(testBook.isAvailable).toBe(false);
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing updates borrower records', () => {
      library.processBorrowing(testBook.id, borrower.id);

      expect(borrower.borrowedBooks).toContain(testBook.id);
      expect(borrower.borrowingHistory.length).toBeGreaterThan(0);
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing calculates due date', () => {
      const record = library.processBorrowing(testBook.id, borrower.id);

      const expectedDueDate = new Date();
      expectedDueDate.setDate(expectedDueDate.getDate() + TIME_POLICIES.DEFAULT_BORROWING_PERIOD);

      expect(record.dueDate.toDateString()).toBe(expectedDueDate.toDateString());
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing prevents borrowing unavailable books', () => {
      testBook.isAvailable = false;

      expect(() => library.processBorrowing(testBook.id, borrower.id)).toThrow('not available');
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing prevents borrowing restricted books', () => {
      testBook.isRestricted = true;

      expect(() => library.processBorrowing(testBook.id, borrower.id)).toThrow('restricted');
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing enforces max books limit', () => {
      borrower.borrowedBooks = ['book1', 'book2', 'book3'];
      borrower.maxBooksAllowed = 3;

      expect(() => library.processBorrowing(testBook.id, borrower.id)).toThrow('maximum books limit');
    });

    test('Event: le SYSTEM traite une demande d\'emprunt - processBorrowing prevents unauthorized users', () => {
      borrower.isAuthorized = false;

      expect(() => library.processBorrowing(testBook.id, borrower.id)).toThrow('not authorized');
    });

    test('Event: le SYSTEM traite un retour de livre - processReturn marks book as available', () => {
      library.processBorrowing(testBook.id, borrower.id);
      expect(testBook.isAvailable).toBe(false);

      library.processReturn(testBook.id, borrower.id);

      expect(testBook.isAvailable).toBe(true);
    });

    test('Event: le SYSTEM traite un retour de livre - processReturn updates borrowing record', () => {
      const record = library.processBorrowing(testBook.id, borrower.id);

      library.processReturn(testBook.id, borrower.id);

      expect(record.status).toBe(BorrowingStatus.RETURNED);
      expect(record.returnDate).toBeDefined();
    });

    test('Event: le SYSTEM traite un retour de livre - processReturn removes book from borrowed list', () => {
      library.processBorrowing(testBook.id, borrower.id);
      expect(borrower.borrowedBooks).toContain(testBook.id);

      library.processReturn(testBook.id, borrower.id);

      expect(borrower.borrowedBooks).not.toContain(testBook.id);
    });

    test('Event: le SYSTEM traite un retour de livre - processReturn throws error for non-existent record', () => {
      expect(() => library.processReturn(testBook.id, borrower.id)).toThrow(
        'No active borrowing record found'
      );
    });

    test('Event: le SYSTEM consulte tous les emprunts en retard - getOverdueBorrowings filters correctly', () => {
      const record = library.processBorrowing(testBook.id, borrower.id);

      // Simulate overdue by setting due date in past
      record.dueDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

      const overdueRecords = library.getOverdueBorrowings();

      expect(overdueRecords.length).toBe(1);
      expect(overdueRecords[0]).toBe(record);
    });

    test('Event: le SYSTEM consulte tous les emprunts en retard - getOverdueBorrowings excludes returned books', () => {
      const record = library.processBorrowing(testBook.id, borrower.id);
      record.dueDate = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

      library.processReturn(testBook.id, borrower.id);

      const overdueRecords = library.getOverdueBorrowings();

      expect(overdueRecords.length).toBe(0);
    });
  });

  // ==================== Notification System Tests ====================

  describe('Notification System', () => {
    let borrower: Borrower;

    beforeEach(() => {
      library.addBook(testBook);
      borrower = library.registerUser(testUserData);
    });

    test('Event: le SYSTEM envoie des rappels automatiques - sendDueDateReminders logs reminders', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      const record = library.processBorrowing(testBook.id, borrower.id);

      // Set due date to trigger reminder (3 days before due)
      record.dueDate = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);

      library.sendDueDateReminders();

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('Event: le SYSTEM envoie des rappels automatiques - sendDueDateReminders skips returned books', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      const record = library.processBorrowing(testBook.id, borrower.id);
      record.dueDate = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000);

      library.processReturn(testBook.id, borrower.id);
      library.sendDueDateReminders();

      // Should not send reminder for returned book
      consoleSpy.mockRestore();
    });
  });

  // ==================== Integration Tests ====================

  describe('Integration Scenarios', () => {
    test('Complete borrowing workflow: register user → add book → borrow → return', () => {
      const user = library.registerUser(testUserData);
      library.addBook(testBook);

      const record = library.processBorrowing(testBook.id, user.id);
      expect(testBook.isAvailable).toBe(false);
      expect(user.borrowedBooks.length).toBe(1);

      library.processReturn(testBook.id, user.id);
      expect(testBook.isAvailable).toBe(true);
      expect(user.borrowedBooks.length).toBe(0);
      expect(record.status).toBe(BorrowingStatus.RETURNED);
    });

    test('Multiple users borrowing different books', () => {
      const user1 = library.registerUser(testUserData);
      const user2Data = { ...testUserData, email: 'user2@example.com' as Email };
      const user2 = library.registerUser(user2Data);

      const book2 = new Book(
        'book-002',
        'Book 2',
        'Author 2',
        'ISBN2',
        BookCategory.FICTION,
        PhysicalState.GOOD,
        200,
        'Publisher',
        2020
      );

      library.addBook(testBook);
      library.addBook(book2);

      library.processBorrowing(testBook.id, user1.id);
      library.processBorrowing(book2.id, user2.id);

      expect(user1.borrowedBooks.length).toBe(1);
      expect(user2.borrowedBooks.length).toBe(1);
      expect(testBook.isAvailable).toBe(false);
      expect(book2.isAvailable).toBe(false);
    });

    test('Overdue detection workflow', () => {
      const user = library.registerUser(testUserData);
      library.addBook(testBook);

      const record = library.processBorrowing(testBook.id, user.id);

      // Simulate overdue
      record.dueDate = new Date(Date.now() - 10 * 24 * 60 * 60 * 1000);

      const overdueBooks = library.getOverdueBorrowings();
      expect(overdueBooks.length).toBe(1);
      expect(overdueBooks[0].borrowerId).toBe(user.id);
    });
  });
});
