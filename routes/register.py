from __main__ import app
from flask import render_template, request, redirect, url_for
from models.user import User
from models.db import db
from blockchain.wallet import generateWallet, saveWallet
from pathlib import Path
import os

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

    return redirect(url_for('register'))

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')