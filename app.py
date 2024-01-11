from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect

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

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['POST'])
def register():
    new_user = User()
    new_user.name = request.form.get('name')
    new_user.email = request.form.get('email')
    new_user.password = request.form.get('password')  # In a real-world application, you should hash the password before storing it
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('register_form'))

@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.password == data.get('password'):
        return {"message": "Login successful."}, 200
    else:
        return {"message": "Invalid email or password."}, 401

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)