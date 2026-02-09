import {
  UUID,
  Email,
  PhoneNumber,
  DateTime,
  UserProfile,
  PartialUpdate,
  SearchCriteria
} from '../types';
import { NotificationType } from '../enums';
import { IUser, INotifiable, ISearchable } from '../interfaces';
import { Book, Notification, Comment, BorrowingRecord } from '../models';

/**
 * Borrower class representing library users who can borrow books
 * Implements IUser, INotifiable, and ISearchable interfaces
 */
export class Borrower implements IUser, INotifiable, ISearchable {
  public readonly id: UUID;
  public name: string;
  public firstname: string;
  public email: Email;
  public phone: PhoneNumber;
  public address: string;
  public readonly registrationDate: DateTime;
  public isAuthorized: boolean;
  public isActiveStatus: boolean;
  public suspensionEndDate: DateTime | null;
  public borrowedBooks: UUID[];
  public borrowingHistory: BorrowingRecord[];
  public maxBooksAllowed: number;
  public notificationsEnabled: boolean;
  public lastLogin: DateTime;

  constructor(
    id: UUID,
    name: string,
    firstname: string,
    email: Email,
    phone: PhoneNumber,
    address: string
  ) {
    this.id = id;
    this.name = name;
    this.firstname = firstname;
    this.email = email;
    this.phone = phone;
    this.address = address;
    this.registrationDate = new Date();
    this.isAuthorized = false;
    this.isActiveStatus = true;
    this.suspensionEndDate = null;
    this.borrowedBooks = [];
    this.borrowingHistory = [];
    this.maxBooksAllowed = 3;
    this.notificationsEnabled = true;
    this.lastLogin = new Date();
  }

  // ==================== IUser Implementation ====================

  /**
   * Get the borrower's profile
   */
  getProfile(): UserProfile {
    return {
      id: this.id,
      name: this.name,
      firstname: this.firstname,
      email: this.email,
      phone: this.phone,
      address: this.address,
      isActive: this.isActive(),
      lastLogin: this.lastLogin,
    };
  }

  /**
   * Update the borrower's profile with partial data
   */
  updateProfile(profileData: PartialUpdate<UserProfile>): void {
    if (profileData.name !== undefined) this.name = profileData.name;
    if (profileData.firstname !== undefined) this.firstname = profileData.firstname;
    if (profileData.email !== undefined) this.email = profileData.email;
    if (profileData.phone !== undefined) this.phone = profileData.phone;
    if (profileData.address !== undefined) this.address = profileData.address;
  }

  /**
   * Check if the borrower account is active
   */
  isActive(): boolean {
    return this.isActiveStatus && this.isAuthorized && !this.isSuspended();
  }

  /**
   * Get the borrower's unique identifier
   */
  getId(): UUID {
    return this.id;
  }

  // ==================== Private Helper Methods ====================

  /**
   * Check if the borrower is currently suspended
   */
  private isSuspended(): boolean {
    if (!this.suspensionEndDate) return false;
    return new Date() < this.suspensionEndDate;
  }

  // ==================== INotifiable Implementation ====================

  /**
   * Send a notification to another user (delegates to library system)
   */
  sendNotification(recipientId: UUID, message: string, type: NotificationType): void {
    // This would typically delegate to a notification service
    // For now, we'll leave it as a placeholder for the service integration
    throw new Error('Notification service not yet integrated.');
  }

  /**
   * Send an email to a recipient (delegates to email service)
   */
  sendEmail(recipientEmail: Email, subject: string, body: string): void {
    // This would typically delegate to an email service
    // For now, we'll leave it as a placeholder for the service integration
    throw new Error('Email service not yet integrated.');
  }

  /**
   * Receive all notifications for this borrower
   */
  receiveNotification(): Notification[] {
    // This would fetch from a notification repository
    // For now, return empty array - will integrate with Library later
    return [];
  }

  /**
   * Mark a specific notification as read
   */
  markNotificationAsRead(notificationId: UUID): void {
    // This would update the notification in the repository
    // For now, placeholder for repository integration
    throw new Error('Notification repository not yet integrated.');
  }

  // ==================== ISearchable Implementation ====================

  /**
   * Search books by title (case-insensitive partial match)
   */
  searchByTitle(title: string): Book[] {
    // This delegates to the Library system
    // For now, placeholder - will integrate with Library
    throw new Error('Search service not yet integrated with Library.');
  }

  /**
   * Search books by author (case-insensitive partial match)
   */
  searchByAuthor(author: string): Book[] {
    // This delegates to the Library system
    // For now, placeholder - will integrate with Library
    throw new Error('Search service not yet integrated with Library.');
  }

  /**
   * Search for a book by exact ISBN
   */
  searchByISBN(isbn: string): Book | null {
    // This delegates to the Library system
    // For now, placeholder - will integrate with Library
    throw new Error('Search service not yet integrated with Library.');
  }

  /**
   * Get all available books (not currently borrowed)
   */
  searchAvailableBooks(): Book[] {
    // This delegates to the Library system
    // For now, placeholder - will integrate with Library
    throw new Error('Search service not yet integrated with Library.');
  }

  /**
   * Filter books by multiple criteria
   */
  filterBooks(criteria: SearchCriteria): Book[] {
    // This delegates to the Library system
    // For now, placeholder - will integrate with Library
    throw new Error('Search service not yet integrated with Library.');
  }

  // ==================== Book Operations Methods ====================

  /**
   * Search books by title (alias for ISearchable method)
   */
  getBookByTitle(title: string): Book[] {
    return this.searchByTitle(title);
  }

