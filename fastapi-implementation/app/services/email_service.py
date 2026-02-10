"""
Email service implementation.

Concrete implementation of IEmailService.
Handles all email operations with templating support.
"""

import os
from datetime import datetime

from app.interfaces.services import IEmailService
from app.core.config import get_settings


class EmailService(IEmailService):
    """
    Email service implementation.
    
    In production, this would integrate with:
    - SMTP (for self-hosted)
    - SendGrid
    - AWS SES
    - Mailgun
    
    For now, implements logging-based email simulation.
    """
    
    def __init__(self):
        """Initialize email service."""
        self.settings = get_settings()
        self.from_email = self.settings.SMTP_FROM_EMAIL
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> bool:
        """
        Send email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (text or HTML)
            html: True if body is HTML
            
        Returns:
            bool: True if sent successfully
        """
        # TODO: Integrate with actual email service
        # For now, just log the email
        
        print("=" * 60)
        print("[EMAIL SERVICE]")
        print(f"From: {self.from_email}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Content-Type: {'text/html' if html else 'text/plain'}")
        print("-" * 60)
        print(body)
        print("=" * 60)
        
        return True
    
    async def send_verification_email(
        self,
        to: str,
        token: str,
    ) -> bool:
        """
        Send email verification.
        
        Args:
            to: User's email address
            token: Verification token
            
        Returns:
            bool: True if sent successfully
        """
        verification_url = f"{self.settings.FRONTEND_URL}/verify-email?token={token}"
        
        subject = "Verify Your Email - Library Management System"
        
        body = f"""
        Welcome to Library Management System!
        
        Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        Library Management Team
        """
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Welcome to Library Management System!</h2>
            
            <p>Please verify your email address by clicking the button below:</p>
            
            <p style="margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #4CAF50; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Verify Email
                </a>
            </p>
            
            <p style="color: #666;">Or copy and paste this link:</p>
            <p style="color: #0066cc;">{verification_url}</p>
            
            <p style="color: #666; font-size: 12px;">
                This link will expire in 24 hours.
            </p>
            
            <p style="color: #666; font-size: 12px;">
                If you didn't create an account, please ignore this email.
            </p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 12px;">
                Best regards,<br>
                Library Management Team
            </p>
        </body>
        </html>
        """
        
        return await self.send_email(to, subject, html_body, html=True)
    
    async def send_password_reset_email(
        self,
        to: str,
        token: str,
    ) -> bool:
        """
        Send password reset email.
        
        Args:
            to: User's email address
            token: Reset token
            
        Returns:
            bool: True if sent successfully
        """
        reset_url = f"{self.settings.FRONTEND_URL}/reset-password?token={token}"
        
        subject = "Password Reset Request - Library Management System"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Password Reset Request</h2>
            
            <p>We received a request to reset your password.</p>
            
            <p>Click the button below to reset your password:</p>
            
            <p style="margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #f44336; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Reset Password
                </a>
            </p>
            
            <p style="color: #666;">Or copy and paste this link:</p>
            <p style="color: #0066cc;">{reset_url}</p>
            
            <p style="color: #666; font-size: 12px;">
                This link will expire in 1 hour.
            </p>
            
            <p style="color: #f44336; font-weight: bold;">
                If you didn't request this, please ignore this email and ensure your account is secure.
            </p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 12px;">
                Best regards,<br>
                Library Management Team
            </p>
        </body>
        </html>
        """
        
        return await self.send_email(to, subject, html_body, html=True)
    
    async def send_welcome_email(
        self,
        to: str,
        username: str,
    ) -> bool:
        """
        Send welcome email to new user.
        
        Args:
            to: User's email address
            username: User's username
            
        Returns:
            bool: True if sent successfully
        """
        subject = f"Welcome to Library Management System, {username}!"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Welcome, {username}! 📚</h2>
            
            <p>Your account has been successfully created and verified.</p>
            
            <h3>What you can do:</h3>
            <ul>
                <li>Browse our extensive catalog of books</li>
                <li>Borrow up to 5 books at a time</li>
                <li>Leave reviews and ratings</li>
                <li>Get personalized recommendations</li>
            </ul>
            
            <h3>Important Information:</h3>
            <ul>
                <li>Borrowing period: 14 days (can be extended once)</li>
                <li>Grace period: 3 days</li>
                <li>Late fees: €0.50 per day (max €50)</li>
            </ul>
            
            <p style="margin: 30px 0;">
                <a href="{self.settings.FRONTEND_URL}/catalog" 
                   style="background-color: #2196F3; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Browse Catalog
                </a>
            </p>
            
            <p>Happy reading!</p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 12px;">
                Best regards,<br>
                Library Management Team
            </p>
        </body>
        </html>
        """
        
        return await self.send_email(to, subject, html_body, html=True)
    
    async def send_suspension_email(
        self,
        to: str,
        reason: str,
        until: datetime,
    ) -> bool:
        """
        Send account suspension notification.
        
        Args:
            to: User's email address
            reason: Suspension reason
            until: Suspension end date
            
        Returns:
            bool: True if sent successfully
        """
        subject = "Account Suspension Notice - Library Management System"
        
        until_str = until.strftime("%B %d, %Y at %I:%M %p")
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #f44336;">Account Suspension Notice</h2>
            
            <p>Your account has been temporarily suspended.</p>
            
            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; 
                        padding: 15px; margin: 20px 0;">
                <strong>Reason:</strong> {reason}
            </div>
            
            <div style="background-color: #d1ecf1; border-left: 4px solid #0c5460; 
                        padding: 15px; margin: 20px 0;">
                <strong>Suspension ends:</strong> {until_str}
            </div>
            
            <p>During this period:</p>
            <ul>
                <li>You cannot borrow new books</li>
                <li>Please return any currently borrowed books</li>
                <li>Your account will be automatically reactivated after the suspension period</li>
            </ul>
            
            <p>If you believe this is an error or have questions, please contact the library administration.</p>
            
            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
            
            <p style="color: #666; font-size: 12px;">
                Library Management Team
            </p>
        </body>
        </html>
        """
        
        return await self.send_email(to, subject, html_body, html=True)
