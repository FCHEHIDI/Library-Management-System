import { UUID, UserProfile, PartialUpdate } from '../types';

/**
 * Interface for user objects
 */
export interface IUser {
  /**
   * Get the user's profile
   */
  getProfile(): UserProfile;

  /**
   * Update the user's profile
   */
  updateProfile(profileData: PartialUpdate<UserProfile>): void;

  /**
   * Check if the user is active
   */
  isActive(): boolean;

  /**
   * Get the user's ID
   */
  getId(): UUID;
}
