/**
 * Business rules and policies for the library management system
 * These constants avoid "magic numbers" and centralize modifiable rules
 */

/**
 * Borrowing limits and restrictions
 */
export const BORROWING_POLICIES = {
  // Quantitative limits
  MAX_BOOKS_PER_USER: 3,
  MAX_BOOKS_STANDARD: 3,
  MAX_BOOKS_PREMIUM: 5,
  MAX_BOOKS_CHILDREN: 2,

  // Extension limits
  MAX_EXTENSION_COUNT: 1,
  MAX_EXTENSION_DAYS: 7,
  MIN_EXTENSION_DAYS: 3,

  // Restrictions
  MIN_DAYS_BEFORE_EXTENSION: 2,
  MAX_ACTIVE_RESERVATIONS: 5,
} as const;

/**
 * Time-based policies (durations and delays)
 */
export const TIME_POLICIES = {
  // Borrowing periods
  DEFAULT_BORROWING_PERIOD: 14,
  REFERENCE_BORROWING_PERIOD: 7,
  NEW_RELEASE_BORROWING_PERIOD: 7,

  // Reminders and notifications
  REMINDER_DAYS_BEFORE_DUE: [3, 1],
  OVERDUE_NOTIFICATION_DAYS: [1, 7, 14, 30],

  // Suspensions and inactivity
  SUSPENSION_DURATION_FIRST_OFFENSE: 7,
  SUSPENSION_DURATION_SECOND_OFFENSE: 30,
  SUSPENSION_DURATION_THIRD_OFFENSE: 90,
  ACCOUNT_INACTIVE_DAYS: 365,
  AUTO_DEACTIVATE_INACTIVE_DAYS: 730,

  // Data retention
  NOTIFICATION_RETENTION_DAYS: 30,
  BORROWING_ARCHIVE_DAYS: 1095,
  CLAIM_AUTO_CLOSE_DAYS: 60,
} as const;

/**
 * Fee and penalty policies
 */
export const FEE_POLICIES = {
  // Late fees
  LATE_FEE_PER_DAY: 0.5,
  MAX_LATE_FEE: 50.0,
  LATE_FEE_GRACE_PERIOD: 1,

  // Loss/damage fees
  LOST_BOOK_FEE_MULTIPLIER: 1.5,
  DAMAGED_BOOK_FEE_LIGHT: 5.0,
  DAMAGED_BOOK_FEE_MODERATE: 15.0,
  DAMAGED_BOOK_FEE_SEVERE: 30.0,

  // Membership fees
  ANNUAL_MEMBERSHIP_FEE: 10.0,
  STUDENT_MEMBERSHIP_FEE: 5.0,
  SENIOR_MEMBERSHIP_FEE: 5.0,
  FAMILY_MEMBERSHIP_FEE: 25.0,
} as const;

/**
 * Access and authorization policies
 */
export const ACCESS_POLICIES = {
  // Minimum age
  MIN_AGE_FOR_ACCOUNT: 13,
  MIN_AGE_FOR_ADULT_CONTENT: 18,
  MIN_AGE_FOR_YOUNG_ADULT: 12,

  // Security
  MAX_FAILED_LOGIN_ATTEMPTS: 3,
  ACCOUNT_LOCKOUT_DURATION: 30,
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_REQUIRE_SPECIAL_CHAR: true,
  SESSION_TIMEOUT_MINUTES: 60,

  // Borrowing authorization
  MIN_ACCOUNT_AGE_DAYS: 1,
  REQUIRE_EMAIL_VERIFICATION: true,
  REQUIRE_PHONE_VERIFICATION: false,

  // Role restrictions
  VOLUNTEER_CAN_APPROVE_COMMENTS: false,
  ASSISTANT_CAN_DELETE_USERS: false,
  ADMIN_ONLY_SYSTEM_CONFIG: true,
} as const;

/**
 * Data validation policies
 */
