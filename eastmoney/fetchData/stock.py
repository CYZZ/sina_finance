# 东方财富获取股票数据
import pandas as pd
import numpy as np
from pandas import *


import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from  eastmoney.kline import kline_test
# import eastmoney


class eastStock():

    @classmethod
    def get_shangzheng(self,code:str):
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112405093671278680167_1646568488454&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=0.' + code + '&beg=0&end=20500000&_=1646568488541'
        print('url=',url)
        data = kline_test.request_data(url)
        splits, name, klines = kline_test.convert_data_to_json(data, pre="jQuery112405093671278680167_1646568488454\(")
        print("name====",name)
        return name, splits, klines
        # "2010-03-19,0.97,0.92,0.99,0.92,197373,1182393994.00,11.86,55.93,0.33,70.49"
        # "2022-03-03,27.21,26.74,27.40,26.57,1455123,3914571824.00,3.06,-1.40,-0.38,1.69",
        # "2022-03-04,26.45,26.00,26.86,25.82,1920698,5035058688.00,3.89,-2.77,-0.74,2.24"
    
    @classmethod
    def get_shenzheng(self,code:str):
        url = 'http://22.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404488523211257569_1646568864231&secid=1.' + code + '&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=1000000&_=1646568864248'
        print('url=',url)
        data = kline_test.request_data(url)
        splits, name, klines = kline_test.convert_data_to_json(data, pre="jQuery112404488523211257569_1646568864231\(")
        print("name====",name)
        return name, splits, klines
    
    @classmethod
    def save_data(self,name:str,klines):
        fields = ['date','open', 'close', 'high', 'low', 'volume', 'money', '最大振幅', '涨跌幅度', '涨跌价', '换手率']
        result =  list(map(lambda kline: kline.split(','), klines))
        print(result[0])
        df = DataFrame(result,columns=fields)
        df.to_csv(name)
        # print(df.head())

# code = "300059"

# name,_, klines = eastStock.get_shangzheng(code)
code = "600519"
name,_, klines = eastStock.get_shenzheng(code)
eastStock.save_data(name=code + "_" + name + ".csv",klines=klines)



# 获取上证的股票日K数据， 测试贵州茅台
# http://22.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404488523211257569_1646568864231&secid=1.600519&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&lmt=1000000&_=1646568864248


# 获取深证的股票数据，测试东方财富。
# http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112405093671278680167_1646568488454&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=0.300059&beg=0&end=20500000&_=1646568488541