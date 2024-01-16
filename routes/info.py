from __main__ import app
from flask import render_template
from models.user import User
from routes.authStorage import auth_storage

@app.route('/info', methods=['GET'])
def info():
    user = auth_storage.auth_user
    users = User.query.all()
    return render_template('info.html', users=users, auth_user=user)