export const VALIDATION_POLICIES = {
  // Comments
  MIN_COMMENT_LENGTH: 10,
  MAX_COMMENT_LENGTH: 500,
  MIN_RATING: 1,
  MAX_RATING: 5,
  REQUIRE_COMMENT_MODERATION: true,

  // ISBN
  ISBN_10_LENGTH: 10,
  ISBN_13_LENGTH: 13,
  ISBN_FORMAT_REGEX: /^(?:\d{9}[\dX]|\d{13})$/,

  // Texts
  MIN_BOOK_TITLE_LENGTH: 1,
  MAX_BOOK_TITLE_LENGTH: 255,
  MIN_BOOK_DESCRIPTION_LENGTH: 0,
  MAX_BOOK_DESCRIPTION_LENGTH: 2000,

  // Users
  MIN_NAME_LENGTH: 2,
  MAX_NAME_LENGTH: 50,
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE_REGEX: /^[\d\s\-+()]{10,20}$/,

  // Claims
  MIN_CLAIM_DESCRIPTION_LENGTH: 20,
  MAX_CLAIM_DESCRIPTION_LENGTH: 1000,
  MAX_CLAIM_ATTACHMENTS: 5,
} as const;

/**
 * Analytics and thresholds policies
 */
export const ANALYTICS_POLICIES = {
  // Popularity
  POPULAR_BOOK_MIN_BORROWS: 10,
  TRENDING_BOOK_PERIOD_DAYS: 30,
  TRENDING_MIN_BORROWS: 5,

  // Quality of service
  TARGET_AVAILABILITY_RATE: 0.95,
  MAX_ACCEPTABLE_OVERDUE_RATE: 0.05,
  GOOD_RATING_THRESHOLD: 4.0,

  // Alerts
  LOW_STOCK_THRESHOLD: 1,
  HIGH_DEMAND_THRESHOLD: 5,
  DAMAGED_BOOK_THRESHOLD_PERCENT: 0.1,

  // Recommendations
  RECOMMEND_BASED_ON_HISTORY: 10,
  SIMILAR_BOOKS_COUNT: 5,
  NEW_RELEASES_DAYS: 90,
} as const;

/**
 * Workflow automation policies
 */
export const WORKFLOW_POLICIES = {
  // Request processing
  AUTO_APPROVE_EXTENSION_IF_NO_RESERVATION: true,
  AUTO_REJECT_EXTENSION_IF_OVERDUE: true,
  AUTO_SUSPEND_ON_THIRD_OVERDUE: true,

  // Priorities
  CLAIM_AUTO_PRIORITY_URGENT_KEYWORDS: ['urgent', 'perdu', 'vol'],
  CLAIM_DEFAULT_PRIORITY: 'MEDIUM',

  // Notifications
  BATCH_NOTIFICATIONS: true,
  BATCH_NOTIFICATION_INTERVAL_HOURS: 24,
  SEND_EMAIL_NOTIFICATIONS: true,
  SEND_SMS_NOTIFICATIONS: false,

  // Moderation
  AUTO_APPROVE_COMMENTS_FROM_VERIFIED_USERS: false,
  FLAG_COMMENT_IF_CONTAINS_PROFANITY: true,
  MAX_COMMENTS_PER_USER_PER_DAY: 10,
} as const;

/**
 * Categorization and tagging policies
 */
export const CATEGORIZATION_POLICIES = {
  // Limits
  MAX_CATEGORIES_PER_BOOK: 3,
  MAX_TAGS_PER_BOOK: 10,
  MIN_TAG_LENGTH: 2,
  MAX_TAG_LENGTH: 30,

  // Auto-classification
  AUTO_TAG_ENABLED: true,
  AUTO_CATEGORIZE_BY_ISBN: true,

  // Search
  SEARCH_MIN_QUERY_LENGTH: 2,
  SEARCH_MAX_RESULTS: 100,
  SEARCH_FUZZY_MATCH_THRESHOLD: 0.8,
} as const;
