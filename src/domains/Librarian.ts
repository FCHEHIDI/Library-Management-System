import { UUID, Email, PhoneNumber, DateTime, UserData, BookData, PartialUpdate, UserProfile } from '../types';
import { LibrarianRole, PhysicalState, NotificationType } from '../enums';
import { IUser, INotifiable } from '../interfaces';
import { Book, Notification, Comment } from '../models';

/**
 * Librarian class representing library staff members
 * Implements IUser and INotifiable interfaces
 */
export class Librarian implements IUser, INotifiable {
  public readonly id: UUID;
  public name: string;
  public firstname: string;
  public email: Email;
  public phone: PhoneNumber;
  public readonly hireDate: DateTime;
  public role: LibrarianRole;
  public isActiveStatus: boolean;
  public lastLogin: DateTime;

  constructor(
    id: UUID,
    name: string,
    firstname: string,
    email: Email,
    phone: PhoneNumber,
    role: LibrarianRole
  ) {
    this.id = id;
    this.name = name;
    this.firstname = firstname;
    this.email = email;
    this.phone = phone;
    this.hireDate = new Date();
    this.role = role;
    this.isActiveStatus = true;
    this.lastLogin = new Date();
  }

  // ==================== IUser Implementation ====================

  getProfile(): UserProfile {
    return {
      id: this.id,
      name: this.name,
      firstname: this.firstname,
      email: this.email,
      phone: this.phone,
      address: '',
      isActive: this.isActive(),
      lastLogin: this.lastLogin
    };
  }

  updateProfile(profileData: PartialUpdate<UserProfile>): void {
    if (profileData.name !== undefined) this.name = profileData.name;
    if (profileData.firstname !== undefined) this.firstname = profileData.firstname;
    if (profileData.email !== undefined) this.email = profileData.email;
    if (profileData.phone !== undefined) this.phone = profileData.phone;
  }

  isActive(): boolean {
    return this.isActive;
  }

  getId(): UUID {
    return this.id;
  }

  // ==================== INotifiable Implementation ====================

  sendNotification(recipientId: UUID, message: string, type: NotificationType): void {
    // Placeholder: Would use notification service
    console.log(`Notification sent to ${recipientId}: ${message}`);
  }

  sendEmail(recipientEmail: Email, subject: string, body: string): void {
    // Placeholder: Would use email service
    console.log(`Email sent to ${recipientEmail}`);
  }

  receiveNotification(): Notification[] {
    // Placeholder: Would query notifications for this librarian
    return [];
  }

  markNotificationAsRead(notificationId: UUID): void {
    // Placeholder: Would update notification read status
    console.log(`Notification ${notificationId} marked as read`);
  }

  // ==================== Book Management Methods ====================

  /**
   * Add a new book to the library catalog
   * Event: "le LIBRARIAN ajoute un nouveau livre au catalogue"
   */
  addBook(bookData: BookData): Book {
    if (!bookData.title || !bookData.author || !bookData.ISBN) {
      throw new Error('Book title, author, and ISBN are required.');
    }
    // Placeholder: Would call Library.addBook()
    console.log(`Book added: ${bookData.title}`);
    return {} as Book;
  }

  /**
   * Delete a book from the catalog
   */
  deleteBookById(bookId: UUID): void {
    // Placeholder: Would call Library.removeBook()
    console.log(`Book ${bookId} deleted.`);
  }

  /**
   * Update book information
   */
  updateBook(bookId: UUID, bookData: PartialUpdate<BookData>): Book {
    // Placeholder: Would update book in Library
    console.log(`Book ${bookId} updated.`);
    return {} as Book;
  }

  /**
   * Get a specific book by ID
   */
  getBookById(bookId: UUID): Book {
    // Placeholder: Would call Library.getBook()
    return {} as Book;
  }

  /**
   * Get all books in the catalog
   */
  getAllBooks(): Book[] {
    // Placeholder: Would call Library.getAllBooks()
    return [];
  }

  /**
   * Check if a book is available for borrowing
   */
  checkBookAvailability(bookId: UUID): boolean {
    // Placeholder: Would call Library.getBook() and check availability
    return false;
  }

  /**
   * Update the physical state of a book
   */
  updatePhysicalState(bookId: UUID, state: PhysicalState): void {
    // Placeholder: Would update book's physicalState
    console.log(`Book ${bookId} physical state updated to ${state}`);
  }

