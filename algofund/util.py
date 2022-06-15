from typing import List, Tuple, Dict, Any, Optional, Union
from base64 import b64decode

from algosdk.v2client.algod import AlgodClient

from algosdk import encoding, kmd, mnemonic, constants
from algosdk.wallet import Wallet
from account import *
from pyteal import compileTeal, Mode, Expr


class PendingTxnResponse:
    def __init__(self, response: Dict[str, Any]) -> None:
        self.poolError: str = response["pool-error"]
        self.txn: Dict[str, Any] = response["txn"]

        self.applicationIndex: Optional[int] = response.get("application-index")
        self.assetIndex: Optional[int] = response.get("asset-index")
        self.closeRewards: Optional[int] = response.get("close-rewards")
        self.closingAmount: Optional[int] = response.get("closing-amount")
        self.confirmedRound: Optional[int] = response.get("confirmed-round")
        self.globalStateDelta: Optional[Any] = response.get("global-state-delta")
        self.localStateDelta: Optional[Any] = response.get("local-state-delta")
        self.receiverRewards: Optional[int] = response.get("receiver-rewards")
        self.senderRewards: Optional[int] = response.get("sender-rewards")

        self.innerTxns: List[Any] = response.get("inner-txns", [])
        self.logs: List[bytes] = [b64decode(l) for l in response.get("logs", [])]


class ContractUtils:
    # Returns KMDCClient used to handle wallet requests
    # The Key Management Daemon (kmd) is a low level wallet and key management tool
    # https://developer.algorand.org/docs/clis/kmd/

    @staticmethod
    def keyManagement():
        kmd_address = "http://localhost:4002"
        kmd_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        kmd_client = kmd.KMDClient(kmd_token, kmd_address)
        return kmd_client

    # Returns Wallet
    @staticmethod
    def walletDetails():
        wallet_name = "unencrypted-default-wallet"
        password = ""
        kmd_client = ContractUtils.keyManagement()
        return Wallet(wallet_name, password, kmd_client)

    # Retrieve accounts associated to wallet
    @staticmethod
    def getAddresses():
        walletid = None
        accountArray = []

        wallet = ContractUtils.walletDetails()

        for key in wallet.list_keys():
            walletid = wallet.kcl.list_wallets()[0].get("id")

            wallethandle = wallet.kcl.init_wallet_handle(walletid, "")
            accountkey = wallet.kcl.export_key(wallethandle, "", key)
            mn = mnemonic.from_private_key(accountkey)
            account = Account.FromMnemonic(mn)
            account.mnemonic = account.getMnemonic()
            accountArray.append(account)

        return accountArray

    # Return the escrow address of an application.
    # Args: appID (int): The ID of the application.
    # Returns: str: The address corresponding to that application's escrow account.
    @staticmethod
    def get_application_address(appID: int) -> str:
        to_sign = constants.APPID_PREFIX + appID.to_bytes(8, "big")
        checksum = encoding.checksum(to_sign)
        return encoding.encode_address(checksum)

    @staticmethod
    def decodeState(stateArray: List[Any]) -> Dict[bytes, Union[int, bytes]]:
        state: Dict[bytes, Union[int, bytes]] = dict()

        for pair in stateArray:
            key = b64decode(pair["key"])

            value = pair["value"]
            valueType = value["type"]

            if valueType == 2:
                # value is uint64
                value = value.get("uint", 0)
            elif valueType == 1:
                # value is byte array
                value = b64decode(value.get("bytes", ""))
            else:
                raise Exception(f"Unexpected state type: {valueType}")

            state[key] = value

        return state

    # Returns contract bytecode
    @staticmethod
    def fullyCompileContract(client: AlgodClient, contract: Expr) -> bytes:
        teal = compileTeal(contract, mode=Mode.Application, version=5)
        response = client.compile(teal)
        return b64decode(response["result"])

    # Return pending transaction
    @staticmethod
    def waitForTransaction(
        client: AlgodClient, txID: str, timeout: int = 10
    ) -> PendingTxnResponse:
        lastStatus = client.status()
        lastRound = lastStatus["last-round"]
        startRound = lastRound

        while lastRound < startRound + timeout:
            pending_txn = client.pending_transaction_info(txID)

            if pending_txn.get("confirmed-round", 0) > 0:
                return PendingTxnResponse(pending_txn)

            if pending_txn["pool-error"]:
                raise Exception("Pool error: {}".format(pending_txn["pool-error"]))

            lastStatus = client.status_after_block(lastRound + 1)

            lastRound += 1

        raise Exception(
            "Transaction {} not confirmed after {} rounds".format(txID, timeout)
        )

    # Returns application state
    @staticmethod
    def getAppGlobalState(
        client: AlgodClient, appID: int
    ) -> Dict[bytes, Union[int, bytes]]:
        appInfo = client.application_info(appID)
        return ContractUtils.decodeState(appInfo["params"]["global-state"])
