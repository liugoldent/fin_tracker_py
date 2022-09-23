from flask import Flask, render_template, jsonify
from flask_cors import CORS
from modules.ptt.pttMainCrawler import ptt_blueprints
from modules.Stock.mainRouter import stock_blueprints
app = Flask(__name__)


app.register_blueprint(ptt_blueprints, url_prefix='/ptt')
app.register_blueprint(stock_blueprints, url_prefix='/stock')

@app.route('/')
def helloA():
    return jsonify({"msg": "hello"})


@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
