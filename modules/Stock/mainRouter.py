# 股票系列-主要爬蟲程式
from .investorsData import postDataToInvestorsDB, getInvestorsData
from .stockDetail import CodeInfo
from .stocksList import getListRawData
from flask_cors import CORS
from flask import jsonify, Blueprint, request
from crypt import methods
import twstock

# 對blueprint 做CORS處理
stock_blueprints = Blueprint('stockFetch', __name__)
CORS(stock_blueprints, resources={
    r"/.*": {"origins": ["http://localhost:3000"]}})


# api homepage -> 連線連到stock是否ok
@stock_blueprints.route('/', methods=['GET'])
def api1():
    try:
        return jsonify({"message": "Stock OK"})
    except:
        return jsonify({"message": "Stock Home Error"})

# 打twstock API，取得股價資料


@stock_blueprints.route('/eachInfo', methods=['POST'])
def api2():
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
@stock_blueprints.route('/investor/<type>', methods=['POST'])
def api3(type):
    try:
        postDataToInvestorsDB(type)
        return 'OK'
    except:
        return jsonify({"msg": "[post]/investor/all Error"})

# 獲得各別買賣超資料


@stock_blueprints.route('/investor/<type>', methods=['GET'])
def api4(type):
    try:
        return getInvestorsData(type)
    except:
        print(f'[post]/investor/{type} Error')

# 獲得台股個股列表


@stock_blueprints.route('/twStockList', methods=['POST'])
def api5():
    try:
        return getListRawData()
    except:
        print('[POST]/twStockList')
