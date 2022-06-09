from cmath import log
from crypt import crypt
from email import feedparser
import logging
from pyteal import *
from algosdk.future.transaction import PaymentTxn
from logging import *

# Txn.application_args are setted on creation transaction call

contract_address_2 = str("2B3I4PZIAH7N6PEQANWHZRALX35SRWNHULIVYEB335VW7X3PKW4CTBYFPY")
minAmount = Bytes("minAmount")


def approval_program():
    minAmount = Bytes("minAmount")
    # creator: donation creator
    # expiryDate: If time reach expiry date contract it will close automatically. If "minAmount" is reached funds goes to "creator" else all donators will refund
    # minAmount: minimum amount to close contract and take funds
    # maxAmount: if wallet reachs max amount algos will send to creator and smart contract will close
    handle_creation = Seq(
        App.globalPut(Bytes("creator"), Txn.application_args[0]),
        App.globalPut(Bytes("minAmount"), Btoi(Txn.application_args[1])),
        App.globalPut(Bytes("expiryDate"), Btoi(Txn.application_args[2])),
        Approve(),
    )

    withdraw = Seq(
        Assert(Global.creator_address() == Txn.sender()),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Balance(Global.current_application_address())
                - Global.min_txn_fee(),
                TxnField.receiver: Txn.sender(),
            }
        ),
        InnerTxnBuilder.Submit(),
        Approve(),
    )

    handle_noop = Cond([Txn.application_args[0] == Bytes("withdraw"), withdraw])

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        # [Txn.application_args[0] == Bytes("donate"), on_donate]
    )

    logging.debug("Approval Program")

    return program


def clear_state_program():
    return Reject()


# approval_program()
