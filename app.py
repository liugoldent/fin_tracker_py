from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient
from modules.ptt.pttMainCrawler import ptt_blueprints
# from modules.Stock.stockMainCrawler import stock_blueprints
import certifi
app = Flask(__name__)

# connect Db
# cluster = "mongodb+srv://mongostock:lltWZuKKO7RTTf7Q@cluster0.67gy5wa.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(cluster, tlsCAFile=certifi.where())

# app.register_blueprint(ptt_blueprints, url_prefix='/ptt')
# app.register_blueprint(stock_blueprints, url_prefix='/stock')


@app.route('/')
def helloA():
    print('123')
    return 'Hello'


@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
