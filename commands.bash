#!/bin/bash

wallet="./output/pyWallet.pem"

function createWallet(){
    echo "Creating multivesex wallet"
    mxpy wallet new --format pem --outfile wallet.pem
}

function createNFTRole(){

    mxpy contract call erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u \
    --pem $wallet \
    --proxy https://testnet-api.multiversx.com \
    --chain T \
    --recall-nonce \
    --gas-limit 60000000 \
    --function setSpecialRole \
    --arguments 0x425044412d613666393637 0x3b468aa3037dbbe2b1eed4dbbf8c0480fe296bad371c41e542918a900ebae150 0x45534454526f6c654e4654437265617465 \
    --send || return
}



function createNFT(){

    # tokenIdentifier = "BPDA-a6f967"
    # quanity = 1
    # NFTName = "RazvanNFT"
    # royalties = 100
    # hash = ""
    # URI = ""

    mxpy contract call erd18drg4gcr0ka79v0w6ndmlrqysrlzj6adxuwyre2zjx9fqr46u9gq7vswyz \
    --pem $wallet \
    --proxy https://testnet-api.multiversx.com \
    --chain T \
    --recall-nonce \
    --gas-limit 40000000 \
    --function ESDTNFTCreate \
    --arguments 0x425044412d613666393637 0x03 0x52617a76616e4e4654 0x64 0x0 0x0 0x0 0x68747470733a2f2f7777772e676f6f676c652e636f6d2f75726c3f73613d692675726c3d68747470732533412532462532467777772e61736b61757469736d2e6f7267253246626c6f6725324677686174697361736426707369673d414f7656617732747069493144485a39376d5f7a4475464a2d35704a267573743d3137303439393434323230333230303026736f757263653d696d616765732663643d766665266f70693d3839393738343439267665643d3043424d516a52787146776f54434b6a6471366d7430344d4446514141414141644141414141424144 --send 

}

