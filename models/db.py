from __main__ import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stefan:1234@localhost:1234/blockchain'
db = SQLAlchemy(app)