  /**
   * Get a specific book by its ID
   */
  getBookById(bookId: UUID): Book {
    // This delegates to the Library system
    throw new Error('Book retrieval service not yet integrated with Library.');
  }

  /**
   * Borrow a book from the library
   * Event: "le USER emprunte un livre"
   */
  borrowBook(bookId: UUID): BorrowingRecord {
    // Validate borrowing conditions
    if (!this.canBorrow()) {
      throw new Error('Cannot borrow: maximum books limit reached or account suspended.');
    }

    if (!this.isAuthorized) {
      throw new Error('Cannot borrow: account not authorized.');
    }

    // This will delegate to Library.processBorrowing()
    throw new Error('Borrowing service not yet integrated with Library.');
  }

  /**
   * Return a borrowed book
   * Event: "le USER retourne un livre"
   */
  returnBook(bookId: UUID): void {
    // Check if book is actually borrowed by this user
    if (!this.borrowedBooks.includes(bookId)) {
      throw new Error('Cannot return: book not borrowed by this user.');
    }

    // Remove from borrowed books
    this.borrowedBooks = this.borrowedBooks.filter((id) => id !== bookId);

    // This will delegate to Library.processReturn()
    throw new Error('Return service not yet integrated with Library.');
  }

  /**
   * Request extension of borrowing period
   * Event: "le USER demande une prolongation d'emprunt"
   */
  extendBorrowingPeriod(bookId: UUID, days: number): boolean {
    // Validate extension request
    if (!this.borrowedBooks.includes(bookId)) {
      throw new Error('Cannot extend: book not borrowed by this user.');
    }

    // This will delegate to Library with business rules validation
    throw new Error('Extension service not yet integrated with Library.');
  }

  /**
   * Get all currently borrowed books
   * Event: "le USER consulte ses livres actuellement empruntés"
   */
  getMyBorrowedBooks(): Book[] {
    // This will fetch books from Library based on borrowedBooks IDs
    throw new Error('Book fetching service not yet integrated with Library.');
  }

  /**
   * Get complete borrowing history
   * Event: "le USER consulte son historique d'emprunts complet"
   */
  getMyBorrowingHistory(): BorrowingRecord[] {
    return [...this.borrowingHistory];
  }

  // ==================== Private Book Helper Methods ====================

  /**
   * Check if the borrower can borrow more books
   */
  private canBorrow(): boolean {
    return (
      this.borrowedBooks.length < this.maxBooksAllowed &&
      this.isActive &&
      !this.isSuspended()
    );
  }

  // ==================== Comments & Reviews Methods ====================

  /**
   * Add a comment and rating to a book
   * Event: "le USER ajoute un commentaire sur un livre"
   */
  addComment(bookId: UUID, content: string, rating: number): Comment {
    // Validate content length
    if (content.length < 10) {
      throw new Error('Comment must be at least 10 characters long.');
    }

    if (content.length > 500) {
      throw new Error('Comment must not exceed 500 characters.');
    }

    // Validate rating
    if (rating < 1 || rating > 5) {
      throw new Error('Rating must be between 1 and 5.');
    }

    // Create comment (will be saved to repository via Library)
    throw new Error('Comment service not yet integrated with Library.');
  }

  /**
   * Edit an existing comment
   * Event: "le USER modifie son commentaire"
   */
  editComment(commentId: UUID, content: string): void {
    // Validate content length
    if (content.length < 10 || content.length > 500) {
      throw new Error('Comment must be between 10 and 500 characters.');
    }

    // Update comment (delegates to repository)
    throw new Error('Comment update service not yet integrated.');
  }

  /**
   * Delete a comment
   * Event: "le USER supprime son commentaire"
   */
  deleteComment(commentId: UUID): void {
    // Delete comment (delegates to repository)
    throw new Error('Comment deletion service not yet integrated.');
  }

  /**
   * Get all comments made by this borrower
   * Event: "le USER consulte ses propres commentaires"
   */
  getMyComments(): Comment[] {
    // Fetch comments from repository
    throw new Error('Comment retrieval service not yet integrated.');
  }

  // ==================== Notifications Methods ====================

  /**
   * Subscribe to availability notifications for a specific book
   * Event: "le USER s'abonne aux notifications de disponibilité d'un livre"
   */
  subscribeToBookAvailability(bookId: UUID): void {
    // Add subscription (delegates to notification service)
    throw new Error('Subscription service not yet integrated.');
  }

  /**
   * Unsubscribe from availability notifications for a specific book
   * Event: "le USER se désabonne des notifications de disponibilité d'un livre"
   */
  unsubscribeFromBookAvailability(bookId: UUID): void {
    // Remove subscription (delegates to notification service)
    throw new Error('Unsubscription service not yet integrated.');
  }

  // ==================== Claims Methods ====================

  /**
   * Submit a claim to the library
   * Event: "le USER soumet une réclamation"
   */
  sendClaim(subject: string, description: string): void {
    // Validate claim data
    if (description.length < 20) {
      throw new Error('Claim description must be at least 20 characters long.');
    }

    if (description.length > 1000) {
      throw new Error('Claim description must not exceed 1000 characters.');
    }

    // Create and submit claim (delegates to claim service)
    throw new Error('Claim service not yet integrated.');
  }

  /**
   * Get all claims submitted by this borrower
   * Event: "le USER consulte ses réclamations"
   */
  getMyClaims(): any[] {
    // Fetch claims from repository
    throw new Error('Claim retrieval service not yet integrated.');
  }
}
