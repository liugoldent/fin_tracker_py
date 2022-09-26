import json
from public.fakeUserAgentGenerate import userAgentRoute
from lxml import html, etree
import requests

# 證交所上市櫃股票列表
stocksUrlList = {
    'listed': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
    'otc': 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
}

# 爬取上市櫃股票列表資料
def getListRawData(type):
    response = requests.get(stocksUrlList['listed'], headers={
                            'User-Agent': userAgentRoute()})
    htmlTree = etree.HTML(response.text)
    stockName = htmlTree.xpath('/html/body/table[2]/tr[3]/td[1]')
    