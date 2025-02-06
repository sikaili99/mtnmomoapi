# MTN MoMo API Python Client

<strong>Power your apps with Python MTN MoMo API</strong>

## Installation

Add the latest version of the library to your project:

```bash
pip install mtnmomoapi
```

This library supports Python 2.7+ or Python 3.4+

## Configuration

Before using the API, set up your environment variables:

```bash
# Base Configuration
export MTN_ENVIRONMENT="sandbox"  # or "mtnzambia" for production in Zambia
export BASE_URL="https://proxy.momoapi.mtn.com"  # Production URL
export CALLBACK_HOST="https://your-domain.com"
export CURRENCY="ZMW"  # "EUR" for sandbox, "ZMW" for Zambia production

# Collection API Keys
export COLLECTION_PRIMARY_KEY="your-primary-key"
export COLLECTION_USER_ID="your-user-id"
export COLLECTION_API_SECRET="your-api-secret"

# Disbursement API Keys
export DISBURSEMENT_PRIMARY_KEY="your-primary-key"
export DISBURSEMENT_USER_ID="your-user-id"
export DISBURSEMENT_API_SECRET="your-api-secret"
```

## Basic Usage Examples

### 1. Simple Collection Request

```python
from mtnmomoapi.collection import Collection

# Initialize the collection client
collection = Collection()

# Request payment
try:
    response = collection.requestToPay(
        amount="100",
        phone_number="260966456787",
        external_id="order-123",
        payee_note="Payment for Order #123",
        payer_message="Please pay for your order"
    )
    print(f"Transaction Reference: {response['transaction_ref']}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### 2. Simple Disbursement

```python
from mtnmomoapi.disbursement import Disbursement

# Initialize the disbursement client
disbursement = Disbursement()

# Transfer money
try:
    response = disbursement.transfer(
        amount="50",
        phone_number="260966456787",
        external_id="payout-123",
        payee_note="Refund for Order #123",
        payer_message="Your refund has been processed"
    )
    print(f"Transaction Reference: {response['transaction_ref']}")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Real-World Integration Examples

### 1. E-commerce Payment Processing

```python
from mtnmomoapi.collection import Collection
from typing import Dict, Any
import time

class EcommercePaymentProcessor:
    def __init__(self):
        self.collection = Collection()
        
    def process_order_payment(self, order_id: str, amount: str, customer_phone: str) -> Dict[str, Any]:
        try:
            # Request payment
            payment = self.collection.requestToPay(
                amount=amount,
                phone_number=customer_phone,
                external_id=f"order-{order_id}",
                payee_note=f"Payment for Order #{order_id}",
                payer_message="Please confirm payment for your order"
            )
            
            # Check payment status (with timeout)
            max_checks = 10
            check_interval = 5  # seconds
            
            for _ in range(max_checks):
                status = self.collection.getTransactionStatus(payment['transaction_ref'])
                
                if status.get('status') == 'SUCCESSFUL':
                    return {
                        'success': True,
                        'order_id': order_id,
                        'transaction_id': payment['transaction_ref'],
                        'status': 'paid'
                    }
                elif status.get('status') == 'FAILED':
                    return {
                        'success': False,
                        'order_id': order_id,
                        'error': 'Payment failed',
                        'status': 'failed'
                    }
                
                time.sleep(check_interval)
            
            return {
                'success': False,
                'order_id': order_id,
                'error': 'Payment timeout',
                'status': 'timeout'
            }
            
        except Exception as e:
            return {
                'success': False,
                'order_id': order_id,
                'error': str(e),
                'status': 'error'
            }

# Usage
processor = EcommercePaymentProcessor()
result = processor.process_order_payment(
    order_id="12345",
    amount="150.00",
    customer_phone="260966456787"
)
```

### 2. Salary Disbursement System

```python
from mtnmomoapi.disbursement import Disbursement
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalaryDisbursementSystem:
    def __init__(self):
        self.disbursement = Disbursement()
        
    def check_available_balance(self) -> float:
        try:
            balance = self.disbursement.getBalance()
            return float(balance.get('availableBalance', 0))
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            raise
            
    def process_payroll(self, payments: List[Dict[str, str]]) -> Dict[str, List]:
        successful_payments = []
        failed_payments = []
        
        # Check total required amount
        total_amount = sum(float(payment['amount']) for payment in payments)
        available_balance = self.check_available_balance()
        
        if available_balance < total_amount:
            raise ValueError(f"Insufficient balance. Required: {total_amount}, Available: {available_balance}")
        
        for payment in payments:
            try:
                # Process individual salary payment
                transfer = self.disbursement.transfer(
                    amount=payment['amount'],
                    phone_number=payment['phone_number'],
                    external_id=f"salary-{payment['employee_id']}",
                    payee_note=f"Salary for {payment['name']}",
                    payer_message="Monthly salary payment"
                )
                
                # Check transfer status
                status = self.disbursement.getTransactionStatus(transfer['transaction_ref'])
                
                if status.get('status') == 'SUCCESSFUL':
                    successful_payments.append({
                        'employee_id': payment['employee_id'],
                        'amount': payment['amount'],
                        'transaction_ref': transfer['transaction_ref']
                    })
                else:
                    failed_payments.append({
                        'employee_id': payment['employee_id'],
                        'amount': payment['amount'],
                        'error': 'Transfer failed'
                    })
                    
            except Exception as e:
                logger.error(f"Failed to process payment for employee {payment['employee_id']}: {str(e)}")
                failed_payments.append({
                    'employee_id': payment['employee_id'],
                    'amount': payment['amount'],
                    'error': str(e)
                })
                
        return {
            'successful': successful_payments,
            'failed': failed_payments
        }

# Usage Example
payroll_system = SalaryDisbursementSystem()

payments = [
    {
        'employee_id': 'EMP001',
        'name': 'John Doe',
        'amount': '1500.00',
        'phone_number': '260966456787'
    },
    {
        'employee_id': 'EMP002',
        'name': 'Jane Smith',
        'amount': '2000.00',
        'phone_number': '260966456788'
    }
]

try:
    result = payroll_system.process_payroll(payments)
    print(f"Successful payments: {len(result['successful'])}")
    print(f"Failed payments: {len(result['failed'])}")
except ValueError as e:
    print(f"Error: {str(e)}")
```

