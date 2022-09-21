from flask import Flask, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from modules.ptt.pttMainCrawler import ptt_blueprints
from modules.Stock.stockMainCrawler import stock_blueprints
import os
import certifi
app = Flask(__name__)

# connect Db
user_name = os.environ['MONGO_USER']
user_pwd = os.environ['MONGO_PWD']
cluster = "mongodb+srv://{user_name}:{user_pwd}@cluster0.67gy5wa.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())

app.register_blueprint(ptt_blueprints, url_prefix='/ptt')
app.register_blueprint(stock_blueprints, url_prefix='/stock')


@app.route('/')
def helloA():
    return jsonify({"msg": "hello"})


@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
