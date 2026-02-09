import { UUID, Email } from '../types';
import { NotificationType } from '../enums';
import { Notification } from '../models';

/**
 * Interface for objects that can send and receive notifications
 */
export interface INotifiable {
  /**
   * Send a notification to a recipient
   */
  sendNotification(recipientId: UUID, message: string, type: NotificationType): void;

  /**
   * Send an email to a recipient
   */
  sendEmail(recipientEmail: Email, subject: string, body: string): void;

  /**
   * Receive all notifications for this user
   */
  receiveNotification(): Notification[];

  /**
   * Mark a notification as read
   */
  markNotificationAsRead(notificationId: UUID): void;
}
