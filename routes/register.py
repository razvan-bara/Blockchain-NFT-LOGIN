from __main__ import app
from flask import render_template, request, redirect, url_for
from models.user import User
from models.db import db

@app.route('/register', methods=['POST'])
def register():
    new_user = User()
    new_user.name = request.form.get('name')
    new_user.email = request.form.get('email')
    new_user.password = request.form.get('password')
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('register_form'))

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')