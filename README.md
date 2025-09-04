# Payment Processor Race Condition Demo

This minimal codebase demonstrates a critical race condition that static analysis tools (SonarQube, pylint, bandit) fail to detect.

## The Issue

In `src/services/payment_processor.py`, the `process_payment()` function has a race condition:

```python
def process_payment(self, user, amount):
    # Check user can afford it
    if user.balance >= amount:
        # Log the attempt
        log.info(f"Payment {amount} for user {user.email}")
        
        # Charge the payment
        result = self.payment_api.charge(user.card_token, amount)
        
        # Update user balance
        user.balance -= amount
        db.save(user)
        
        # Send confirmation
        email.send(user.email, f"Charged ${amount}")
        
        # Record transaction
        db.save_transaction(user.id, amount, result.id)
        
        return {"success": True, "transaction": result.id}
    
    return {"success": False, "error": "Insufficient funds"}
```

## The Problem

This code has **non-atomic operations** that can cause:

1. **Double Charges**: Two concurrent requests can both pass the balance check before either updates it
2. **Lost Money**: System failure after charging but before saving = money taken but balance not updated
3. **Data Inconsistency**: If email/logging fails after charge, transaction state is corrupted

## Why Tools Miss This

Static analysis tools cannot detect:
- Race conditions requiring understanding of concurrent execution
- Business logic flaws about transaction atomicity
- State management issues across service boundaries

These require understanding the **semantic meaning** of payment processing, not just syntax patterns.