### 3. Subscription Payment System

```python
from mtnmomoapi.collection import Collection
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubscriptionManager:
    def __init__(self):
        self.collection = Collection()
        
    def process_subscription_payment(
        self,
        subscriber_id: str,
        phone_number: str,
        plan_amount: str,
        plan_name: str
    ) -> Dict[str, Any]:
        try:
            # Generate unique payment reference
            payment_ref = f"sub-{subscriber_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Request payment
            payment = self.collection.requestToPay(
                amount=plan_amount,
                phone_number=phone_number,
                external_id=payment_ref,
                payee_note=f"Subscription renewal: {plan_name}",
                payer_message=f"Please confirm payment for {plan_name} subscription"
            )
            
            # Monitor payment status
            max_attempts = 5
            attempt = 0
            
            while attempt < max_attempts:
                status = self.collection.getTransactionStatus(payment['transaction_ref'])
                
                if status.get('status') == 'SUCCESSFUL':
                    next_renewal = datetime.now() + timedelta(days=30)
                    return {
                        'success': True,
                        'subscriber_id': subscriber_id,
                        'transaction_ref': payment['transaction_ref'],
                        'plan_name': plan_name,
                        'amount_paid': plan_amount,
                        'next_renewal_date': next_renewal.strftime('%Y-%m-%d'),
                        'status': 'active'
                    }
                elif status.get('status') == 'FAILED':
                    return {
                        'success': False,
                        'subscriber_id': subscriber_id,
                        'error': 'Payment failed',
                        'status': 'payment_failed'
                    }
                
                attempt += 1
                time.sleep(5)
            
            return {
                'success': False,
                'subscriber_id': subscriber_id,
                'error': 'Payment timeout',
                'status': 'timeout'
            }
            
        except Exception as e:
            logger.error(f"Subscription payment failed for {subscriber_id}: {str(e)}")
            return {
                'success': False,
                'subscriber_id': subscriber_id,
                'error': str(e),
                'status': 'error'
            }

# Usage Example
subscription_manager = SubscriptionManager()

result = subscription_manager.process_subscription_payment(
    subscriber_id="SUB123",
    phone_number="260966456787",
    plan_amount="50.00",
    plan_name="Premium Monthly"
)

if result['success']:
    print(f"Subscription renewed successfully. Next renewal: {result['next_renewal_date']}")
else:
    print(f"Subscription renewal failed: {result['error']}")
```

## Best Practices

1. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Log errors for debugging
   - Provide meaningful error messages to users

2. **Transaction Monitoring**
   - Implement retry logic for status checks
   - Set appropriate timeouts
   - Store transaction references for reconciliation

3. **Security**
   - Never expose API keys in client-side code
   - Validate input data
   - Use HTTPS for callbacks

4. **Performance**
   - Implement caching where appropriate
   - Use asynchronous processing for bulk operations
   - Set up monitoring for API limits

## Common Issues and Solutions

1. **Transaction Timeout**
   ```python
   # Implement exponential backoff
   def check_transaction_with_backoff(transaction_ref, max_attempts=5):
       for attempt in range(max_attempts):
           try:
               status = collection.getTransactionStatus(transaction_ref)
               if status.get('status') in ['SUCCESSFUL', 'FAILED']:
                   return status
           except Exception:
               wait_time = (2 ** attempt) * 1  # exponential backoff
               time.sleep(wait_time)
       return {'status': 'TIMEOUT'}
   ```

2. **Balance Check**
   ```python
   def ensure_sufficient_balance(amount):
       try:
           balance = disbursement.getBalance()
           available = float(balance.get('availableBalance', 0))
           required = float(amount)
           if available < required:
               raise ValueError(f"Insufficient balance: {available} < {required}")
           return True
       except Exception as e:
           logger.error(f"Balance check failed: {str(e)}")
           raise
   ```

3. **Input Validation**
   ```python
   def validate_phone_number(phone):
       # Adjust pattern based on your country's format
       pattern = r'^26096\d{7}$'
       if not re.match(pattern, phone):
           raise ValueError("Invalid phone number format")
       return True
   ```

## Testing

```python
import unittest
from unittest.mock import patch
from mtnmomoapi.collection import Collection

class TestMomoAPI(unittest.TestCase):
    def setUp(self):
        self.collection = Collection()
        
    @patch('mtnmomoapi.collection.Collection.requestToPay')
    def test_payment_request(self, mock_request):
        mock_request.return_value = {
            'status_code': 202,
            'transaction_ref': 'test-ref'
        }
        
        response = self.collection.requestToPay(
            amount="100",
            phone_number="260966456787",
            external_id="test-123"
        )
        
        self.assertEqual(response['status_code'], 202)
        self.assertTrue('transaction_ref' in response)

if __name__ == '__main__':
    unittest.main()
```

## Support

For issues and feature requests, please visit our [GitHub repository](https://github.com/sikaili99/mtnmomoapi/issues).

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
