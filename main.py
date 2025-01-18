from multiversx_sdk_wallet import Mnemonic, UserWallet, UserPEM, UserSigner
from multiversx_sdk_core import Address, TransactionComputer, TokenComputer
from multiversx_sdk_core.transaction_factories import SmartContractTransactionsFactory, TransactionsFactoryConfig
from multiversx_sdk_network_providers import ProxyNetworkProvider
from multiversx_sdk_core.transaction_builders.relayed_v2_builder import RelayedTransactionV2Builder

from pathlib import Path

WALLET_PATH = Path("pyWallet.pem")
provider = ProxyNetworkProvider("https://testnet-api.multiversx.com")

def generateAndSaveWallet():
    mnemonic = Mnemonic.generate()
    words = mnemonic.get_words()

    wallet = UserWallet.from_mnemonic(mnemonic.get_text(), "password")

    secret_key = mnemonic.derive_key(0)
    public_key = secret_key.generate_public_key()

    label = Address(public_key.buffer, "erd").to_bech32()
    pem = UserPEM(label=label, secret_key=secret_key)
    pem.save(WALLET_PATH)

def getAccountBalance(account):

    pem = UserPEM.from_file(account)
    owner = pem.public_key.to_address("erd")
    account_on_network = provider.get_account(owner)

    print("Nonce:", account_on_network.nonce)
    print("Balance:", account_on_network.balance)

def createNFTCollection(sender):

    signer = UserSigner.from_pem_file(Path(sender))
    pem = UserPEM.from_file(sender)

    senderAddress = pem.public_key.to_address("erd")

    config = provider.get_network_config()
    sc_factory = SmartContractTransactionsFactory(config, TokenComputer())

    sc_address = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u")

    NFT_COLLECTION_NAME = 0x6578616d706c65525a564e
    NFT_TICKER = 0x525a56544b
    tx = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=sc_address,
        function="issueNonFungible",
        native_transfer_amount=50000000000000000,
        gas_limit=60000000,
        arguments=[NFT_COLLECTION_NAME, NFT_TICKER]
    )

    sender_on_network = provider.get_account(senderAddress)
    tx.nonce = sender_on_network.nonce

    transaction_computer = TransactionComputer()
    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

    hash = provider.send_transaction(tx)

    print("Transaction:", tx.__dict__)
    print("Transaction data:", tx.data)
    print("Transaction hash:", hash)

# createNFTCollection(WALLET_PATH)
# getAccountBalance(WALLET_PATH)

# def giveNFTCreationRole(sender): 

#     signer = UserSigner.from_pem_file(Path(sender))
#     pem = UserPEM.from_file(sender)

#     senderAddress = pem.public_key.to_address("erd")

#     config = provider.get_network_config()
#     sc_factory = SmartContractTransactionsFactory(config, TokenComputer())

#     sc_address = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u")

#     config = provider.get_network_config()
#     sc_factory = SmartContractTransactionsFactory(config, TokenComputer())
#     sc_address = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u")

#     NFT_TICKER = 0x525a56544b2d343161396566
#     NFT_CREATOR_ROLE = 0x45534454526f6c654e4654437265617465
#     NFT_RECIEVER_ROLE = int(senderAddress.to_hex(), 16)

#     tx = sc_factory.create_transaction_for_execute(
#         sender=senderAddress,
#         contract=sc_address,
#         function="setSpecialRole",
#         gas_limit=60000000,
#         arguments=[NFT_TICKER, NFT_RECIEVER_ROLE, NFT_CREATOR_ROLE]
#     )

#     sender_on_network = provider.get_account(senderAddress)
#     tx.nonce = sender_on_network.nonce

#     transaction_computer = TransactionComputer()
#     tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

#     provider.send_transaction(tx)

# giveNFTCreationRole(WALLET_PATH)
    
def createNFTForCollection(sender, nft_name : str): 

    signer = UserSigner.from_pem_file(Path(sender))
    pem = UserPEM.from_file(sender)

    senderAddress = pem.public_key.to_address("erd")

    config = provider.get_network_config()
    sc_factory = SmartContractTransactionsFactory(config, TokenComputer())

    NFT_COLLECTION_ID = 0x525a56544b2d343161396566
    NFT_QUANTITY = 0x1
    NFT_NAME = int(nft_name.encode().hex(), 16)
    NFT_ROYALTIES = 0x1000
    NFT_HASH = 0x0
    NFT_ATTRIBUTES = 0x6d657461646174613a697066734349442f6e66745f61747472732e6a736f6e3b746167733a6465736372697074696f6e2c61747472696275746573
    NFT_URI = 0x2e2f6e6674696d672e6a7067
    
    # hel = "metadata:ipfsCID/nft_attrs.json;tags:description,attributes"
    tx = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=senderAddress,
        function="ESDTNFTCreate",
        gas_limit=55000000,
        arguments=[NFT_COLLECTION_ID, NFT_QUANTITY, NFT_NAME, NFT_ROYALTIES, NFT_HASH, NFT_ATTRIBUTES, NFT_URI]
    )

    sender_on_network = provider.get_account(senderAddress)
    tx.nonce = sender_on_network.nonce

    transaction_computer = TransactionComputer()
    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

    hash = provider.send_transaction(tx)
    got_tx = provider.get_transaction(hash)
    print(got_tx.status)
    while(got_tx.status == "pending"):
        print("Waiting for transaction to be mined...")
    print("Finish")

# createNFTForCollection(WALLET_PATH, "WaitingNFT")
    
# def nftTransfer(sender): 

#     signer = UserSigner.from_pem_file(Path(sender))
#     pem = UserPEM.from_file(sender)

#     senderAddress = pem.public_key.to_address("erd")

#     config = provider.get_network_config()
#     sc_factory = SmartContractTransactionsFactory(config, TokenComputer())

#     NFT_COLLECTION_ID = 0x525a56544b2d343161396566
#     NFT_NONCE = 0x1
#     NFT_QTY = 0x1
#     NFT_RECIEVER = int(Address.from_bech32("erd10n5e3ky42hmjly4y6svrupszgwd87sg84skdt02ttxu9fxpfvg8sr86n7g").to_hex(), 16)
    
#     tx = sc_factory.create_transaction_for_execute(
#         sender=senderAddress,
#         contract=senderAddress,
#         function="ESDTNFTTransfer",
#         gas_limit=55000000,
#         arguments=[NFT_COLLECTION_ID, NFT_NONCE, NFT_QTY, NFT_RECIEVER]
#     )

#     sender_on_network = provider.get_account(senderAddress)
#     tx.nonce = sender_on_network.nonce

#     transaction_computer = TransactionComputer()
#     tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

#     provider.send_transaction(tx)

# nftTransfer(WALLET_PATH)
    
def getNFTIdentifier(sender):
    pem = UserPEM.from_file(sender)

    address = Address.new_from_bech32("erd1gyvz7fvmuc8xh2xjld9r5jfx0w9ewagmav6jdgzzqf9kq25ug34sd32nqc")
    print(address.to_bech32())
    nfts = provider.get_nonfungible_tokens_of_account(address)
    
    print(nfts[-1].__dict__)

getNFTIdentifier(WALLET_PATH)