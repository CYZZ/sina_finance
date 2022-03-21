# 基金相关
from typing import List
import requests
import re
import json
from lxml import etree
from bs4 import BeautifulSoup
from pandas import *
import pandas as pd
import numpy as np
import jqdatasdk as jq

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
from plot_test.jukuang_test import auth_jukuang


class EastFunds():
    @classmethod
    def request_funds(self, code, year=2001, topline=10):
        '''
        获取基金的历史持仓
        year: 当前年份
        topline: 前十大持仓
        '''
        url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx"
        params = {
            "type": "jjcc",
            "code": code,
            "topline": topline,
            "year": year
        }
        response = requests.get(url=url, params=params)
        regular = r'(\{.*?\})'
        find_json = re.compile(regular)
        all_match = re.findall(find_json, response.text)
        json_str: str = all_match[0]
        json_str = json_str.replace('content:', '"content":')
        json_str = json_str.replace('arryear:', '"arryear":')
        json_str = json_str.replace('curyear:', '"curyear":')
        dic = json.loads(json_str)

        arryear: List[int] = dic["arryear"]
        curyear = dic["curyear"]
        content = dic["content"]
        return content, arryear, curyear

    @classmethod
    def request_fund_all_data(self, code):
        # 先获取年份数组
        _, arryear, _ = self.request_funds(code=code)
        arryear.reverse()  # 取反，将时间按照从早到晚的顺序排序
        print(arryear)
        myDF = DataFrame()
        for year in arryear:
            # 遍历数组，请求所有的历史数据
            content, _, _ = EastFunds.request_funds(code=code, year=year)
            content = content.replace('&nbsp;', ' ')
            tree = etree.HTML(content)
            div_list = tree.xpath('//div[@class="box"]')
            div_list.reverse()  # reverse将数组取反，时间按照一季度到四季度的排序
            for div in div_list:
                # 获取持仓截止日期，
                deadline = div.xpath(
                    'div[@class="boxitem w790"]/h4/label[2]/font/text()')[0]
                print(deadline)

                column = div.xpath(
                    'div[@class="boxitem w790"]/table/thead/tr/th')
                column = list(map(lambda th: etree.tostring(
                    th, encoding='utf-8', method='text').decode(), column))
                print(column)

                tbody_tr = div.xpath('div[@class="boxitem w790"]/table/tbody/tr')
                tbody_tr_tds = list(map(lambda td: list(map(lambda obj: etree.tostring(obj, encoding='utf-8', method='text').decode(), td)), tbody_tr))
                df = DataFrame(tbody_tr_tds, columns=column)
                df = df.loc[:, ['序号', '股票代码', '股票名称', '占净值比例', '持股数（万股）', '持仓市值（万元）']]
                df.insert(0, 'date', deadline)
                df.set_index(['序号'], inplace=True)
                # print(df)
                myDF = myDF.append(df)
                # break
                # for tr in tbody_tr:
                #     td = tr.xpath('td')
                #     tbody_td = list(map(lambda obj: etree.tostring(obj, encoding='utf-8', method='text').decode(), td))
                #     print(tbody_td)

        print(myDF)
        # print(myDF.info)
        myDF.to_csv(str(code) + '_基金历史十大持仓.csv')

    @classmethod
    def read_funds_from(self, file: str) -> DataFrame:
        df = pd.read_csv(file, dtype={'股票代码': str})
        df.占净值比例 = df.apply(lambda x: float(x.占净值比例[0:-1]) / 100.0, axis=1)
        df.set_index(['date'], inplace=True)
        return df

    @classmethod
    def load_data_from_jukuang_service(self, codes, end_date: str, count=1):
        """
        从聚宽平台获取数据
        :return:
        """
        auth_jukuang()
        print("codes=",codes)
        # 转换代码格式
        nm_code = jq.normalize_code(codes)
        print("获取格式代码=",nm_code)

        # 输入
        # jq.normalize_code(['000001', 'SZ000001', '000001SZ', '000001.sz', '000001.XSHE'])
        # ['000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE']
        # 获取股票的数据
        # fields = ['open', 'close', 'low', 'high', 'volume', 'money',
        #           'factor', 'high_limit', 'low_limit', 'avg', 'pre_close', 'paused']
        fields = None
        # 获取当前的行情数据
        df_stock: DataFrame = jq.get_price(nm_code, count=count, end_date=end_date, fields=fields, panel=False)
        print("----开始查看持仓股票的信息----")
        print(df_stock)

# content, arryear, curyear = eastFunds.request_funds(code="512880")
# print(content)
# print(arryear)


# df = pd.read_csv("159928_基金历史十大持仓.csv", dtype={'股票代码':str})
# df.占净值比例 = df.apply(lambda x: float(x.占净值比例[0:-1])/100.0, axis=1)
# df.set_index(['date', '序号'],inplace=True)
df = EastFunds.read_funds_from('159928_基金历史十大持仓.csv')
print(df.head())
# end_date = '2013-12-31'
# end_date = df.loc[:,'date']
end_date = df.index.tolist()
end_date = list(set(end_date)) # 不能保证原有的顺序
end_date.sort()
# new_numbers = []
# for x in end_date:
#     if x not in new_numbers:
#        new_numbers.append(x)
# new_numbers = end_date.map(lambda x: x)


first_quarterly = df.loc[end_date[0]]
print(first_quarterly)
codes = first_quarterly.loc[:, '股票代码'].tolist()



df_stock = EastFunds.load_data_from_jukuang_service(codes=codes, end_date=end_date)
print(df_stock)

