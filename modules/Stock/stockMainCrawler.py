# 股票系列-主要爬蟲程式
import sys
sys.path.append('/Users/guantingliu/Desktop/BackEnd/fin_tracker_py/modules/Stock')
import twstock
from crypt import methods
from flask import jsonify, Blueprint, request
from flask_cors import CORS
from stockDetail import CodeInfo
from getInvestorsRawData import getInvestorsRawData
from db import postInvestorsDB


# 對blueprint 做CORS處理
stock_blueprints = Blueprint('stockFetch', __name__)
CORS(stock_blueprints, resources={
    r"/.*": {"origins": ["http://localhost:3000"]}})

# api homepage -> 連線連到stock是否ok
@stock_blueprints.route('/', methods=['GET'])
def api():
    return jsonify({"message": "Stock OK"})

# 打twstock API，取得股價資料
@stock_blueprints.route('/eachInfo', methods=['POST'])
def crawInvestor():
    newCodeClass = CodeInfo('2330')
    pastPrice = newCodeClass.baseInfo()
    # tpexValue = twstock.tpex

    # code = request.args.get('code')
    # print(code)
    # value = IndividualStocksInfo(code)
    # stock = twstock.Stock(code)
    # print(value.moviing_average())
    # data = stock.fetch_from(2022, 7)
    # print(stock.ma_bias_ratio(5,10))
    # return in JSON format. (For API)
    return jsonify({"message": pastPrice})

# 爬取法人買賣超資料 & 把他打給資料庫
# type：包含listed_foreign：上市外資買賣超一日。
@stock_blueprints.route('/investors/<type>', methods=['GET'])
def api3(type):
    buySellList = getInvestorsRawData(type)
    postInvestorsDB(buySellList, type)
    return buySellList