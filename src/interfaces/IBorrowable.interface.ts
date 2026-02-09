import { UUID } from '../types';
import { BorrowingRecord } from '../models';

/**
 * Interface for objects that can be borrowed
 */
export interface IBorrowable {
  /**
   * Check if the item can be borrowed
   */
  canBeBorrowed(): boolean;

  /**
   * Borrow the item
   */
  borrow(borrowerId: UUID): BorrowingRecord;

  /**
   * Return the item
   */
  return(borrowerId: UUID): void;

  /**
   * Extend the borrowing period
   */
  extendBorrowingPeriod(days: number): boolean;

  /**
   * Get the borrowing history
   */
  getBorrowingHistory(): BorrowingRecord[];
}
