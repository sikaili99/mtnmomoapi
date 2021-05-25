from mtnmomo.collection import Collection
from mtnmomo.disbursement import Disbursement

def collection_example(amount,mobile_number):

    response = Collection.requestToPay(amount,mobile_number)
    pay_status = Collection.getTransactionStatus(response['transaction_ref'])
    if pay_status['status'] == "SUCCESS":
        pass #Do something here

    return pay_status['status']

def disbursement_example(amount,mobile_number):
    response = Disbursement.transfer(amount,mobile_number)
    transfer_status = Disbursement.getTransactionStatus(response['transaction_ref'])
    if transfer_status['status'] == "SUCCESS":
        pass #Do something here

    return transfer_status['status']

