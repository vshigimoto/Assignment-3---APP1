from flask import Flask, render_template, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

headers = {
    "accept": "application/json",
    "X-API-Key": "F5GCxxgXhLDTENlIDl8RHLBva7jXUC0SQuyrIV8jL1LJ8H9ZznttU81G50Rrhwqq"
}
db = SQLAlchemy(app)

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

@app.route("/")
def addperson():
    return render_template("index.html")

@app.route("/personadd", methods=['POST'])
def personadd():
    address = request.form["url"]
    url = f"https://solana-gateway.moralis.io/nft/mainnet/{address}/metadata"
    response = requests.get(url, headers=headers)
    payload = response.json()
    name = payload["name"]
    mint = payload["mint"]
    entry = Nft(url, name, mint)
    entry.add_to_db()
    return render_template("index.html")


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)