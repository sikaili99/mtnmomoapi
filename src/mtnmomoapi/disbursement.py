import os
import json
import requests
from uuid import uuid4
from basicauth import encode

class Disbursement:
    def __init__(self):
        self.disbursements_primary_key = os.environ.get('DISBURSEMENT_PRIMARY_KEY')
        self.api_key_disbursements = os.environ.get('DISBURSEMENT_API_SECRET')
        self.disbursements_apiuser = os.environ.get('DISBURSEMENT_USER_ID')
        self.environment_mode = os.environ.get('MTN_ENVIRONMENT', 'sandbox')
        self.callback_url = os.environ.get('CALLBACK_URL')
        self.base_url = os.environ.get('BASE_URL', 'https://sandbox.momodeveloper.mtn.com')
        self.currency = os.environ.get('CURRENCY', 'EUR')

        if not all([self.disbursements_primary_key, self.callback_url]):
            raise ValueError("Missing required environment variables")

        # Generate Basic authorization key when in test mode
        if self.environment_mode == "sandbox":
            self.disbursements_apiuser = str(uuid4())
            self._create_api_user()

        # Create basic key for disbursements
        self.username = self.disbursements_apiuser
        self.password = self.api_key_disbursements
        self.basic_authorisation_disbursements = str(encode(self.username, self.password))
        self._auth_token = None

    def _create_api_user(self):
        url = f"{self.base_url}/v1_0/apiuser"
        payload = {"providerCallbackHost": self.callback_url}
        headers = {
            'X-Reference-Id': self.disbursements_apiuser,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            if self.environment_mode == "sandbox":
                self.api_key_disbursements = response.json().get("apiKey")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create API user: {str(e)}")

    def authToken(self):
        if self._auth_token:
            return self._auth_token

        url = f"{self.base_url}/disbursement/token/"
        headers = {
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Authorization': self.basic_authorisation_disbursements
        }
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            self._auth_token = response.json()
            return self._auth_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get auth token: {str(e)}")

    def getBalance(self):
        url = f"{self.base_url}/disbursement/v1_0/account/balance"
        headers = {
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Authorization': f"Bearer {self.authToken()['access_token']}",
            'X-Target-Environment': self.environment_mode,
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get balance: {str(e)}")

    def transfer(self, amount, phone_number, external_id, payer_message='', payee_note=''):
        if not all([amount, phone_number, external_id]):
            raise ValueError("Missing required parameters")

        transaction_ref = str(uuid4())
        url = f"{self.base_url}/disbursement/v1_0/transfer"
        payload = {
            "amount": str(amount),
            "currency": self.currency,
            "externalId": str(external_id),
            "payee": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payer_message,
            "payeeNote": payee_note
        }
        
        headers = {
            'X-Reference-Id': transaction_ref,
            'X-Target-Environment': self.environment_mode,
            'X-Callback-Url': self.callback_url,
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.authToken()['access_token']}"
        }

        proxies = None
        if os.environ.get('QUOTAGUARDSTATIC_URL'):
            proxies = {
                "http": os.environ.get('QUOTAGUARDSTATIC_URL'),
                "https": os.environ.get('QUOTAGUARDSTATIC_URL')
            }

        try:
            response = requests.post(url, headers=headers, json=payload, proxies=proxies)
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "transaction_ref": transaction_ref
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Transfer failed: {str(e)}")

    def getTransactionStatus(self, transaction_ref):
        if not transaction_ref:
            raise ValueError("Transaction reference is required")

        url = f"{self.base_url}/disbursement/v1_0/transfer/{transaction_ref}"
        headers = {
            'X-Target-Environment': self.environment_mode,
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.authToken()['access_token']}"
        }

        proxies = None
        if os.environ.get('QUOTAGUARDSTATIC_URL'):
            proxies = {
                "http": os.environ.get('QUOTAGUARDSTATIC_URL'),
                "https": os.environ.get('QUOTAGUARDSTATIC_URL')
            }

        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "transaction_ref": transaction_ref,
                "data": response.json()
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get transaction status: {str(e)}")
            
