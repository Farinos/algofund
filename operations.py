from typing import Tuple, List
from urllib import response

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.logic import get_application_address
from algosdk import account, encoding

from pyteal import Txn, compileTeal, Mode

from account import Account
from contract import approval_program, clear_state_program
from util import fullyCompileContract, waitForTransaction
from datetime import date
from algosdk.transaction import PaymentTxn

APPROVAL_PROGRAM = b""
CLEAR_STATE_PROGRAM = b""

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

contract_address = str(
    "2B3I4PZIAH7N6PEQANWHZRALX35SRWNHULIVYEB335VW7X3PKW4CTBYFPY")
testnet_gh = "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI="

app_id = 4


def getContracts(client: AlgodClient) -> Tuple[bytes, bytes]:

    global APPROVAL_PROGRAM
    global CLEAR_STATE_PROGRAM

    if len(APPROVAL_PROGRAM) == 0:
        APPROVAL_PROGRAM = fullyCompileContract(client, approval_program())
        CLEAR_STATE_PROGRAM = fullyCompileContract(
            client, clear_state_program())

    return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM


def createDonationPool(
    client: AlgodClient,
    sender: Account,
    minAmount: int,
    expiryTime: int
) -> int:

    approval, clear = getContracts(client)
    senderAddress = sender.getAddress()

    globalSchema = transaction.StateSchema(num_uints=2, num_byte_slices=1)
    localSchema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_args = [
        senderAddress,
        minAmount,
        expiryTime
    ]

    txn = transaction.ApplicationCreateTxn(
        sender=senderAddress,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=globalSchema,
        local_schema=localSchema,
        app_args=app_args,
        sp=client.suggested_params()
    )

    signedTxn = txn.sign(sender.getPrivateKey())

    client.send_transaction(signedTxn)

    response = waitForTransaction(client, signedTxn.get_txid())
    assert response.applicationIndex is not None and response.applicationIndex > 0
    return response.applicationIndex


def fundPool(client: AlgodClient, sender: Account, amount: int):
    account_info = client.account_info(sender.addr)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    note = "Hello World".encode()

    unsigned_txn = PaymentTxn(sender.getAddress(), first=params.first, last=params.last,
                              gh=params.gh, receiver=contract_address, fee=params.fee * 2, amt=amount)
    signed_txn = unsigned_txn.sign(sender.getPrivateKey())

    txid = client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        confirmed_txn = wait_for_confirmation(client, txid, 4)
    except Exception as err:
        print(err)
        return

    account_info = client.account_info(contract_address)
    print("Final Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")


def withdrawFunds(client: AlgodClient, sender: Account):
    withdrawTxn = transaction.ApplicationCallTxn(
        sender=sender.getAddress(),
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[b"withdraw"],
        sp=client.suggested_params(),
    )

    signedTxn = withdrawTxn.sign(sender.getPrivateKey())
    client.send_transaction(signedTxn)

    waitForTransaction(client, signedTxn.get_txid())

# utility for waiting on a transaction confirmation


def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


_mnemonic = "chunk top humor ski derive outdoor dice library brush spoon twin surface rescue surprise kite climb space code color employ garden peace chuckle ability junior"
#_mnemonic = "roof depth upon brick organ panther panther plug permit original acoustic pottery call edge sheriff private clean error tobacco volcano found step present ability trap"
client = AlgodClient(algod_token, algod_address)
#pKey = Account.FromMnemonic(_mnemonic)[0]
user = Account.FromMnemonic(_mnemonic)

#createDonationPool(client, user, 5000, 1000000)
# getContracts(client)

#fundPool(client, user, 6051001)
withdrawFunds(client, user)
