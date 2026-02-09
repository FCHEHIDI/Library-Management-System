import { Notification } from '../../src/models/Notification.model';
import { NotificationType } from '../../src/enums';

describe('Notification Model Tests', () => {
  test('Notification is created with correct default values', () => {
    const notification = new Notification(
      'notif-001',
      'user-001',
      'Your book is due tomorrow',
      NotificationType.DUE_DATE_REMINDER
    );

    expect(notification.id).toBe('notif-001');
    expect(notification.userId).toBe('user-001');
    expect(notification.message).toBe('Your book is due tomorrow');
    expect(notification.type).toBe(NotificationType.DUE_DATE_REMINDER);
    expect(notification.sentAt).toBeInstanceOf(Date);
    expect(notification.isRead).toBe(false);
  });

  test('Notification can be marked as read', () => {
    const notification = new Notification(
      'notif-001',
      'user-001',
      'Test message',
      NotificationType.INFO
    );

    expect(notification.isRead).toBe(false);

    notification.isRead = true;
    expect(notification.isRead).toBe(true);
  });

  test('Notification supports different types', () => {
    const infoNotif = new Notification(
      'notif-001',
      'user-001',
      'Info message',
      NotificationType.INFO
    );
    expect(infoNotif.type).toBe(NotificationType.INFO);

    const warningNotif = new Notification(
      'notif-002',
      'user-001',
      'Warning message',
      NotificationType.WARNING
    );
    expect(warningNotif.type).toBe(NotificationType.WARNING);

    const errorNotif = new Notification(
      'notif-003',
      'user-001',
      'Error message',
      NotificationType.ERROR
    );
    expect(errorNotif.type).toBe(NotificationType.ERROR);

    const reminderNotif = new Notification(
      'notif-004',
      'user-001',
      'Reminder message',
      NotificationType.DUE_DATE_REMINDER
    );
    expect(reminderNotif.type).toBe(NotificationType.DUE_DATE_REMINDER);

    const overdueNotif = new Notification(
      'notif-005',
      'user-001',
      'Overdue message',
      NotificationType.OVERDUE_NOTICE
    );
    expect(overdueNotif.type).toBe(NotificationType.OVERDUE_NOTICE);
  });

  test('Notification timestamp is set on creation', () => {
    const beforeCreation = new Date();
    const notification = new Notification(
      'notif-001',
      'user-001',
      'Test',
      NotificationType.INFO
    );
    const afterCreation = new Date();

    expect(notification.sentAt.getTime()).toBeGreaterThanOrEqual(beforeCreation.getTime());
    expect(notification.sentAt.getTime()).toBeLessThanOrEqual(afterCreation.getTime());
  });
});
