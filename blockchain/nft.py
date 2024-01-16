from multiversx_sdk_wallet import UserPEM, UserSigner
from multiversx_sdk_core import Address, TransactionComputer, TokenComputer
from multiversx_sdk_core.transaction_factories import SmartContractTransactionsFactory
from multiversx_sdk_network_providers import ProxyNetworkProvider
from blockchain.provider import provider 
from models.user import User
from pathlib import Path

NFT_IDENTIFIER = 0x525a56544b2d343161396566
NFT_CREATOR_USER_WALLET = Path("./pyWallet.pem")
NFT_CREATOR_ROLE = 0x45534454526f6c654e4654437265617465

config = provider.get_network_config()
sc_factory = SmartContractTransactionsFactory(config, TokenComputer())

def getNFTsOwnerAddress() -> Address:
    return UserPEM.from_pem_file(NFT_CREATOR_USER_WALLET).public_key.to_address("erd")

def  generateNFT(nft_name : str):

    signer = UserSigner.from_pem_file(NFT_CREATOR_USER_WALLET)
    sender = UserPEM.from_file(NFT_CREATOR_USER_WALLET)
    senderAddress = sender.public_key.to_address("erd")

    NFT_QUANTITY = 0x1
    NFT_NAME = int(nft_name.encode().hex(), 16)
    NFT_ROYALTIES = 0x1000
    NFT_HASH = 0x0
    NFT_ATTRIBUTES = 0x6d657461646174613a697066734349442f6e66745f61747472732e6a736f6e3b746167733a6465736372697074696f6e2c61747472696275746573
    NFT_URI = 0x2e2f6e6674696d672e6a7067
    
    tx = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=senderAddress,
        function="ESDTNFTCreate",
        gas_limit=55000000,
        arguments=[NFT_IDENTIFIER, NFT_QUANTITY, NFT_NAME, NFT_ROYALTIES, NFT_HASH, NFT_ATTRIBUTES, NFT_URI]
    )

    sender_on_network = provider.get_account(senderAddress)
    tx.nonce = sender_on_network.nonce

    transaction_computer = TransactionComputer()
    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

    hash = provider.send_transaction(tx)
    got_tx = provider.get_transaction(hash)
    status = got_tx.status
    while(status == "pending"):
        print("Waiting for transaction to be mined...")
        status = provider.get_transaction(hash).status
    print("Finish")

def transferLatestNFT(reciever : User) -> int:
    print("Transfering NFT to " + reciever.address)
    
    signer = UserSigner.from_pem_file(NFT_CREATOR_USER_WALLET)
    sender = UserPEM.from_file(NFT_CREATOR_USER_WALLET)

    senderAddress = sender.public_key.to_address("erd")

    address = Address.new_from_bech32("erd1q9697er823ykyrn9hnmdppc9y0fegrkfy4qz4k94ywlx8d5r2uvsryy45j")
    print(address.to_bech32())
    nfts = provider.get_nonfungible_tokens_of_account(senderAddress)
    
    print(hex(nfts[-1].nonce))

    NFT_NONCE = int(hex(nfts[-1].nonce), 16)
    NFT_QTY = 0x1
    NFT_RECIEVER = int(Address.from_bech32(reciever.address).to_hex(), 16)

    tx = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=senderAddress,
        function="ESDTNFTTransfer",
        gas_limit=55000000,
        arguments=[NFT_IDENTIFIER, NFT_NONCE, NFT_QTY, NFT_RECIEVER]
    )

    sender_on_network = provider.get_account(senderAddress)
    tx.nonce = sender_on_network.nonce

    transaction_computer = TransactionComputer()
    tx.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx))

    provider.send_transaction(tx)
    return nfts[-1].nonce
