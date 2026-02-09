import { Borrower } from '../../src/domains/Borrower';
import { Book, BorrowingRecord, Comment, Notification } from '../../src/models';
import {
  BookCategory,
  PhysicalState,
  BorrowingStatus,
  NotificationType,
  UserStatus,
  ClaimType,
  ClaimPriority
} from '../../src/enums';
import { UUID, Email, PhoneNumber, Address } from '../../src/types';
import { VALIDATION_POLICIES, BORROWING_POLICIES } from '../../src/policies';

describe('Borrower - Event-Driven Tests', () => {
  let borrower: Borrower;
  let testEmail: Email;
  let testPhone: PhoneNumber;
  let testAddress: Address;

  beforeEach(() => {
    testEmail = 'john.doe@example.com' as Email;
    testPhone = '+33612345678' as PhoneNumber;
    testAddress = {
      street: '123 Main St',
      city: 'Paris',
      zipCode: '75001',
      country: 'France'
    };

    borrower = new Borrower(
      'borrower-123',
      'Doe',
      'John',
      testEmail,
      testPhone,
      testAddress
    );
  });

  // ==================== IUser Interface Tests ====================

  describe('IUser Interface Implementation', () => {
    test('Event: le USER consulte son profil - getProfile returns complete profile', () => {
      const profile = borrower.getProfile();

      expect(profile.id).toBe('borrower-123');
      expect(profile.name).toBe('Doe');
      expect(profile.firstname).toBe('John');
      expect(profile.email).toBe(testEmail);
      expect(profile.phone).toBe(testPhone);
      expect(profile.address).toEqual(testAddress);
    });

    test('Event: le USER modifie son profil - updateProfile updates fields correctly', () => {
      const newEmail = 'jane.doe@example.com' as Email;
      const updates = {
        name: 'Smith',
        email: newEmail
      };

      borrower.updateProfile(updates);

      const updatedProfile = borrower.getProfile();
      expect(updatedProfile.name).toBe('Smith');
      expect(updatedProfile.email).toBe(newEmail);
      expect(updatedProfile.firstname).toBe('John'); // Unchanged
    });

    test('Event: le SYSTEM vérifie si USER est actif - isActive returns authorization status', () => {
      expect(borrower.isActive()).toBe(true);

      borrower.isAuthorized = false;
      expect(borrower.isActive()).toBe(false);
    });

    test('getId returns user unique identifier', () => {
      expect(borrower.getId()).toBe('borrower-123');
    });
  });

  // ==================== INotifiable Interface Tests ====================

  describe('INotifiable Interface Implementation', () => {
    test('Event: le USER envoie une notification - sendNotification placeholder logs correctly', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.sendNotification(
        'recipient-123',
        'Test notification',
        NotificationType.INFO
      );

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Notification sent')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le USER envoie un email - sendEmail placeholder logs correctly', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.sendEmail('test@example.com' as Email, 'Subject', 'Body');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Email sent')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le USER consulte ses notifications - receiveNotification returns empty array', () => {
      const notifications = borrower.receiveNotification();
      expect(Array.isArray(notifications)).toBe(true);
      expect(notifications.length).toBe(0);
    });

    test('Event: le USER marque notification comme lue - markNotificationAsRead logs correctly', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.markNotificationAsRead('notification-123');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  // ==================== Book Operations Tests ====================

  describe('Book Operations', () => {
    test('Event: le USER emprunte un livre - borrowBook requires valid book ID', () => {
      expect(() => borrower.borrowBook('')).toThrow('Book ID is required');
    });

    test('Event: le USER emprunte un livre - borrowBook enforces max books limit', () => {
      borrower.borrowedBooks = ['book1', 'book2', 'book3'];
      borrower.maxBooksAllowed = 3;

      expect(() => borrower.borrowBook('book4')).toThrow(
        'Maximum books limit reached'
      );
    });

    test('Event: le USER emprunte un livre - borrowBook prevents suspended users', () => {
      borrower.status = UserStatus.SUSPENDED;

      expect(() => borrower.borrowBook('book1')).toThrow(
        'Suspended users cannot borrow books'
      );
    });

    test('Event: le USER emprunte un livre - borrowBook prevents unauthorized users', () => {
      borrower.isAuthorized = false;

      expect(() => borrower.borrowBook('book1')).toThrow(
        'User is not authorized to borrow books'
      );
    });

    test('Event: le USER retourne un livre - returnBook requires valid book ID', () => {
      expect(() => borrower.returnBook('')).toThrow('Book ID is required');
    });

    test('Event: le USER prolonge un emprunt - extendBorrowingPeriod requires valid borrowing ID', () => {
      expect(() => borrower.extendBorrowingPeriod('')).toThrow(
        'Borrowing ID is required'
      );
    });

    test('Event: le USER consulte ses livres empruntés - getMyBorrowedBooks returns borrowed list', () => {
      borrower.borrowedBooks = ['book1', 'book2'];
      const books = borrower.getMyBorrowedBooks();

      expect(books).toEqual(['book1', 'book2']);
      expect(books.length).toBe(2);
    });

    test('Event: le USER consulte son historique - getMyBorrowingHistory returns history', () => {
      const history = borrower.getMyBorrowingHistory();
      expect(Array.isArray(history)).toBe(true);
    });
  });

  // ==================== ISearchable Interface Tests ====================

  describe('Search Operations', () => {
    test('Event: le USER recherche par titre - searchByTitle requires non-empty title', () => {
      expect(() => borrower.searchByTitle('')).toThrow('Search title is required');
    });

    test('Event: le USER recherche par titre - searchByTitle enforces min length', () => {
      expect(() => borrower.searchByTitle('ab')).toThrow(
        `Title must be at least ${VALIDATION_POLICIES.MIN_SEARCH_QUERY_LENGTH} characters`
      );
    });

    test('Event: le USER recherche par auteur - searchByAuthor requires non-empty author', () => {
      expect(() => borrower.searchByAuthor('')).toThrow('Author name is required');
    });

    test('Event: le USER recherche par ISBN - searchByISBN requires non-empty ISBN', () => {
      expect(() => borrower.searchByISBN('')).toThrow('ISBN is required');
    });

    test('Event: le USER filtre les livres - filterBooks requires valid category', () => {
      expect(() => borrower.filterBooks('', undefined, undefined)).toThrow(
        'At least one filter criterion is required'
      );
    });

    test('Event: le USER filtre les livres - filterBooks accepts category filter', () => {
      const result = borrower.filterBooks(BookCategory.FICTION, undefined, undefined);
      expect(Array.isArray(result)).toBe(true);
    });
  });

  // ==================== Comments & Reviews Tests ====================

  describe('Comments & Reviews Management', () => {
    test('Event: le USER ajoute un commentaire - addComment requires book ID', () => {
      expect(() => borrower.addComment('', 'Great book!')).toThrow(
        'Book ID is required'
      );
    });

    test('Event: le USER ajoute un commentaire - addComment requires content', () => {
      expect(() => borrower.addComment('book1', '')).toThrow(
        'Comment content is required'
      );
    });

    test('Event: le USER ajoute un commentaire - addComment enforces min length', () => {
      expect(() => borrower.addComment('book1', 'Short')).toThrow(
        `Comment must be at least ${VALIDATION_POLICIES.MIN_COMMENT_LENGTH} characters`
      );
    });

    test('Event: le USER ajoute un commentaire - addComment enforces max length', () => {
      const longComment = 'a'.repeat(VALIDATION_POLICIES.MAX_COMMENT_LENGTH + 1);
      expect(() => borrower.addComment('book1', longComment)).toThrow(
        `Comment cannot exceed ${VALIDATION_POLICIES.MAX_COMMENT_LENGTH} characters`
      );
    });

    test('Event: le USER ajoute un commentaire - addComment accepts rating', () => {
      const validComment = 'This is a great book with excellent content!';
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.addComment('book1', validComment, 5);

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('Event: le USER modifie son commentaire - editComment requires comment ID', () => {
      expect(() => borrower.editComment('', 'Updated content')).toThrow(
        'Comment ID is required'
      );
    });

    test('Event: le USER modifie son commentaire - editComment requires new content', () => {
      expect(() => borrower.editComment('comment1', '')).toThrow(
        'New content is required'
      );
    });

    test('Event: le USER supprime son commentaire - deleteComment requires comment ID', () => {
      expect(() => borrower.deleteComment('')).toThrow('Comment ID is required');
    });
  });

  // ==================== Notification Management Tests ====================

  describe('Notification Management', () => {
    test('Event: le USER consulte toutes ses notifications - getAllNotifications returns array', () => {
      const notifications = borrower.getAllNotifications();
      expect(Array.isArray(notifications)).toBe(true);
    });

    test('Event: le USER consulte notifications non lues - getUnreadNotifications returns array', () => {
      const unread = borrower.getUnreadNotifications();
      expect(Array.isArray(unread)).toBe(true);
    });

    test('Event: le USER marque toutes notifications comme lues - markAllNotificationsAsRead logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.markAllNotificationsAsRead();

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  // ==================== Claims Management Tests ====================

  describe('Claims Management', () => {
    test('Event: le USER envoie une réclamation - sendClaim requires description', () => {
      expect(() =>
        borrower.sendClaim(ClaimType.DAMAGED_BOOK, '', ClaimPriority.MEDIUM)
      ).toThrow('Claim description is required');
    });

    test('Event: le USER envoie une réclamation - sendClaim enforces min length', () => {
      expect(() =>
        borrower.sendClaim(ClaimType.DAMAGED_BOOK, 'Short', ClaimPriority.MEDIUM)
      ).toThrow(
        `Claim description must be at least ${VALIDATION_POLICIES.MIN_CLAIM_DESCRIPTION_LENGTH} characters`
      );
    });

    test('Event: le USER envoie une réclamation - sendClaim enforces max length', () => {
      const longClaim = 'a'.repeat(VALIDATION_POLICIES.MAX_CLAIM_DESCRIPTION_LENGTH + 1);
      expect(() =>
        borrower.sendClaim(ClaimType.DAMAGED_BOOK, longClaim, ClaimPriority.MEDIUM)
      ).toThrow(
        `Claim description cannot exceed ${VALIDATION_POLICIES.MAX_CLAIM_DESCRIPTION_LENGTH} characters`
      );
    });

    test('Event: le USER envoie une réclamation - sendClaim accepts valid claim', () => {
      const validDescription = 'The book I borrowed has a torn cover page. I noticed this when I received it.';
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.sendClaim(ClaimType.DAMAGED_BOOK, validDescription, ClaimPriority.HIGH);

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('Event: le USER consulte ses réclamations - getMyClaims returns array', () => {
      const claims = borrower.getMyClaims();
      expect(Array.isArray(claims)).toBe(true);
    });
  });

  // ==================== Integration Tests ====================

  describe('Integration Scenarios', () => {
    test('Complete borrower workflow: profile update → search → borrow attempt', () => {
      // Update profile
      borrower.updateProfile({ name: 'Johnson' });
      expect(borrower.name).toBe('Johnson');

      // Search for book
      const results = borrower.filterBooks(BookCategory.SCIENCE, undefined, undefined);
      expect(Array.isArray(results)).toBe(true);

      // Attempt to borrow (should fail at placeholder integration)
      borrower.borrowedBooks = [];
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      borrower.borrowBook('book-sci-123');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('User cannot borrow when limits are enforced', () => {
      borrower.borrowedBooks = ['book1', 'book2', 'book3'];
      borrower.maxBooksAllowed = BORROWING_POLICIES.MAX_BOOKS_PER_USER;

      expect(() => borrower.borrowBook('book4')).toThrow();
    });

    test('Suspended user workflow is blocked', () => {
      borrower.status = UserStatus.SUSPENDED;

      expect(() => borrower.borrowBook('book1')).toThrow('Suspended users');
      expect(borrower.isActive()).toBe(false);
    });
  });
});
