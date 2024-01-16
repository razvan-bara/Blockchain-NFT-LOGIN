from __main__ import app
from flask import render_template, request, redirect, url_for, send_file, jsonify
from models.user import User
from models.db import db
from blockchain.wallet import generateWallet, saveWallet
from blockchain.nft import generateNFT, transferLatestNFT
from pathlib import Path
from blockchain.provider import provider
import os
import json

@app.route('/register', methods=['POST'])
def register():
    new_user = User()
    new_user.name = request.form.get('name')
    new_user.email = request.form.get('email')
    new_user.password = request.form.get('password')
    
    pemWallet = generateWallet()
    new_user.public_key = pemWallet.public_key.hex()
    new_user.address = pemWallet.public_key.to_address("erd").to_bech32()
    new_user.secret_key = pemWallet.secret_key.hex()

    db.session.add(new_user)
    db.session.commit()

    saveWallet(pemWallet, new_user.id)
    nft_name = "AUTH_NFT_OF_ID_#" + str(new_user.id)
    
    generateNFT(nft_name)
    nft_nonce = transferLatestNFT(new_user)
    
    new_user.nft_nonce = nft_nonce
    db.session.add(new_user)
    db.session.commit()

    if not os.path.exists("output/nfts"):
        os.makedirs("output/nfts")

    nft_json  = {
        'description': 'NFT USED FOR 2023/2024 BLOCKCHAIN PROJECT SPCD-1A',
        'ownership': new_user.address
    }

    nft_file = "output/nfts/" + nft_name + ".json"
    file = open(nft_file, "w")
    file.write(json.dumps(nft_json))
    file.close()
    
    return send_file(nft_file, as_attachment=True)

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')