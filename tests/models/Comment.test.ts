import { Comment } from '../../src/models/Comment.model';
import { ClaimType, ClaimStatus, ClaimPriority } from '../../src/enums';

describe('Comment Model Tests', () => {
  test('Comment is created with correct default values', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'This is a great book!'
    );

    expect(comment.id).toBe('comment-001');
    expect(comment.userId).toBe('user-001');
    expect(comment.bookId).toBe('book-001');
    expect(comment.content).toBe('This is a great book!');
    expect(comment.createdAt).toBeInstanceOf(Date);
    expect(comment.approved).toBe(false);
    expect(comment.rating).toBeUndefined();
    expect(comment.claimType).toBeNull();
    expect(comment.claimStatus).toBe(ClaimStatus.PENDING);
    expect(comment.claimPriority).toBe(ClaimPriority.LOW);
  });

  test('Comment can include rating', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'Excellent read!',
      5
    );

    expect(comment.rating).toBe(5);
  });

  test('Comment can be approved', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'Good book'
    );

    expect(comment.approved).toBe(false);

    comment.approved = true;
    expect(comment.approved).toBe(true);
  });

  test('Comment can be used as a claim', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'The book has missing pages'
    );

    comment.claimType = ClaimType.DAMAGED_BOOK;
    comment.claimStatus = ClaimStatus.PENDING;
    comment.claimPriority = ClaimPriority.HIGH;

    expect(comment.claimType).toBe(ClaimType.DAMAGED_BOOK);
    expect(comment.claimStatus).toBe(ClaimStatus.PENDING);
    expect(comment.claimPriority).toBe(ClaimPriority.HIGH);
  });

  test('Claim status can be updated', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'Issue with book'
    );

    comment.claimType = ClaimType.LOST_BOOK;
    comment.claimStatus = ClaimStatus.PENDING;

    expect(comment.claimStatus).toBe(ClaimStatus.PENDING);

    comment.claimStatus = ClaimStatus.IN_PROGRESS;
    expect(comment.claimStatus).toBe(ClaimStatus.IN_PROGRESS);

    comment.claimStatus = ClaimStatus.RESOLVED;
    expect(comment.claimStatus).toBe(ClaimStatus.RESOLVED);
  });

  test('Claim priority levels work correctly', () => {
    const comment = new Comment(
      'comment-001',
      'user-001',
      'book-001',
      'Claim description'
    );

    comment.claimType = ClaimType.OTHER;

    comment.claimPriority = ClaimPriority.LOW;
    expect(comment.claimPriority).toBe(ClaimPriority.LOW);

    comment.claimPriority = ClaimPriority.MEDIUM;
    expect(comment.claimPriority).toBe(ClaimPriority.MEDIUM);

    comment.claimPriority = ClaimPriority.HIGH;
    expect(comment.claimPriority).toBe(ClaimPriority.HIGH);

    comment.claimPriority = ClaimPriority.URGENT;
    expect(comment.claimPriority).toBe(ClaimPriority.URGENT);
  });
});
