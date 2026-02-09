/**
 * Common types used across the library management system
 */

/**
 * UUID type for unique identifiers
 */
export type UUID = string;

/**
 * DateTime type for timestamps
 */
export type DateTime = Date;

/**
 * Email validation type
 */
export type Email = string;

/**
 * Phone number type
 */
export type PhoneNumber = string;

/**
 * Partial type utility for update operations
 */
export type PartialUpdate<T> = Partial<T>;

/**
 * User profile data transfer object
 */
export interface UserProfile {
  id: UUID;
  name: string;
  firstname: string;
  email: Email;
  phone: PhoneNumber;
  address?: string;
  isActive: boolean;
  lastLogin: DateTime;
}

/**
 * Book data transfer object for creation
 */
export interface BookData {
  title: string;
  author: string;
  ISBN: string;
  publisher: string;
  publicationYear: number;
  category: string;
  description?: string;
  coverImageUrl?: string;
}

/**
 * User data transfer object for registration
 */
export interface UserData {
  name: string;
  firstname: string;
  email: Email;
  phone: PhoneNumber;
  address: string;
}

/**
 * Search criteria for filtering books
 */
export interface SearchCriteria {
  title?: string;
  author?: string;
  category?: string;
  year?: number;
  availability?: boolean;
  minRating?: number;
}

/**
 * Opening hours configuration
 */
export interface OpeningHours {
  monday: { open: string; close: string };
  tuesday: { open: string; close: string };
  wednesday: { open: string; close: string };
  thursday: { open: string; close: string };
  friday: { open: string; close: string };
  saturday: { open: string; close: string };
  sunday: { open: string; close: string };
}

/**
 * Claim data for user complaints
 */
export interface ClaimData {
  subject: string;
  description: string;
  type: string;
  priority?: string;
}
