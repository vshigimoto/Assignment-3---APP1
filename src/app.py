from flask import Flask, render_template, url_for, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import requests
import email_validator
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
headers = {
    "accept": "application/json",
    "X-API-Key": "F5GCxxgXhLDTENlIDl8RHLBva7jXUC0SQuyrIV8jL1LJ8H9ZznttU81G50Rrhwqq"
}
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=7, max=40)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=7, max=40)])

class Nft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(800), unique=True, nullable=False)
    name = db.Column(db.String(800), unique=True, nullable=False)
    mint = db.Column(db.String(800), unique=True, nullable=False)

    def __init__(self, adress, name, mint):
        self.adress = adress
        self.name = name
        self.mint = mint

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(800),unique=True, nullable=False)
    password = db.Column(db.String(800), nullable=False)
    email = db.Column(db.String(800),unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/nft")
@login_required
def addperson():
    return render_template("index.html")
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Person.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return render_template("index.html")
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_person = Person(username=form.username.data, email= form.email.data, password=hashed_password)
        Person.query.all()
        new_person.add_to_db()
        return render_template("index.html")

    return render_template('signup.html', form=form)

@app.route("/personadd", methods=['POST'])
def personadd():
    address = request.form["url"]
    url = f"https://solana-gateway.moralis.io/nft/mainnet/{address}/metadata"
    nfts = Nft.query.filter_by(mint = address).first()
    if(nfts == None):
        response = requests.get(url, headers=headers)
        payload = response.json()
        name = payload["name"]
        mint = payload["mint"]
        entry = Nft(url, name, mint)
        Nft.query.all()
        entry.add_to_db()
        return render_template("result.html", mint=mint, name=name)
    mint = nfts.mint
    name = nfts.name
    return render_template("db.html", mint=mint, name=name)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
