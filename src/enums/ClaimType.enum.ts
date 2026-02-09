/**
 * Types of possible claims
 */
export enum ClaimType {
  DAMAGED_BOOK = 'damaged_book', // Damaged book
  LOST_BOOK = 'lost_book', // Lost book
  INCORRECT_CHARGE = 'incorrect_charge', // Incorrect fees
  ACCOUNT_ISSUE = 'account_issue', // Account problem
  SERVICE_COMPLAINT = 'service_complaint', // Service complaint
  TECHNICAL_ISSUE = 'technical_issue', // Technical problem
  OTHER = 'other', // Other
}
