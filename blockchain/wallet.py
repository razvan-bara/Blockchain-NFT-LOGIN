from multiversx_sdk_wallet import Mnemonic, UserWallet, UserPEM
from multiversx_sdk_core import Address
from pathlib import Path
import os

def saveWallet(userPEM, user_id):
    if not os.path.exists("./output"):
        os.mkdir("./output/")
        
    if not os.path.exists("./output/userWallets"):
        os.mkdir("./output/userWallets")

    os.mkdir("./output/userWallets/"+ str(user_id))

    userPEM.save(Path("./output/userWallets/"+str(user_id)+"/user_"+str(user_id)+"_wallet.pem"))

def generateWallet() -> UserPEM:
    mnemonic = Mnemonic.generate()
    words = mnemonic.get_words()

    wallet = UserWallet.from_mnemonic(mnemonic.get_text(), "password")

    secret_key = mnemonic.derive_key(0)
    public_key = secret_key.generate_public_key()

    label = Address(public_key.buffer, "erd").to_bech32()
    pem = UserPEM(label=label, secret_key=secret_key)

    return pem