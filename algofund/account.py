from algosdk import account, mnemonic

class Account:
    """Represents a private key and address for an Algorand account"""

    def __init__(self, privateKey: str) -> None:
        self.sk = privateKey
        self.addr = account.address_from_private_key(privateKey)

    def getAddress(self) -> str:
        return self.addr

    def getPrivateKey(self) -> str:
        return self.sk

    def getMnemonic(self) -> str:
        return mnemonic.from_private_key(self.sk)

    @classmethod
    def FromMnemonic(cls, m: str) -> "Account":
        return cls(mnemonic.to_private_key(m))


if __name__ == '__main__':
    _mnemonic = "blanket cruise impose property thing fatal exhaust salad ship frozen similar mesh term noise coral nest cool just stool cream whisper poet box ability true"
    addr = Account.FromMnemonic(_mnemonic)
    print(addr)
