# 爬取三大法人買賣超資料
import json
from public.fakeUserAgentGenerate import userAgentRoute
from .db import postInvestorsDB, getStockInvestorCollection
from lxml import html, etree
import requests

urlList = {
    "listed_foreign": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_D.djhtm",
    "listed_local": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_DD.djhtm",
    "listed_employed": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_DB.djhtm",
    "otc_foreign": "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=D&B=1&C=1",
    "otc_local": [
        "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DD&B=1&C=1",
        "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DD&B=1&C=5",
        "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DD&B=1&C=10",
        "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DD&B=1&C=30"
    ],
    "otc_employed": ["https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DB&B=1&C=1"],
}


# 爬蟲：三大法人買賣超資料，爬完的純資料
def getInvestorsRawData(type):
    detailUrlList = typeSelect(type)
    accu = 0
    buyList = []
    sellList = []
    for index, url in enumerate(detailUrlList):
        if index == 0:
            accu = '1'
        elif index == 1:
            accu = '5'
        elif index == 2:
            accu = '10'
        elif index == 3:
            accu = '30'
        response = requests.get(url, headers={
                                'User-Agent': userAgentRoute()})
        htmlTree = etree.HTML(response.text)

        date = htmlTree.xpath('//div[@class="t11"]/text()')
        # 買超股票名稱
        buyRawCodeNameList = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[2]/a/text()')
        # 買超股票代號
        buyRawCodeList = [a.attrib['href']
                          for a in htmlTree.xpath('//table[@class="t01"]/tr/td[2]/a')]
        # 買超張數
        buyPiece = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[3]/text()')
        # 收盤價錢
        buyClosePrice = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[4]/text()')
        # 賣超股票名稱
        sellRawCodeNameList = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[7]/a/text()')
        # 賣超股票代號
        sellRawCodeList = [a.attrib['href']
                           for a in htmlTree.xpath('//table[@class="t01"]/tr/td[7]/a')]
        # 賣超張數
        sellPiece = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[8]/text()')
        # 收盤價錢
        sellClosePrice = htmlTree.xpath(
            '//table[@class="t01"]/tr/td[9]/text()')

        buyList = buyList + \
            dealRawCrawData(buyRawCodeNameList, buyRawCodeList,
                            buyPiece, buyClosePrice,   'buy', date, accu)
        sellList = sellList + dealRawCrawData(
            sellRawCodeNameList, sellRawCodeList, sellPiece, sellClosePrice,  'sell', date, accu)
    return {"buyList": buyList, "sellList": sellList}

# 處理法人買賣超的資料，將其變為json格式（包含買/賣資料）


def dealRawCrawData(codeName, codeHref, piece, closePrice, type, date, accu):
    list = []
    print(piece)
    print(closePrice)
    for index, href in enumerate(codeHref):
        pureCode = href[href.find("'")+1: href.rfind("'")]
        pureName = codeName[index].replace(pureCode, "")
        list.append({
            "no": index+1,
            "code": pureCode,
            "name": pureName,
            "type": type,
            "date": date[0],
            "accumulation": accu,
            "piece": piece[index+1],
            "close": closePrice[index+1]
        })
    return list

# 決定這次要爬什麼資料回來


def typeSelect(type):
    return urlList[type]

# post更新stock-DB資料（一次更新全部）


def postDataToInvestorsDB(type):
    postInvestorsDB(getInvestorsRawData(type), type)
    return 'OK'

# 得到法人買賣超資料


def getInvestorsData(type):
    resultList = []
    apiResult = getStockInvestorCollection(type)
    for doc in apiResult:
        resultList.append({
            'no': doc['no'],
            'code': doc['code'],
            'name': doc['name'],
            'type': doc['type'],
            'date': doc['date'],
        })
    return resultList
