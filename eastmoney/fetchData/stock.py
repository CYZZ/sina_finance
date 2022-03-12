# 东方财富获取股票数据
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
    def convert_javascript_to_json(self, data: str, pre=""):
        print("start convert data----====")
        regular = r'%s\((.*?)\)' % pre
        # find_json = re.compile(r'jQuery33103422893090882453_1641114428433\((.*?)\)')
        find_json = re.compile(regular)
        all_match = re.findall(find_json, data)
        json_str = all_match[0]
        dic = json.loads(json_str)
        name = dic["data"]["name"]
        klines = dic["data"]["klines"]
        return name, klines
    #     "klines": [
    #   "2010-03-19,0.97,0.92,0.99,0.92,197373,1182393994.00,11.86,55.93,0.33,70.49",
    #   "2010-03-22,0.97,1.03,1.03,0.96,110104,693595698.00,7.61,11.96,0.11,39.32",]

    @classmethod
    def request_shangzheng(self,code: str):
        url = "http://22.push2his.eastmoney.com/api/qt/stock/kline/get"
        cb = "jQuery112404488523211257569_1646568864231"
        params = {
            "cb": cb,
            "secid": "1." + code,
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "0",
            "end": "20500101",
            "lmt": "1000000",
            "_": "1646568864248"
        }
        head = {
            "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62"
        }
        response = requests.get(url=url,params=params,headers=head).text
        return self.convert_javascript_to_json(response,pre=cb)


    
    @classmethod
    def request_shenzheng(self, code: str):
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        cb = "jQuery112405093671278680167_1646568488454"
        params = {
            "cb": cb,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "klt": "101",
            "fqt": "1",
            "secid": "0." + code,
            "beg": "0",
            "end": "20500000",
            "_": "1646568488541"
        }
        head = {
            "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62"
        }
        response = requests.get(url=url,params=params,headers=head).text
        return self.convert_javascript_to_json(response,pre=cb)
    
    @classmethod
    def save_data(self,name:str,klines):
        fields = ['date','open', 'close', 'high', 'low', 'volume', 'money', '最大振幅', '涨跌幅度', '涨跌价', '换手率']
        result =  list(map(lambda kline: kline.split(','), klines))
        print(result[0])
        df = DataFrame(result,columns=fields)
        df.to_csv(name)
        # print(df.head())

code = "300059"

# name,_, klines = eastStock.get_shangzheng(code)
# code = "600519"
# name,_, klines = eastStock.get_shenzheng(code)
# eastStock.save_data(name=code + "_" + name + ".csv",klines=klines)
name, klines = eastStock.request_shenzheng(code=code)
print(name)
print(klines[-1])



# 获取上证的股票日K数据， 测试贵州茅台
# http://22.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404488523211257569_1646568864231&secid=1.600519&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=1000000&_=1646568864248


# 获取深证的股票数据，测试东方财富。
# http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112405093671278680167_1646568488454&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=0.300059&beg=0&end=20500000&_=1646568488541