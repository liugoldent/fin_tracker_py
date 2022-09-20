import twstock


class CodeInfo:
   # 初始化
   # singleStock：這個物件的股票代號
   def __init__(self, val):
      print(val)
      self.singleStock = twstock.Stock(val)
   # 個股基本資料
   def baseInfo(self):
      code = self.singleStock.sid
      return twstock.codes[code]
   # 過去的交易資料
   def pastPrice(self):
      return self.singleStock.fetch_from(2022, 6)
   # 六十均價
   def movingAverage60(self, arg1):
      return self.singleStock.moving_average(self.singleStock.price, 5)