from models.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    secret_key = db.Column(db.Text, nullable=False)
    nft_nonce = db.Column(db.SmallInteger, nullable=True)