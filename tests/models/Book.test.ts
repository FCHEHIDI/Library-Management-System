import { Book } from '../../src/models/Book.model';
import { BookCategory, PhysicalState, BorrowingStatus } from '../../src/enums';
import { BorrowingRecord } from '../../src/models';

describe('Book Model Tests', () => {
  test('Book is created with correct default values', () => {
    const book = new Book(
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

    expect(book.id).toBe('book-001');
    expect(book.title).toBe('Clean Code');
    expect(book.author).toBe('Robert C. Martin');
    expect(book.ISBN).toBe('978-0132350884');
    expect(book.category).toBe(BookCategory.TECHNOLOGY);
    expect(book.physicalState).toBe(PhysicalState.NEW);
    expect(book.pages).toBe(350);
    expect(book.publisher).toBe('Prentice Hall');
    expect(book.year).toBe(2008);
    expect(book.isAvailable).toBe(true);
    expect(book.isRestricted).toBe(false);
    expect(book.borrowingHistory).toEqual([]);
    expect(book.comments).toEqual([]);
    expect(book.rating).toBe(0);
    expect(book.lastModified).toBeInstanceOf(Date);
  });

  test('Book can be marked as unavailable', () => {
    const book = new Book(
      'book-001',
      'Test',
      'Author',
      'ISBN',
      BookCategory.FICTION,
      PhysicalState.GOOD,
      200,
      'Publisher',
      2020
    );

    expect(book.isAvailable).toBe(true);
    book.isAvailable = false;
    expect(book.isAvailable).toBe(false);
  });

  test('Book can be restricted', () => {
    const book = new Book(
      'book-001',
      'Test',
      'Author',
      'ISBN',
      BookCategory.FICTION,
      PhysicalState.GOOD,
      200,
      'Publisher',
      2020
    );

    expect(book.isRestricted).toBe(false);
    book.isRestricted = true;
    expect(book.isRestricted).toBe(true);
  });

  test('Book tracks borrowing history', () => {
    const book = new Book(
      'book-001',
      'Test',
      'Author',
      'ISBN',
      BookCategory.FICTION,
      PhysicalState.GOOD,
      200,
      'Publisher',
      2020
    );

    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date(Date.now() + 14 * 24 * 60 * 60 * 1000)
    );

    book.borrowingHistory.push(record);

    expect(book.borrowingHistory.length).toBe(1);
    expect(book.borrowingHistory[0]).toBe(record);
  });

  test('Book physical state can be updated', () => {
    const book = new Book(
      'book-001',
      'Test',
      'Author',
      'ISBN',
      BookCategory.FICTION,
      PhysicalState.NEW,
      200,
      'Publisher',
      2020
    );

    expect(book.physicalState).toBe(PhysicalState.NEW);

    book.physicalState = PhysicalState.WORN;
    expect(book.physicalState).toBe(PhysicalState.WORN);

    book.physicalState = PhysicalState.DAMAGED;
    expect(book.physicalState).toBe(PhysicalState.DAMAGED);
  });
});
