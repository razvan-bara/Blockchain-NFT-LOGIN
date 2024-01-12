from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "UP"}, 200

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

import routes.login, routes.register, routes.info
from models.db import db

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)