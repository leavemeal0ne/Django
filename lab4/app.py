from flask import Flask
from flask import render_template
from static.img.sources import data
app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/apartments')
def home():
    return render_template('goods.html',data=data)

@app.get('/contacts')
def contacts():
    return render_template('contacts.html')

@app.get('/additions')
def additions():
    return render_template('additions.html')