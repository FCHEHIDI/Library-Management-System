import { UUID, DateTime } from '../types';
import { NotificationType } from '../enums';

/**
 * Notification model representing a notification sent to a user
 */
export class Notification {
  public readonly id: UUID;
  public readonly recipientId: UUID;
  public readonly senderId: UUID | null;
  public readonly type: NotificationType;
  public readonly message: string;
  public readonly createdDate: DateTime;
  public isRead: boolean;

  constructor(
    id: UUID,
    recipientId: UUID,
    type: NotificationType,
    message: string,
    senderId: UUID | null = null
  ) {
    this.id = id;
    this.recipientId = recipientId;
    this.senderId = senderId;
    this.type = type;
    this.message = message;
    this.createdDate = new Date();
    this.isRead = false;
  }
}
