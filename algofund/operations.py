from typing import Tuple, List
from urllib import response

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.logic import get_application_address
from algosdk import account, encoding

from pyteal import Txn, compileTeal, Mode

from account import Account
from contract import approval_program, clear_state_program
from util import ContractUtils
from datetime import date
from algosdk.transaction import PaymentTxn

APPROVAL_PROGRAM = b""
CLEAR_STATE_PROGRAM = b""

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
contract_address = "TBXCKFOFZWMTTB3MJOZGECCJDIGIJW2E3QTLJV2SP5GOGEPTOZY4UH562M"
# contract_address = str("2B3I4PZIAH7N6PEQANWHZRALX35SRWNHULIVYEB335VW7X3PKW4CTBYFPY")
testnet_gh = "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI="

app_id = 33


def getContracts(client: AlgodClient) -> Tuple[bytes, bytes]:

    global APPROVAL_PROGRAM
    global CLEAR_STATE_PROGRAM

    if len(APPROVAL_PROGRAM) == 0:
        APPROVAL_PROGRAM = ContractUtils.fullyCompileContract(client, approval_program())
        CLEAR_STATE_PROGRAM = ContractUtils.fullyCompileContract(client, clear_state_program())

    return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM


def createDonationPool(
    client: AlgodClient, sender: Account, minAmount: int, expiryTime: int
) -> int:

    approval, clear = getContracts(client)
    senderAddress = sender.getAddress()

    globalSchema = transaction.StateSchema(num_uints=2, num_byte_slices=1)
    localSchema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_args = [senderAddress, minAmount, expiryTime]

    txn = transaction.ApplicationCreateTxn(
        sender=senderAddress,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=globalSchema,
        local_schema=localSchema,
        app_args=app_args,
        sp=client.suggested_params(),
    )

    signedTxn = txn.sign(sender.getPrivateKey())

    client.send_transaction(signedTxn)

    response = ContractUtils.waitForTransaction(client, signedTxn.get_txid())
    assert response.applicationIndex is not None and response.applicationIndex > 0
    return response.applicationIndex


def fundPool(client: AlgodClient, sender: Account, contractAddr: str, amount: int):
    account_info = client.account_info(sender.addr)
    print("Account balance: {} microAlgos".format(account_info.get("amount")))

    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    unsigned_txn = PaymentTxn(
        sender.getAddress(),
        first=params.first,
        last=params.last,
        gh=params.gh,
        receiver=contractAddr,
        fee=params.fee * 2,
        amt=amount,
    )
    signed_txn = unsigned_txn.sign(sender.getPrivateKey())

    txid = client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        return wait_for_confirmation(client, txid, 2)
    except Exception as err:
        print(err)
        return None


def withdrawFunds(client: AlgodClient, applicationIndex: int, sender: Account) -> bool:
    withdrawTxn = transaction.ApplicationCallTxn(
        sender=sender.getAddress(),
        index=applicationIndex,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=[b"withdraw"],
        sp=client.suggested_params(),
    )

    signedTxn = withdrawTxn.sign(sender.getPrivateKey())
    client.send_transaction(signedTxn)

    try:
        ContractUtils.waitForTransaction(client, signedTxn.get_txid())
        return True
    except:
        return False


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
            raise Exception("pool error: {}".format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception(
        "pending tx not found in timeout rounds, timeout value = : {}".format(timeout)
    )


if __name__ == "__main__":
    _mnemonic = "chunk top humor ski derive outdoor dice library brush spoon twin surface rescue surprise kite climb space code color employ garden peace chuckle ability junior"
    # _mnemonic = "roof depth upon brick organ panther panther plug permit original acoustic pottery call edge sheriff private clean error tobacco volcano found step present ability trap"
    client = AlgodClient(algod_token, algod_address)
    # pKey = Account.FromMnemonic(_mnemonic)[0]
    user = Account.FromMnemonic(_mnemonic)

    # createDonationPool(client, user, 1000000, 1000003)
    # adrs = get_application_address(1)
    # print(adrs)
    # getContracts(client)
    # wlt = wallet_details()
    # print(wlt)
    # accnts = testMnemonic()

    # print(accnts)
    # address = get_application_address(33)
    # fundPool(client, user, address, 10000666)
    # withdrawFunds(client, user)
    state = ContractUtils.getAppGlobalState(client, 33)
    print("")
