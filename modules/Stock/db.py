# 寫入db
from pymongo import MongoClient
import certifi
from bson import json_util
import json

# connect Db
cluster = "mongodb+srv://mongostock:lltWZuKKO7RTTf7Q@cluster0.67gy5wa.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())

# 寫入db for stock -> collection = 買賣超系列

def postInvestorsDB(buyAndSellList, collectionType):
    db = client['stock']
    db[collectionType].delete_many({})
    sellList = json.loads(json_util.dumps(buyAndSellList['sellList']))
    buyList = json.loads(json_util.dumps(buyAndSellList['buyList']))
    db[collectionType].insert_many(sellList)
    db[collectionType].insert_many(buyList)