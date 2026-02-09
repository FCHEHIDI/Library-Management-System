import { UUID, DateTime } from '../types';
import { BookCategory, PhysicalState } from '../enums';
import { BorrowingRecord } from './BorrowingRecord.model';

/**
 * Book model representing a book in the library
 */
export class Book {
  public readonly id: UUID;
  public title: string;
  public author: string;
  public ISBN: string;
  public publisher: string;
  public publicationYear: number;
  public category: BookCategory;
  public isAvailable: boolean;
  public physicalState: PhysicalState;
  public borrowingHistory: BorrowingRecord[];
  public isRestricted: boolean;
  public addedDate: DateTime;
  public lastModified: DateTime;
  public description: string;
  public coverImageUrl: string;

  constructor(
    id: UUID,
    title: string,
    author: string,
    ISBN: string,
    publisher: string,
    publicationYear: number,
    category: BookCategory,
    description: string = '',
    coverImageUrl: string = ''
  ) {
    this.id = id;
    this.title = title;
    this.author = author;
    this.ISBN = ISBN;
    this.publisher = publisher;
    this.publicationYear = publicationYear;
    this.category = category;
    this.isAvailable = true;
    this.physicalState = PhysicalState.EXCELLENT;
    this.borrowingHistory = [];
    this.isRestricted = false;
    this.addedDate = new Date();
    this.lastModified = new Date();
    this.description = description;
    this.coverImageUrl = coverImageUrl;
  }
}
