from multiversx_sdk_wallet import UserPEM, UserSigner
from multiversx_sdk_core import Address, TransactionComputer, TokenComputer, AccountNonceHolder, Transaction
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

def  generateAndTransferNFT(nft_name : str, reciever : User) -> int:

    signer = UserSigner.from_pem_file(NFT_CREATOR_USER_WALLET)
    sender = UserPEM.from_file(NFT_CREATOR_USER_WALLET)
    senderAddress = sender.public_key.to_address("erd")

    NFT_QUANTITY = 0x1
    NFT_NAME = int(nft_name.encode().hex(), 16)
    NFT_ROYALTIES = 0x1000
    NFT_HASH = 0x0
    NFT_ATTRIBUTES = 0x6d657461646174613a697066734349442f6e66745f61747472732e6a736f6e3b746167733a6465736372697074696f6e2c61747472696275746573
    NFT_URI = 0x2e2f6e6674696d672e6a7067
    
    tx_gen_nft = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=senderAddress,
        function="ESDTNFTCreate",
        gas_limit=55000000,
        arguments=[NFT_IDENTIFIER, NFT_QUANTITY, NFT_NAME, NFT_ROYALTIES, NFT_HASH, NFT_ATTRIBUTES, NFT_URI]
    )

    nfts = provider.get_nonfungible_tokens_of_account(senderAddress)
    NFT_NONCE = int(hex(nfts[-1].nonce), 16)
    NFT_QTY = 0x1
    NFT_RECIEVER = int(Address.from_bech32(reciever.address).to_hex(), 16)

    
    tx_transfer_nft = sc_factory.create_transaction_for_execute(
        sender=senderAddress,
        contract=senderAddress,
        function="ESDTNFTTransfer",
        gas_limit=55000000,
        arguments=[NFT_IDENTIFIER, NFT_NONCE, NFT_QTY, NFT_RECIEVER]
    )

    sender_on_network = provider.get_account(senderAddress)
    nonce_holder = AccountNonceHolder(sender_on_network.nonce)
    
    tx_gen_nft.nonce = nonce_holder.get_nonce_then_increment()
    tx_transfer_nft.nonce = nonce_holder.get_nonce_then_increment()

    transaction_computer = TransactionComputer()
    tx_gen_nft.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx_gen_nft))
    tx_transfer_nft.signature = signer.sign(transaction_computer.compute_bytes_for_signing(tx_transfer_nft))

    provider.send_transactions([tx_gen_nft, tx_transfer_nft])
    return nfts[-1].nonce

def check_nft_ownership(user : User) -> bool:
    nfts = provider.get_nonfungible_tokens_of_account(Address.from_bech32(user.address))
    if len(nfts) == 0:
        return False
    
    return user.nft_nonce == nfts[0].nonce