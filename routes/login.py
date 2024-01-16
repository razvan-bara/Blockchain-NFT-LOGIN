from __main__ import app
from flask import render_template, request, redirect, url_for
from models.user import User
from models.db import db
from blockchain.nft import check_nft_ownership
from routes.authStorage import auth_storage
import json 

@app.route('/login', methods=['POST'])
def login():
    
    data = request.files['nft']
    nft_json = json.loads(data.stream.read())
    owner_of_nft = nft_json['ownership']
    
    user = User.query.filter_by(address=owner_of_nft).first()
    if not user:
        return render_template('login.html', message="User not registered on the platform")
    
    if check_nft_ownership(user):
        auth_storage.set_auth_user(user)
        return redirect(url_for('info'))
    else:
        return render_template('login.html', message="Invalid NFT ownership")
    
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')