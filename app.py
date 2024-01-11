from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stefan:1234@localhost/blockchain'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "UP"}, 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User()
    new_user.name = data.get('name')
    new_user.email = data.get('email')
    new_user.password = data.get('password')
    db.session.add(new_user)
    db.session.commit()
    return {"message": "New user registered."}, 201

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)