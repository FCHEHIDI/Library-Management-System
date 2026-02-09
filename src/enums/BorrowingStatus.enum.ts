/**
 * Status of a borrowing in the system
 */
export enum BorrowingStatus {
  ACTIVE = 'active', // Borrowing in progress
  RETURNED = 'returned', // Book returned
  OVERDUE = 'overdue', // Late
  EXTENDED = 'extended', // Extended
  CANCELLED = 'cancelled', // Cancelled before pickup
  RESERVED = 'reserved', // Reserved but not yet borrowed
}
