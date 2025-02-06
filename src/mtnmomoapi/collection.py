import os
from uuid import uuid4
import requests
import json
from basicauth import encode

class Collection:
    def __init__(self):
        self.collections_primary_key = os.environ.get('COLLECTION_PRIMARY_KEY')
        self.api_key_collections = os.environ.get('COLLECTION_API_SECRET')
        self.collections_apiuser = os.environ.get('COLLECTION_USER_ID')
        self.environment_mode = os.environ.get('MTN_ENVIRONMENT', 'sandbox')
        self.callback_url = os.environ.get('CALLBACK_URL')
        self.base_url = os.environ.get('BASE_URL', 'https://sandbox.momodeveloper.mtn.com')
        self.currency = os.environ.get('CURRENCY', 'EUR')

        if not all([self.collections_primary_key, self.callback_url]):
            raise ValueError("Missing required environment variables")

        # Generate Basic authorization key when in test mode
        if self.environment_mode == "sandbox":
            self.collections_apiuser = str(uuid4())
            self._create_api_user()

        # Create basic key for Collections
        self.username = self.collections_apiuser
        self.password = self.api_key_collections
        self.basic_authorisation_collections = str(encode(self.username, self.password))
        self._auth_token = None

    def _create_api_user(self):
        url = f"{self.base_url}/v1_0/apiuser"
        payload = {"providerCallbackHost": self.callback_url}
        headers = {
            'X-Reference-Id': self.collections_apiuser,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.collections_primary_key
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            if self.environment_mode == "sandbox":
                self.api_key_collections = response.json().get("apiKey")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create API user: {str(e)}")

    def authToken(self):
        if self._auth_token:
            return self._auth_token

        url = f"{self.base_url}/collection/token/"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Authorization': self.basic_authorisation_collections
        }
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            self._auth_token = response.json()
            return self._auth_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get auth token: {str(e)}")

    def requestToPay(self, amount, phone_number, external_id, payee_note="Payment", payer_message="Payment request"):
        if not all([amount, phone_number, external_id]):
            raise ValueError("Missing required parameters")

        transaction_ref = str(uuid4())
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        payload = {
            "amount": str(amount),
            "currency": self.currency,
            "externalId": external_id,
            "payer": {
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
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.authToken()['access_token']}"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "transaction_ref": transaction_ref
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request to pay failed: {str(e)}")

    def getTransactionStatus(self, transaction_ref):
        if not transaction_ref:
            raise ValueError("Transaction reference is required")

        url = f"{self.base_url}/collection/v1_0/requesttopay/{transaction_ref}"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Authorization': f"Bearer {self.authToken()['access_token']}",
            'X-Target-Environment': self.environment_mode,
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get transaction status: {str(e)}")

    def getBalance(self):
        url = f"{self.base_url}/collection/v1_0/account/balance"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Authorization': f"Bearer {self.authToken()['access_token']}",
            'X-Target-Environment': self.environment_mode,
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get balance: {str(e)}")
            
