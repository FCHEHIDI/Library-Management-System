import { BorrowingRecord } from '../../src/models/BorrowingRecord.model';
import { BorrowingStatus, ExtensionStatus } from '../../src/enums';

describe('BorrowingRecord Model Tests', () => {
  test('BorrowingRecord is created with correct initial values', () => {
    const borrowDate = new Date('2024-01-01');
    const dueDate = new Date('2024-01-15');

    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      borrowDate,
      dueDate
    );

    expect(record.id).toBe('record-001');
    expect(record.bookId).toBe('book-001');
    expect(record.borrowerId).toBe('user-001');
    expect(record.borrowDate).toBe(borrowDate);
    expect(record.dueDate).toBe(dueDate);
    expect(record.status).toBe(BorrowingStatus.ACTIVE);
    expect(record.returnDate).toBeNull();
    expect(record.extensionRequested).toBe(false);
    expect(record.extensionStatus).toBe(ExtensionStatus.NOT_REQUESTED);
  });

  test('BorrowingRecord can be marked as returned', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    expect(record.status).toBe(BorrowingStatus.ACTIVE);
    expect(record.returnDate).toBeNull();

    const returnDate = new Date();
    record.returnDate = returnDate;
    record.status = BorrowingStatus.RETURNED;

    expect(record.status).toBe(BorrowingStatus.RETURNED);
    expect(record.returnDate).toBe(returnDate);
  });

  test('BorrowingRecord can track extension request', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    expect(record.extensionRequested).toBe(false);
    expect(record.extensionStatus).toBe(ExtensionStatus.NOT_REQUESTED);

    record.extensionRequested = true;
    record.extensionStatus = ExtensionStatus.PENDING;

    expect(record.extensionRequested).toBe(true);
    expect(record.extensionStatus).toBe(ExtensionStatus.PENDING);
  });

  test('BorrowingRecord can be marked as overdue', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    record.status = BorrowingStatus.OVERDUE;

    expect(record.status).toBe(BorrowingStatus.OVERDUE);
  });

  test('BorrowingRecord can be cancelled', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    record.status = BorrowingStatus.CANCELLED;

    expect(record.status).toBe(BorrowingStatus.CANCELLED);
  });

  test('Extension can be approved', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    record.extensionRequested = true;
    record.extensionStatus = ExtensionStatus.APPROVED;

    expect(record.extensionStatus).toBe(ExtensionStatus.APPROVED);
  });

  test('Extension can be rejected', () => {
    const record = new BorrowingRecord(
      'record-001',
      'book-001',
      'user-001',
      new Date(),
      new Date()
    );

    record.extensionRequested = true;
    record.extensionStatus = ExtensionStatus.REJECTED;

    expect(record.extensionStatus).toBe(ExtensionStatus.REJECTED);
  });
});
