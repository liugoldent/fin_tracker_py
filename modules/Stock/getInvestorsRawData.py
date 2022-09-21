# 爬取三大法人買賣超資料
import json
from public.fakeUserAgentGenerate import userAgentRoute
from lxml import html, etree
import requests

# 爬蟲：三大法人買賣超資料，爬完的純資料


def getInvestorsRawData(type):
    response = requests.get(typeSelect(type), headers={
                            'User-Agent': userAgentRoute()})
    htmlTree = etree.HTML(response.text)

    date = htmlTree.xpath('//div[@class="t11"]/text()')
    buyRawCodeNameList = htmlTree.xpath(
        '//table[@class="t01"]/tr/td[2]/a/text()')
    buyRawCodeList = [a.attrib['href']
                      for a in htmlTree.xpath('//table[@class="t01"]/tr/td[2]/a')]
    sellRawCodeNameList = htmlTree.xpath(
        '//table[@class="t01"]/tr/td[7]/a/text()')
    sellRawCodeList = [a.attrib['href']
                       for a in htmlTree.xpath('//table[@class="t01"]/tr/td[7]/a')]

    buyList = dealRawCrawData(buyRawCodeNameList, buyRawCodeList, 'buy', date)
    sellList = dealRawCrawData(
        sellRawCodeNameList, sellRawCodeList, 'sell', date)
    return {"buyList": buyList, "sellList": sellList}

# 處理法人買賣超的資料，將其變為json格式（包含買/賣資料）


def dealRawCrawData(codeName, CodeHref, type, date):
    list = []
    for index, href in enumerate(CodeHref):
        pureCode = href[href.find("'")+1: href.rfind("'")]
        pureName = codeName[index].replace(pureCode, "")
        list.append({
            "no": index+1,
            "code": pureCode,
            "name": pureName,
            "type": type,
            "date": date[0],
        })
    return list

# 決定這次要爬什麼資料回來


def typeSelect(type):
    typeList = {
        "listed_foreign": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_D.djhtm",
        "listed_local": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_DD.djhtm",
        "listed_employed": "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_DB.djhtm",
        "otc_foreign": "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=D&B=1&C=1",
        "otc_local": "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DD&B=1&C=1",
        "otc_employed": "https://fubon-ebrokerdj.fbs.com.tw/z/zg/zgk.djhtm?A=DB&B=1&C=1",
    }
    return typeList[type]
