from __main__ import app
from flask import render_template
from models.user import User

@app.route('/info', methods=['GET'])
def info():
    users = User.query.all()
    return render_template('info.html', users=users)