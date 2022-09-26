# 寫入db
from pymongo import MongoClient
import certifi
from bson import json_util
import json
import os

# connect Db
user_name = os.environ['MONGO_USER']
user_pwd = os.environ['MONGO_PWD']
print(user_name)
print(user_pwd)
cluster = f"mongodb+srv://{user_name}:{user_pwd}@cluster0.lzg4zlq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())

# 寫入db stock 各個買賣超 collection資料


def postInvestorsDB(buyAndSellList, collectionType):
    db = client['investor']
    db[collectionType].delete_many({})
    sellList = json.loads(json_util.dumps(buyAndSellList['sellList']))
    buyList = json.loads(json_util.dumps(buyAndSellList['buyList']))
    db[collectionType].insert_many(sellList)
    db[collectionType].insert_many(buyList)

# 從db stock取出各自的買賣超資料


def getStockInvestorCollection(collectionType):
    db = client['investor']
    return db[collectionType].find({})


# 要修改DB記得先輸入此資訊
# del os.environ['MONGO_USER']
# del os.environ['MONGO_PWD']
# os.environ['MONGO_USER'] = 'fintrackerowner' 
# os.environ['MONGO_PWD'] = 'MEyAVn830L7GuiMo'