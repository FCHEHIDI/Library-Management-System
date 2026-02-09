import { Librarian } from '../../src/domains/Librarian';
import { Book, Comment, BorrowingRecord } from '../../src/models';
import { LibrarianRole, PhysicalState, BookCategory } from '../../src/enums';
import { UUID, Email, PhoneNumber, UserData, BookData } from '../../src/types';

describe('Librarian - Administrative Tests', () => {
  let librarian: Librarian;

  beforeEach(() => {
    librarian = new Librarian(
      'librarian-001',
      'Martin',
      'Sophie',
      'sophie.martin@library.fr' as Email,
      '+33123456789' as PhoneNumber,
      LibrarianRole.SENIOR
    );
  });

  // ==================== IUser Implementation Tests ====================

  describe('IUser Interface Implementation', () => {
    test('getProfile returns librarian profile information', () => {
      const profile = librarian.getProfile();

      expect(profile.id).toBe('librarian-001');
      expect(profile.name).toBe('Martin');
      expect(profile.firstname).toBe('Sophie');
      expect(profile.email).toBe('sophie.martin@library.fr');
    });

    test('updateProfile updates librarian information', () => {
      librarian.updateProfile({
        name: 'Dubois',
        phone: '+33987654321' as PhoneNumber
      });

      expect(librarian.name).toBe('Dubois');
      expect(librarian.phone).toBe('+33987654321');
      expect(librarian.firstname).toBe('Sophie'); // Unchanged
    });

    test('getId returns librarian unique identifier', () => {
      expect(librarian.getId()).toBe('librarian-001');
    });
  });

  // ==================== INotifiable Implementation Tests ====================

  describe('INotifiable Interface Implementation', () => {
    test('sendNotification logs notification action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.sendNotification('user-123', 'Test notification', 0);

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Notification sent')
      );
      consoleSpy.mockRestore();
    });

    test('sendEmail logs email action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.sendEmail('user@example.com' as Email, 'Subject', 'Body');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Email sent')
      );
      consoleSpy.mockRestore();
    });

    test('receiveNotification returns empty array (placeholder)', () => {
      const notifications = librarian.receiveNotification();
      expect(Array.isArray(notifications)).toBe(true);
      expect(notifications.length).toBe(0);
    });

    test('markNotificationAsRead logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.markNotificationAsRead('notif-123');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  // ==================== Book Management Tests ====================

  describe('Book Management Methods', () => {
    const validBookData: BookData = {
      title: 'Test Book',
      author: 'Test Author',
      ISBN: '978-1234567890',
      category: BookCategory.FICTION,
      physicalState: PhysicalState.NEW,
      pages: 300,
      publisher: 'Test Publisher',
      year: 2023
    };

    test('Event: le LIBRARIAN ajoute un nouveau livre - addBook requires title', () => {
      const invalidBook = { ...validBookData, title: '' };

      expect(() => librarian.addBook(invalidBook as any)).toThrow('title');
    });

    test('Event: le LIBRARIAN ajoute un nouveau livre - addBook requires author', () => {
      const invalidBook = { ...validBookData, author: '' };

      expect(() => librarian.addBook(invalidBook as any)).toThrow('author');
    });

    test('Event: le LIBRARIAN ajoute un nouveau livre - addBook requires ISBN', () => {
      const invalidBook = { ...validBookData, ISBN: '' };

      expect(() => librarian.addBook(invalidBook as any)).toThrow('ISBN');
    });

    test('Event: le LIBRARIAN ajoute un nouveau livre - addBook logs success', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.addBook(validBookData as any);

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Book added')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN modifie les informations d\'un livre - updateBook logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.updateBook('book-123', { title: 'Updated Title' });

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN supprime un livre - deleteBookById logs deletion', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.deleteBookById('book-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('deleted')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN rend un livre non empruntable - restrictBook requires reason', () => {
      expect(() => librarian.restrictBook('book-123', '')).toThrow('reason');
    });

    test('Event: le LIBRARIAN rend un livre non empruntable - restrictBook logs restriction', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.restrictBook('book-123', 'Damaged cover');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('restricted')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN rend un livre à nouveau empruntable - unrestrictBook logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.unrestrictBook('book-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('unrestricted')
      );
      consoleSpy.mockRestore();
    });

    test('updatePhysicalState logs state change', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.updatePhysicalState('book-123', PhysicalState.WORN);

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('physical state updated')
      );
      consoleSpy.mockRestore();
    });

    test('setBookAvailability logs availability change', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.setBookAvailability('book-123', false);

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('getAllBooks returns empty array (placeholder)', () => {
      const books = librarian.getAllBooks();
      expect(Array.isArray(books)).toBe(true);
    });
  });

  // ==================== User Management Tests ====================

  describe('User Management Methods', () => {
    const validUserData: UserData = {
      name: 'Dupont',
      firstname: 'Jean',
      email: 'jean.dupont@example.com' as Email,
      phone: '+33612345678' as PhoneNumber,
      address: { street: '1 rue Test', city: 'Paris', zipCode: '75001', country: 'France' }
    };

    test('Event: le SYSTEM enregistre un nouveau USER - addUser requires email', () => {
      const invalidUser = { ...validUserData, email: '' };

      expect(() => librarian.addUser(invalidUser as any)).toThrow('email');
    });

    test('Event: le SYSTEM enregistre un nouveau USER - addUser requires name', () => {
      const invalidUser = { ...validUserData, name: '' };

      expect(() => librarian.addUser(invalidUser as any)).toThrow('name');
    });

    test('Event: le SYSTEM enregistre un nouveau USER - addUser logs success', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.addUser(validUserData);

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('User added')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN supprime un USER - deleteUser logs deletion', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.deleteUser('user-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('deleted')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN suspend un USER - suspendUser requires positive duration', () => {
      expect(() => librarian.suspendUser('user-123', -5, 'Test')).toThrow('positive');
    });

    test('Event: le LIBRARIAN suspend un USER - suspendUser requires reason', () => {
      expect(() => librarian.suspendUser('user-123', 7, '')).toThrow('reason');
    });

    test('Event: le LIBRARIAN suspend un USER - suspendUser logs suspension', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.suspendUser('user-123', 7, 'Late returns');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('suspended for 7 days')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN désactive un USER - deactivateUser requires reason', () => {
      expect(() => librarian.deactivateUser('user-123', '')).toThrow('reason');
    });

    test('Event: le LIBRARIAN active un USER - activateUser logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.activateUser('user-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('activated')
      );
      consoleSpy.mockRestore();
    });

    test('authorizeUser logs authorization', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.authorizeUser('user-123');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('revokeUserAuthorization logs revocation', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.revokeUserAuthorization('user-123');

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });

  // ==================== Communication Methods Tests ====================

  describe('Communication Methods', () => {
    test('Event: le LIBRARIAN envoie un email à un USER - sendEmailToUser requires subject', () => {
      expect(() => librarian.sendEmailToUser('user-123', '', 'Body')).toThrow('subject');
    });

    test('Event: le LIBRARIAN envoie un email à un USER - sendEmailToUser requires body', () => {
      expect(() => librarian.sendEmailToUser('user-123', 'Subject', '')).toThrow('body');
    });

    test('Event: le LIBRARIAN envoie un email à un USER - sendEmailToUser logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.sendEmailToUser('user-123', 'Test Subject', 'Test Body');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Email sent to user')
      );
      consoleSpy.mockRestore();
    });

    test('sendEmailToAdmin requires subject and body', () => {
      expect(() => librarian.sendEmailToAdmin('', 'Body')).toThrow('subject');
      expect(() => librarian.sendEmailToAdmin('Subject', '')).toThrow('body');
    });

    test('Event: le LIBRARIAN poste une info générale - postGeneralInfo requires message', () => {
      expect(() => librarian.postGeneralInfo('')).toThrow('Message is required');
    });

    test('Event: le LIBRARIAN poste une info générale - postGeneralInfo logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.postGeneralInfo('Library will close early on Friday');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('General info posted')
      );
      consoleSpy.mockRestore();
    });
  });

  // ==================== Comments Management Tests ====================

  describe('Comments Management Methods', () => {
    test('Event: le LIBRARIAN approuve un commentaire - approveComment logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.approveComment('comment-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('approved')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN refuse un commentaire - rejectComment logs action', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.rejectComment('comment-123');

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('rejected')
      );
      consoleSpy.mockRestore();
    });

    test('Event: le LIBRARIAN consulte les commentaires en attente - getPendingComments returns array', () => {
      const pending = librarian.getPendingComments();
      expect(Array.isArray(pending)).toBe(true);
    });
  });

  // ==================== Integration Tests ====================

  describe('Integration Scenarios', () => {
    test('Librarian complete workflow: add book → add user → manage communications', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      // Add book
      librarian.addBook({
        title: 'New Book',
        author: 'Author',
        ISBN: '123456',
        category: BookCategory.FICTION,
        physicalState: PhysicalState.NEW,
        pages: 200,
        publisher: 'Publisher',
        year: 2023
      } as any);

      // Add user
      librarian.addUser({
        name: 'User',
        firstname: 'Test',
        email: 'test@example.com' as Email,
        phone: '+33123456789' as PhoneNumber,
        address: { street: '', city: '', zipCode: '', country: '' }
      });

      // Send communication
      librarian.postGeneralInfo('New book available!');

      expect(consoleSpy).toHaveBeenCalledTimes(3);
      consoleSpy.mockRestore();
    });

    test('Book restriction workflow', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.restrictBook('book-123', 'Pages damaged');
      librarian.updatePhysicalState('book-123', PhysicalState.DAMAGED);

      expect(consoleSpy).toHaveBeenCalledTimes(2);
      consoleSpy.mockRestore();
    });

    test('User suspension and reactivation workflow', () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      librarian.suspendUser('user-123', 14, 'Multiple late returns');
      librarian.activateUser('user-123');

      expect(consoleSpy).toHaveBeenCalledTimes(2);
      consoleSpy.mockRestore();
    });
  });
});
