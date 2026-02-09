/**
 * Roles and permissions for librarians
 */
export enum LibrarianRole {
  ADMIN = 'admin', // Administrator (all rights)
  STANDARD = 'standard', // Standard librarian
  ASSISTANT = 'assistant', // Assistant (limited rights)
  VOLUNTEER = 'volunteer', // Volunteer (read-only + some actions)
}
