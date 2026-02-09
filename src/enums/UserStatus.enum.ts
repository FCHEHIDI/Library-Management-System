/**
 * Status of a user account
 */
export enum UserStatus {
  ACTIVE = 'active', // Active account
  INACTIVE = 'inactive', // Inactive account (no recent login)
  SUSPENDED = 'suspended', // Temporarily suspended
  DEACTIVATED = 'deactivated', // Deactivated by admin
  PENDING = 'pending', // Pending approval
  BANNED = 'banned', // Permanently banned
}
