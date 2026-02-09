import { UUID, DateTime } from '../types';

/**
 * Comment model representing a user comment on a book
 */
export class Comment {
  public readonly id: UUID;
  public readonly bookId: UUID;
  public readonly userId: UUID;
  public content: string;
  public rating: number;
  public readonly createdDate: DateTime;
  public isApproved: boolean;

  constructor(id: UUID, bookId: UUID, userId: UUID, content: string, rating: number) {
    this.id = id;
    this.bookId = bookId;
    this.userId = userId;
    this.content = content;
    this.rating = rating;
    this.createdDate = new Date();
    this.isApproved = false;
  }
}
