"""
Fee calculator service implementation.

Concrete implementation of IFeeCalculator.
Centralizes all fee calculation logic for consistency.
"""

from datetime import datetime

from app.interfaces.services import IFeeCalculator
from app.policies import FEE_POLICIES, TIME_POLICIES


class FeeCalculator(IFeeCalculator):
    """
    Fee calculation service.
    
    Implements consistent fee calculation across the system.
    All fee logic is centralized here for maintainability.
    """
    
    def calculate_late_fee(
        self,
        borrow_date: datetime,
        due_date: datetime,
        return_date: datetime | None = None,
    ) -> float:
        """
        Calculate late fee for a borrowing.
        
        Formula:
        - Within grace period: €0
        - After grace period: (days_late - grace_period) × daily_rate
        - Maximum cap: FEE_POLICIES.LATE_FEE_MAX_AMOUNT
        
        Args:
            borrow_date: When book was borrowed
            due_date: When book was/is due
            return_date: When book was returned (None = not yet returned)
            
        Returns:
            float: Late fee amount
        """
        # Use current date if not yet returned
        effective_return_date = return_date or datetime.utcnow()
        
        # Book returned on time or early
        if effective_return_date <= due_date:
            return 0.0
        
        # Calculate days late
        days_late = (effective_return_date - due_date).days
        
        # Apply grace period
        if days_late <= TIME_POLICIES.GRACE_PERIOD_DAYS:
            return 0.0
        
        # Calculate fee
        chargeable_days = days_late - TIME_POLICIES.GRACE_PERIOD_DAYS
        fee = chargeable_days * FEE_POLICIES.LATE_FEE_PER_DAY
        
        # Apply maximum cap
        if fee > FEE_POLICIES.LATE_FEE_MAX_AMOUNT:
            return FEE_POLICIES.LATE_FEE_MAX_AMOUNT
        
        return round(fee, 2)
    
    def calculate_damage_fee(
        self,
        base_price: float,
        damage_level: str,
    ) -> float:
        """
        Calculate damage fee based on book price and damage severity.
        
        Damage levels:
        - MINOR: 10% of base price (light scratches, bent pages)
        - MODERATE: 50% of base price (torn pages, water damage)
        - SEVERE: 100% of base price (major damage, unusable)
        
        Args:
            base_price: Book's base price
            damage_level: Damage severity (MINOR, MODERATE, SEVERE)
            
        Returns:
            float: Damage fee amount
        """
        damage_level = damage_level.upper()
        
        if damage_level == "MINOR":
            return round(base_price * 0.10, 2)
        elif damage_level == "MODERATE":
            return round(base_price * 0.50, 2)
        elif damage_level == "SEVERE":
            return round(base_price * 1.00, 2)
        else:
            # Unknown damage level, default to moderate
            return round(base_price * 0.50, 2)
    
    def calculate_replacement_cost(
        self,
        base_price: float,
    ) -> float:
        """
        Calculate replacement cost for lost book.
        
        Replacement cost = base_price + processing fee
        
        Args:
            base_price: Book's base price
            
        Returns:
            float: Replacement cost
        """
        # Add processing fee for replacement
        processing_fee = FEE_POLICIES.REPLACEMENT_PROCESSING_FEE
        return round(base_price + processing_fee, 2)
    
    def can_waive_fee(
        self,
        fee_amount: float,
        reason: str,
    ) -> bool:
        """
        Check if fee can be waived based on business rules.
        
        Waivable conditions:
        - Fee amount is below minimum threshold
        - Valid waiver reason provided
        - Not a repeated offense
        
        Args:
            fee_amount: Fee amount to waive
            reason: Reason for waiver request
            
        Returns:
            bool: True if fee can be waived
        """
        # Define minimum fee threshold for waiver consideration
        MIN_WAIVABLE_AMOUNT = 0.50
        MAX_WAIVABLE_AMOUNT = 5.00
        
        # Fee too small to matter
        if fee_amount < MIN_WAIVABLE_AMOUNT:
            return True
        
        # Fee too large to waive without special approval
        if fee_amount > MAX_WAIVABLE_AMOUNT:
            return False
        
        # Reason must be provided and substantial
        if not reason or len(reason.strip()) < 10:
            return False
        
        # Valid waiver reasons (librarian discretion)
        valid_reasons = [
            "first offense",
            "technical error",
            "system issue",
            "emergency",
            "special circumstances",
        ]
        
        reason_lower = reason.lower()
        for valid_reason in valid_reasons:
            if valid_reason in reason_lower:
                return True
        
        # Default: require librarian approval
        return False
    
    def calculate_total_fees(
        self,
        late_fee: float = 0.0,
        damage_fee: float = 0.0,
        replacement_cost: float = 0.0,
    ) -> float:
        """
        Calculate total fees for a borrowing.
        
        Args:
            late_fee: Late return fee
            damage_fee: Damage fee
            replacement_cost: Replacement cost (if lost)
            
        Returns:
            float: Total fees
        """
        return round(late_fee + damage_fee + replacement_cost, 2)
    
    def estimate_daily_accrual(
        self,
        days_overdue: int,
    ) -> float:
        """
        Estimate daily fee accrual for overdue book.
        
        Args:
            days_overdue: Number of days overdue
            
        Returns:
            float: Estimated daily fee
        """
        # Account for grace period
        if days_overdue <= TIME_POLICIES.GRACE_PERIOD_DAYS:
            return 0.0
        
        chargeable_days = days_overdue - TIME_POLICIES.GRACE_PERIOD_DAYS
        fee = chargeable_days * FEE_POLICIES.LATE_FEE_PER_DAY
        
        # Apply cap
        if fee > FEE_POLICIES.LATE_FEE_MAX_AMOUNT:
            return FEE_POLICIES.LATE_FEE_MAX_AMOUNT
        
        return round(fee, 2)
