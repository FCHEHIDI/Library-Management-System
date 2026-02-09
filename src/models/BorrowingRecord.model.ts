import { UUID, DateTime } from '../types';
import { BorrowingStatus } from '../enums';

/**
 * BorrowingRecord model representing a book borrowing transaction
 */
export class BorrowingRecord {
  public readonly id: UUID;
  public readonly bookId: UUID;
  public readonly borrowerId: UUID;
  public readonly borrowDate: DateTime;
  public dueDate: DateTime;
  public returnDate: DateTime | null;
  public isExtended: boolean;
  public extensionCount: number;
  public status: BorrowingStatus;

  constructor(id: UUID, bookId: UUID, borrowerId: UUID, borrowDate: DateTime, dueDate: DateTime) {
    this.id = id;
    this.bookId = bookId;
    this.borrowerId = borrowerId;
    this.borrowDate = borrowDate;
    this.dueDate = dueDate;
    this.returnDate = null;
    this.isExtended = false;
    this.extensionCount = 0;
    this.status = BorrowingStatus.ACTIVE;
  }
}
