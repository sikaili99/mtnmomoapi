import os
from uuid import uuid4
import requests
import json
from uuid import uuid4
from basicauth import encode


class Collection:
    def __init__(self):
        self.collections_primary_key = os.environ.get('COLLECTION_PRIMARY_KEY')
        self.api_key_collections = os.environ.get('COLLECTION_API_SECRET')
        self.collections_apiuser = os.environ.get('COLLECTION_USER_ID')
        self.environment_mode = os.environ.get('MTN_ENVIRONMENT')
        self.base_url = os.environ.get('BASE_URL')
        if self.environment_mode == "sandbox":
            self.base_url = "https://sandbox.momodeveloper.mtn.com"

        # Generate Basic authorization key when in test mode
        if self.environment_mode == "sandbox":
            self.collections_apiuser = str(uuid4())

        # Create API user
        self.url = f"{self.base_url}/v1_0/apiuser"
        payload = json.dumps({
            "providerCallbackHost": os.environ.get('')
        })
        self.headers = {
            'X-Reference-Id': self.collections_apiuser,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.collections_primary_key
        }
        response = requests.post(self.url, headers=self.headers, data=payload)

        # Auto-generate when in test mode
        if self.environment_mode == "sandbox":
            self.api_key_collections = str(response["apiKey"])

        # Create basic key for Collections
        self.username, self.password = self.collections_apiuser, self.api_key_collections
        self.basic_authorisation_collections = str(encode(self.username, self.password))

    def authToken(self):
        url = f"{self.base_url}/collection/token/"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Authorization': self.basic_authorisation_collections
        }
        response = requests.post(url, headers=headers, data=payload).json()
        return response

    def requestToPay(self, amount, phone_number, external_id,payernote="SPARCO", payermessage="SPARCOPAY"):
        uuidgen = str(uuid4())
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        payload = json.dumps({
            "amount": amount,
            "currency": os.environ.get('CURRENCY'),
            "externalId": external_id,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payermessage,
            "payeeNote": payernote
        })
        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': self.environment_mode,
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + str(self.authToken()["access_token"])
        }
        response = requests.post(url, headers=headers, data=payload)

        context = {"status_code": response.status_code,"ref": uuidgen}
        return context

    def getTransactionStatus(self, txn):
        url = f"{self.base_url}/collection/v1_0/requesttopay/{txn}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
        'Authorization': f"Bearer {self.authToken()['access_token']}",
            'X-Target-Environment': self.environment_mode,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_respon = response.json()
        return json_respon

    # Check momo collections balance
    def getBalance(self):
        url = f"{self.base_url}/collection/v1_0/account/balance"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_primary_key,
            'Authorization':  f"Bearer {self.authToken()['access_token']}",
            'X-Target-Environment': self.environment_mode,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_respon = response.json()
        return json_respon
