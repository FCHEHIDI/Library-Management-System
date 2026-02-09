/**
 * Types of notifications sent to users
 */
export enum NotificationType {
  DUE_DATE = 'due_date', // Due date reminder
  OVERDUE = 'overdue', // Overdue notification
  EXTENSION_APPROVED = 'extension_approved', // Extension approved
  EXTENSION_DENIED = 'extension_denied', // Extension denied
  AVAILABILITY = 'availability', // Book available (subscription)
  RESERVATION_READY = 'reservation_ready', // Reservation ready for pickup
  ACCOUNT_SUSPENDED = 'account_suspended', // Account suspended
  ACCOUNT_ACTIVATED = 'account_activated', // Account activated
  GENERAL = 'general', // General information
  COMMENT_APPROVED = 'comment_approved', // Comment approved
  COMMENT_REJECTED = 'comment_rejected', // Comment rejected
  NEW_BOOK_ADDED = 'new_book_added', // New book added
  CLAIM_RECEIVED = 'claim_received', // Claim received
  CLAIM_RESOLVED = 'claim_resolved', // Claim resolved
}
