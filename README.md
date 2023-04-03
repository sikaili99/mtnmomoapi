# MTN MoMo API Python Client</h1>

<strong>Power your apps with Python MTN MoMo API</strong>

# Usage

## Installation

Add the latest version of the library to your project:

```bash
 $ pip install mtnmomoapi
```

This library supports Python 2.7+ or Python 3.4+

# Sandbox Environment

## Creating a sandbox environment API user 

Next, we need to get the `User ID` and `User Secret` and to do this we shall need to use the Primary Key for the Product to which we are subscribed, as well as specify a host. The library ships with a commandline application that helps to create sandbox credentials. It assumes you have created an account on `https://momodeveloper.mtn.com` and have your `Ocp-Apim-Subscription-Key`. 

These are the credentials we shall use for the sandbox environment. In production, these credentials are provided for you on the MTN OVA management dashboard after KYC requirements are met.

## Configuration

Before we can fully utilize the library, we need to specify global configurations. The global configuration must contain the following:

* `BASE_URL`: An optional base url to the MTN Momo API. By default the staging base url will be used
* `ENVIRONMENT`: Optional environment, either "sandbox" or "production". Default is 'sandbox'
* `CALLBACK_HOST`: The domain where you webhooks urls are hosted. This is mandatory.

Once you have specified the global variables, you can now provide the product-specific variables. Each MoMo API product requires its own authentication details i.e its own `Subscription Key`, `User ID` and `User Secret`, also sometimes refered to as the `API Secret`. As such, we have to configure subscription keys for each product you will be using. 

The full list of configuration options can be seen in the example below:

 ```python
 config = {
    "MTN_ENVIRONMENT": os.environ.get("MTN_ENVIRONMENT"), 
    "BASE_URL": os.environ.get("BASE_URL"), 
    "CALLBACK_HOST": os.environ.get("CALLBACK_HOST"), # Mandatory.
    "COLLECTION_PRIMARY_KEY": os.environ.get("COLLECTION_PRIMARY_KEY"), 
    "COLLECTION_USER_ID": os.environ.get("COLLECTION_USER_ID"),
    "COLLECTION_API_SECRET": os.environ.get("COLLECTION_API_SECRET"),
    "REMITTANCE_USER_ID": os.environ.get("REMITTANCE_USER_ID"), 
    "REMITTANCE_API_SECRET": os.environ.get("REMITTANCE_API_SECRET"),
    "REMITTANCE_PRIMARY_KEY": os.envieon.get("REMITTANCE_PRIMARY_KEY"),
    "DISBURSEMENT_USER_ID": os.environ.get("DISBURSEMENT_USER_ID"), 
    "DISBURSEMENT_API_SECRET": os.environ.get("DISBURSEMENTS_API_SECRET"),
    "DISBURSEMENT_PRIMARY_KEY": os.environ.get("DISBURSEMENT_PRIMARY_KEY"), 
}
```

You will only need to configure the variables for the product(s) you will be using.

## Collections

The collections client can be created with the following paramaters. Note that the `COLLECTION_USER_ID` and `COLLECTION_API_SECRET` for production are provided on the MTN OVA dashboard;

* `COLLECTION_PRIMARY_KEY`: Primary Key for the `Collection` product on the developer portal.
* `COLLECTION_USER_ID`: For sandbox, use the one generated with the `mtnmomo` command.
* `COLLECTION_API_SECRET`: For sandbox, use the one generated with the `mtnmomo` command.

You can create a collection client with the following:

```python
import os
from mtnmomo.collection import Collection

client = Collection()
```

### Methods

1. `requestToPay`: This operation is used to request a payment from a consumer (Payer). The payer will be asked to authorize the payment. The transaction is executed once the payer has authorized the payment. The transaction will be in status PENDING until it is authorized or declined by the payer or it is timed out by the system. Status of the transaction can be validated by using `getTransactionStatus`.

2. `getTransactionStatus`: Retrieve transaction information using the `transactionId` returned by `requestToPay`. You can invoke it at intervals until the transaction fails or succeeds. If the transaction has failed, it will throw an appropriate error. 

3. `getBalance`: Get the balance of the account.

### TODO: create this methode

`isPayerActive`: check if an account holder is registered and active in the system.

### Sample Code

```python
import os
from mtnmomo.collection import Collection

client = Collection()

response = client.requestToPay(amount="600", phone_number="0966456787", external_id="123456789", payee_note="dd", payer_message="dd", currency="EUR")
```

## Disbursement

The Disbursements client can be created with the following paramaters. Note that the `DISBURSEMENT_USER_ID` and `DISBURSEMENT_API_SECRET` for production are provided on the MTN OVA dashboard;

* `DISBURSEMENT_PRIMARY_KEY`: Primary Key for the `Disbursement` product on the developer portal.
* `DISBURSEMENT_USER_ID`: For sandbox, use the one generated with the `mtnmomo` command.
* `DISBURSEMENT_API_SECRET`: For sandbox, use the one generated with the `mtnmomo` command.

You can create a disbursements client with the following

```python
import os
from mtnmomo.disbursement import Disbursement

client = Disbursement()
```

### Methods

1. `transfer`: Used to transfer an amount from the owner’s account to a payee account. Status of the transaction can be validated by using the `getTransactionStatus` method.

2. `getTransactionStatus`: Retrieve transaction information using the `transactionId` returned by `transfer`. You can invoke it at intervals until the transaction fails or succeeds.

2. `getBalance`: Get your account balance.

### TODO: create this methode

`isPayerActive`: This method is used to check if an account holder is registered and active in the system.

#### Sample Code

```python
import os
from mtnmomo.disbursement import Disbursement

client = Disbursement()
response = client.transfer(amount="600", phone_number="0966456787", external_id="123456789", payee_note="dd",      payer_message="dd", currency="EUR")

```

Keep coding!
