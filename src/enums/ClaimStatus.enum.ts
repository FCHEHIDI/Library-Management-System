/**
 * Status of a user claim
 */
export enum ClaimStatus {
  PENDING = 'pending', // Awaiting processing
  IN_PROGRESS = 'in_progress', // Being processed
  RESOLVED = 'resolved', // Resolved
  REJECTED = 'rejected', // Rejected
  CLOSED = 'closed', // Closed
}
