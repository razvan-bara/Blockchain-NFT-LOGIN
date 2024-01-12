from __main__ import app
from flask import render_template, request, redirect, url_for
from models.user import User
from models.db import db

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.password == data.get('password'):
        return redirect(url_for('info'))
    else:
        return render_template('login.html', message="Invalid email or password. Please try again.")
    
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')