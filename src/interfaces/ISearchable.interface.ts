import { SearchCriteria } from '../types';
import { Book } from '../models';

/**
 * Interface for searchable objects
 */
export interface ISearchable {
  /**
   * Search for books by title
   */
  searchByTitle(title: string): Book[];

  /**
   * Search for books by author
   */
  searchByAuthor(author: string): Book[];

  /**
   * Search for a book by ISBN
   */
  searchByISBN(isbn: string): Book | null;

  /**
   * Search for available books
   */
  searchAvailableBooks(): Book[];

  /**
   * Filter books by criteria
   */
  filterBooks(criteria: SearchCriteria): Book[];
}
