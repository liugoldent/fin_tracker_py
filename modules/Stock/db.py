# 寫入db
from pymongo import MongoClient
import certifi
from bson import json_util
import json
import os

# connect Db
user_name = os.environ['MONGO_USER']
user_pwd = os.environ['MONGO_PWD']
cluster = f"mongodb+srv://{user_name}:{user_pwd}@cluster0.67gy5wa.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())

# 寫入db stock 各個買賣超 collection資料


def postInvestorsDB(buyAndSellList, collectionType):
    db = client['stock']
    db[collectionType].delete_many({})
    sellList = json.loads(json_util.dumps(buyAndSellList['sellList']))
    buyList = json.loads(json_util.dumps(buyAndSellList['buyList']))
    db[collectionType].insert_many(sellList)
    db[collectionType].insert_many(buyList)

# 從db stock取出各自的買賣超資料


def getStockInvestorCollection(collectionType):
    db = client['stock']
    return db[collectionType].find({})
