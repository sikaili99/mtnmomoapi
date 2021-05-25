from os import stat
from mtnmomo.collection import Collection
from mtnmomo.disbursement import Disbursement

def collection_example(amount,mobile_number):

    response = Collection.requestToPay(amount,mobile_number)
    status = Collection.getTransactionStatus(response['transaction_ref'])
    if status['status'] == "SUCCESS":
        pass #Do something here

    return status['status']

def disbursement_example(amount,mobile_number):
    response = Disbursement.transfer(amount,mobile_number)
    status = Disbursement.getTransactionStatus(response['transaction_ref'])
    if status['status'] == "SUCCESS":
        pass #Do something here

    return status['status']
