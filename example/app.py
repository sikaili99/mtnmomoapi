from mtnmomoapi.collection import Collection
from mtnmomoapi.disbursement import Disbursement


def collection(amount,mobile_number):
    coll = Collection()
    response = coll.requestToPay(amount=amount,mobile_number=mobile_number)
    status_resposne = coll.getTransactionStatus(response['transaction_ref'])
    if status_resposne['status'] == "SUCCESS":
        pass #Do something here

    return status_resposne['status']

def disbursement(amount,mobile_number):
    disbur = Disbursement()
    response = disbur.transfer(amount=amount,mobile_number=mobile_number)
    transfer_status_res = disbur.getTransactionStatus(response['transaction_ref'])
    if transfer_status_res['status'] == "SUCCESS":
        pass #Do something here

    return transfer_status_res['status']
