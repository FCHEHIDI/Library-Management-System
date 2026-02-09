import { UUID, Email, PhoneNumber, OpeningHours, UserData } from '../types';
import { Book, BorrowingRecord, Notification } from '../models';
import { BorrowingStatus } from '../enums';
import { Borrower } from './Borrower';
import { Librarian } from './Librarian';
import { TIME_POLICIES } from '../policies';
import { v4 as uuidv4 } from 'uuid';

export class Library {
  public readonly id: UUID;
  public name: string;
  public address: string;
  public phone: PhoneNumber;
  public email: Email;
  public openingHours: OpeningHours;
  public books: Map<UUID, Book>;
  public users: Map<UUID, Borrower>;
  public librarians: Map<UUID, Librarian>;
  public borrowingRecords: Map<UUID, BorrowingRecord>;
  public notifications: Map<UUID, Notification>;

  constructor(
    id: UUID,
    name: string,
    address: string,
    phone: PhoneNumber,
    email: Email,
    openingHours: OpeningHours
  ) {
    this.id = id;
    this.name = name;
    this.address = address;
    this.phone = phone;
    this.email = email;
    this.openingHours = openingHours;
    this.books = new Map();
    this.users = new Map();
    this.librarians = new Map();
    this.borrowingRecords = new Map();
    this.notifications = new Map();
  }

  addBook(book: Book): void {
    if (this.books.has(book.id)) throw new Error(`Book with ID ${book.id} already exists.`);
    this.books.set(book.id, book);
  }

  removeBook(bookId: UUID): void {
    if (!this.books.has(bookId)) throw new Error(`Book with ID ${bookId} not found.`);
    const book = this.books.get(bookId)!;
    if (!book.isAvailable) throw new Error('Cannot remove a book that is currently borrowed.');
    this.books.delete(bookId);
  }

  getBook(bookId: UUID): Book {
    const book = this.books.get(bookId);
    if (!book) throw new Error(`Book with ID ${bookId} not found.`);
    return book;
  }

  getAllBooks(): Book[] {
    return Array.from(this.books.values());
  }

  getAvailableBooks(): Book[] {
    return Array.from(this.books.values()).filter((book) => book.isAvailable && !book.isRestricted);
  }

  registerUser(userData: UserData): Borrower {
    const userId = uuidv4();
    const borrower = new Borrower(userId, userData.name, userData.firstname, userData.email, userData.phone, userData.address);
    this.users.set(userId, borrower);
    return borrower;
  }

  getUser(userId: UUID): Borrower {
    const user = this.users.get(userId);
    if (!user) throw new Error(`User with ID ${userId} not found.`);
    return user;
  }

  getAllUsers(): Borrower[] {
    return Array.from(this.users.values());
  }

  processBorrowing(bookId: UUID, borrowerId: UUID): BorrowingRecord {
    const book = this.getBook(bookId);
    const borrower = this.getUser(borrowerId);

    if (!book.isAvailable) throw new Error('Book is not available for borrowing.');
    if (book.isRestricted) throw new Error('Book is restricted and cannot be borrowed.');
    if (!borrower.isAuthorized) throw new Error('Borrower is not authorized to borrow books.');
    if (borrower.borrowedBooks.length >= borrower.maxBooksAllowed) throw new Error('Borrower has reached maximum books limit.');

    const borrowDate = new Date();
    const dueDate = this.calculateDueDate(borrowDate);
    const recordId = uuidv4();
    const record = new BorrowingRecord(recordId, bookId, borrowerId, borrowDate, dueDate);

    book.isAvailable = false;
    book.borrowingHistory.push(record);
    book.lastModified = new Date();

    borrower.borrowedBooks.push(bookId);
    borrower.borrowingHistory.push(record);

    this.borrowingRecords.set(recordId, record);
    return record;
  }

  processReturn(bookId: UUID, borrowerId: UUID): void {
    const book = this.getBook(bookId);
    const borrower = this.getUser(borrowerId);
    const activeRecord = Array.from(this.borrowingRecords.values()).find(
      (record) => record.bookId === bookId && record.borrowerId === borrowerId && record.status === BorrowingStatus.ACTIVE
    );

    if (!activeRecord) throw new Error('No active borrowing record found for this book and borrower.');

    activeRecord.returnDate = new Date();
    activeRecord.status = BorrowingStatus.RETURNED;
    book.isAvailable = true;
    book.lastModified = new Date();
    borrower.borrowedBooks = borrower.borrowedBooks.filter((id) => id !== bookId);
  }

  getOverdueBorrowings(): BorrowingRecord[] {
    const now = new Date();
    return Array.from(this.borrowingRecords.values()).filter(
      (record) => record.status === BorrowingStatus.ACTIVE && record.dueDate < now && !record.returnDate
    );
  }

  sendDueDateReminders(): void {
    const now = new Date();
    const reminderDays = TIME_POLICIES.REMINDER_DAYS_BEFORE_DUE as readonly number[];
    Array.from(this.borrowingRecords.values()).forEach((record) => {
      if (record.status !== BorrowingStatus.ACTIVE || record.returnDate) return;
      const daysUntilDue = Math.ceil((record.dueDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
      if (reminderDays.includes(daysUntilDue)) {
        console.log(`Reminder: Book due in ${daysUntilDue} days for borrower ${record.borrowerId}`);
      }
    });
  }

  private calculateDueDate(borrowDate: Date): Date {
    const dueDate = new Date(borrowDate);
    dueDate.setDate(dueDate.getDate() + TIME_POLICIES.DEFAULT_BORROWING_PERIOD);
    return dueDate;
  }
}