  /**
   * Set book availability status
   */
  setBookAvailability(bookId: UUID, isAvailable: boolean): void {
    // Placeholder: Would update book's isAvailable flag
    console.log(`Book ${bookId} availability set to ${isAvailable}`);
  }

  /**
   * Restrict a book from borrowing
   */
  restrictBook(bookId: UUID, reason: string): void {
    if (!reason || reason.trim().length === 0) {
      throw new Error('Restriction reason is required.');
    }
    console.log(`Book ${bookId} restricted. Reason: ${reason}`);
  }

  /**
   * Remove restriction from a book
   */
  unrestrictBook(bookId: UUID): void {
    console.log(`Book ${bookId} unrestricted.`);
  }

  // ==================== User Management Methods ====================

  /**
   * Register a new user in the system
   */
  addUser(userData: UserData): any {
    if (!userData.email || !userData.name) {
      throw new Error('User email and name are required.');
    }
    // Placeholder: Would call Library.registerUser()
    console.log(`User added: ${userData.name}`);
    return {};
  }

  /**
   * Get a specific user by ID
   */
  getUserById(userId: UUID): any {
    // Placeholder: Would call Library.getUser()
    return {};
  }

  /**
   * Get all registered users
   */
  getAllUsers(): any[] {
    // Placeholder: Would call Library.getAllUsers()
    return [];
  }

  /**
   * Delete a user account
   */
  deleteUser(userId: UUID): void {
    // Placeholder: Would verify no active borrowings then delete
    console.log(`User ${userId} deleted.`);
  }

  /**
   * Activate a user account
   */
  activateUser(userId: UUID): void {
    // Placeholder: Would update user status to active
    console.log(`User ${userId} activated.`);
  }

  /**
   * Deactivate a user account
   */
  deactivateUser(userId: UUID, reason: string): void {
    if (!reason || reason.trim().length === 0) {
      throw new Error('Deactivation reason is required.');
    }
    console.log(`User ${userId} deactivated. Reason: ${reason}`);
  }

  /**
   * Suspend a user account temporarily
   */
  suspendUser(userId: UUID, durationDays: number, reason: string): void {
    if (durationDays <= 0) {
      throw new Error('Suspension duration must be positive.');
    }
    if (!reason || reason.trim().length === 0) {
      throw new Error('Suspension reason is required.');
    }
    console.log(`User ${userId} suspended for ${durationDays} days. Reason: ${reason}`);
  }

  /**
   * Authorize a user to borrow books
   */
  authorizeUser(userId: UUID): void {
    console.log(`User ${userId} authorized.`);
  }

  /**
   * Revoke user's authorization to borrow
   */
  revokeUserAuthorization(userId: UUID): void {
    console.log(`User ${userId} authorization revoked.`);
  }

  // ==================== Communication Methods ====================

  /**
   * Send an email to a specific user
   */
  sendEmailToUser(userId: UUID, subject: string, body: string): void {
    if (!subject || !body) {
      throw new Error('Email subject and body are required.');
    }
    // Placeholder: Would get user email and send via email service
    console.log(`Email sent to user ${userId}: ${subject}`);
  }

  /**
   * Send an email to administrators
   */
  sendEmailToAdmin(subject: string, body: string): void {
    if (!subject || !body) {
      throw new Error('Email subject and body are required.');
    }
    console.log(`Email sent to admin: ${subject}`);
  }

  /**
   * Post general information/announcement to all users
   */
  postGeneralInfo(message: string): void {
    if (!message || message.trim().length === 0) {
      throw new Error('Message is required.');
    }
    console.log(`General info posted: ${message}`);
  }

  // ==================== Comments Management Methods ====================

  /**
   * Approve a pending comment/review
   */
  approveComment(commentId: UUID): void {
    // Placeholder: Would update comment approved status
    console.log(`Comment ${commentId} approved.`);
  }

  /**
   * Reject a pending comment/review
   */
  rejectComment(commentId: UUID): void {
    // Placeholder: Would update comment to rejected
    console.log(`Comment ${commentId} rejected.`);
  }

  /**
   * Get all pending comments awaiting approval
   */
  getPendingComments(): Comment[] {
    // Placeholder: Would query comments where approved = false
    return [];
  }
}
