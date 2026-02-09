/**
 * Physical state of a book for tracking wear and tear
 */
export enum PhysicalState {
  EXCELLENT = 'excellent', // Like new, no signs of wear
  GOOD = 'good', // Good overall condition, slight signs of use
  FAIR = 'fair', // Fair condition, visible signs of wear
  POOR = 'poor', // Poor condition, requires repair
  DAMAGED = 'damaged', // Damaged, not borrowable
  LOST = 'lost', // Lost by a borrower
  IN_REPAIR = 'in_repair', // Under repair
}
