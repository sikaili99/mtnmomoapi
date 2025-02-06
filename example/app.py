from mtnmomoapi.collection import Collection
from mtnmomoapi.disbursement import Disbursement
from typing import Dict, Any, Optional

class MomoTransaction:
    def __init__(self):
        self.collection = Collection()
        self.disbursement = Disbursement()

    def process_collection(self, amount: str, mobile_number: str, external_id: str) -> Dict[str, Any]:
        try:
            # Input validation
            if not self._validate_inputs(amount, mobile_number, external_id):
                raise ValueError("Invalid input parameters")

            # Request payment
            payment_response = self.collection.requestToPay(
                amount=amount,
                phone_number=mobile_number,
                external_id=external_id
            )

            # Validate payment request response
            if payment_response["status_code"] != 202:
                raise Exception(f"Payment request failed with status {payment_response['status_code']}")

            # Get transaction status
            transaction_status = self._check_transaction_status(
                payment_response["transaction_ref"],
                is_collection=True
            )

            return {
                "success": True,
                "transaction_ref": payment_response["transaction_ref"],
                "status": transaction_status.get("status", "PENDING"),
                "details": transaction_status
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "validation_error"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "system_error"
            }

    def process_disbursement(self, amount: str, mobile_number: str, external_id: str) -> Dict[str, Any]:
        try:
            # Input validation
            if not self._validate_inputs(amount, mobile_number, external_id):
                raise ValueError("Invalid input parameters")

            # Check balance before disbursement
            balance = self.disbursement.getBalance()
            if not self._has_sufficient_balance(balance, amount):
                raise ValueError("Insufficient balance for disbursement")

            # Process transfer
            transfer_response = self.disbursement.transfer(
                amount=amount,
                phone_number=mobile_number,
                external_id=external_id
            )

            # Validate transfer response
            if transfer_response["status_code"] != 202:
                raise Exception(f"Transfer failed with status {transfer_response['status_code']}")

            # Get transaction status
            transaction_status = self._check_transaction_status(
                transfer_response["transaction_ref"],
                is_collection=False
            )

            return {
                "success": True,
                "transaction_ref": transfer_response["transaction_ref"],
                "status": transaction_status.get("status", "PENDING"),
                "details": transaction_status
            }

        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "validation_error"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "system_error"
            }

    def _validate_inputs(self, amount: str, mobile_number: str, external_id: str) -> bool:
        """Validate input parameters"""
        try:
            # Amount should be a valid number
            float(amount)
            
            # Mobile number validation (basic example - adjust according to your needs)
            if not mobile_number.isdigit() or len(mobile_number) < 9:
                return False
                
            # External ID should not be empty
            if not external_id:
                return False
                
            return True
        except ValueError:
            return False

    def _check_transaction_status(self, transaction_ref: str, is_collection: bool = True) -> Dict[str, Any]:
        """Check transaction status with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if is_collection:
                    status = self.collection.getTransactionStatus(transaction_ref)
                else:
                    status = self.disbursement.getTransactionStatus(transaction_ref)
                
                if status.get("status") in ["SUCCESSFUL", "FAILED"]:
                    return status
                    
                retry_count += 1
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise Exception(f"Failed to get transaction status after {max_retries} attempts: {str(e)}")
        
        return {"status": "PENDING"}

    def _has_sufficient_balance(self, balance: Dict[str, Any], amount: str) -> bool:
        """Check if there's sufficient balance for disbursement"""
        try:
            available_balance = float(balance.get("availableBalance", "0"))
            required_amount = float(amount)
            return available_balance >= required_amount
        except (ValueError, TypeError):
            return False

# Usage example
def main():
    momo = MomoTransaction()
    
    # Example collection
    collection_result = momo.process_collection(
        amount="100",
        mobile_number="260966456787",
        external_id="123456789"
    )
    print("Collection Result:", collection_result)
    
    # Example disbursement
    disbursement_result = momo.process_disbursement(
        amount="50",
        mobile_number="260966456787",
        external_id="987654321"
    )
    print("Disbursement Result:", disbursement_result)

if __name__ == "__main__":
    main()
