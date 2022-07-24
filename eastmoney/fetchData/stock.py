# 东方财富获取股票数据
from typing import Iterable
import pandas as pd
import numpy as np
from pandas import *
import requests
import re
import json

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from  eastmoney.kline import kline_test
# import eastmoney


class eastStock():

    @classmethod
    def request_shangzheng_shenzheng(self, code: str, ctype=1,klt="101",fqt="0",lmt="1000000",end="20500101"):
        """
        请求A股的股票数据,默认请求所有的历史日K数据，
        param:code:股票代码
        ctype:股票类型，1表示上证，0表示深证
        klt:是k线类型，默认是日K，101是周K,
        fqt:0不复权，1前复权，2后复权
        lmt:获取的数量
        end:截止日期
        """
        url = "http://22.push2his.eastmoney.com/api/qt/stock/kline/get"
        cb = ""
        params = {
            "cb": cb,
            "secid":'{type}.{code}'.format(type=ctype,code=code),
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": klt,
            "fqt": fqt,
            "end": end,
            "lmt": lmt,
            "_": "1646568864248"
        }
        head = {
            "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62"
        }
        response = requests.get(url=url, params=params, headers=head).json()
        print('{type}.{code}'.format(type=ctype,code=code))
        print("responseTYpe=", type(response))
        name = response["data"]["name"]
        klines = response["data"]["klines"]
        fields = ['date','open', 'close', 'high', 'low', 'volume', 'money', '最大振幅', '涨跌幅度', '涨跌价', '换手率']
        result =  list(map(lambda kline: kline.split(','), klines))
        print(result[0])
        df = DataFrame(result,columns=fields)
        df = df.apply(lambda col: pd.to_numeric(col,errors='ignore'))
        return name, df
        #     "klines": [
        #   "2010-03-19,0.97,0.92,0.99,0.92,197373,1182393994.00,11.86,55.93,0.33,70.49",
        #   "2010-03-22,0.97,1.03,1.03,0.96,110104,693595698.00,7.61,11.96,0.11,39.32",]

    @classmethod
    def request_day_trends(self, code: str, ctype=1, day=1):
        """
        获取分时行情数据
        """
        url = "http://push2.eastmoney.com/api/qt/stock/trends2/get"
        params = {
            "secid": '{type}.{code}'.format(type=ctype, code=code),
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55",
            "iscr": 0,  # 是否获取集合竞价0是否
            "cb": ""
        }
        head = {
            "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62"
        }
        response = requests.get(url=url, params=params, headers=head).json()
        print('{type}.{code}'.format(type=ctype, code=code))
        print("responseTYpe=", type(response))
        name = response["data"]["name"]
        klines = response["data"]["trends"]
        fields = ['date', 'open', 'close', 'high', 'low']
        result = list(map(lambda kline: kline.split(','), klines))
        print(result[0])
        df = DataFrame(result, columns=fields)
        df = df.apply(lambda col: pd.to_numeric(col, errors='ignore'))
        # 昨收价
        prePrice = response["data"]["prePrice"]
        print(df)
        return name, df, prePrice

    @classmethod
    def request_ulist_stocks(self, secids: Iterable[str]):
        """
        获取多个股票的收盘价
        secids: 股票代码, ctye.code例如([0.002466])

        """
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"

        params = {
            "secids": ",".join(secids),
            "fields": "f3,f12,f14,f1,f2,f4",
            "fltt": 2,
            "invt": 2,
            "_": "1657945282430"
        }
        response = requests.get(url,  params=params).json()
        return [obj["f2"] for obj in response["data"]["diff"]]

    @classmethod
    def get_stock_info(self, input: str):
        """
        根据关键字获取股票信息

        """
        url = "https://searchapi.eastmoney.com/api/suggest/get"
        params = {
            "input": input,
            "type": 14,
            "count": 1,
            "token": "D43BF722C8E33BDC906FB84D85E326E8",
        }
        response = requests.get(url,  params=params).json()
        return response


    @classmethod
    def test_save_local(self):
        code = "510300"
        # code = "300015"
        name, df = eastStock.request_shangzheng_shenzheng(code, ctype=1, klt="101", fqt="2")

        # name,_, klines = eastStock.get_shenzheng(code)
        # eastStock.save_data(name=code + "_" + name + "后复权日K" + ".csv",klines=klines)
        file_name = code + "_" + name + "后复权日K" + ".csv"
        df.to_csv(file_name)
        # name, klines = eastStock.request_shenzheng(code=code)
        print(name)
        print(df[-1:])
        # python3 eastmoney/fetchData/stock.py 

# abc = eastStock.get_stock_info("东方财富")
# print(abc)
# print(abc["QuotationCodeTable"])