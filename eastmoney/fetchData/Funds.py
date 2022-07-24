# 基金相关
from typing import List
from wsgiref import headers
import requests
import re
import json
from lxml import etree
from bs4 import BeautifulSoup
from pandas import *
import pandas as pd
import numpy as np
# import jqdatasdk as jq
from datetime import date
import matplotlib.pyplot as plt
import math

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from eastmoney.fetchData.stock import eastStock
# from plot_test.jukuang_test import auth_jukuang


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
        return myDF

    @classmethod
    def read_funds_from(self, file: str) -> DataFrame:
        '''
        从本地文件读取基金持仓数据，
        return:以时间为索引，例：2013-12-01
        '''
        df = pd.read_csv(file, dtype={'股票代码': str})
        df.占净值比例 = df.apply(lambda x: float(x.占净值比例[0:-1]) / 100.0, axis=1)
        df.set_index(['date'], inplace=True)  # 设置时间为索引
        return df

    @classmethod
    def calculate_fund_earnings_rate(self, fileName: str):
        """
        计算拟合收益率,
        return:每个季度的持仓收益率
        """
        #先从文件中读取对应的基金持仓数据
        df = self.read_funds_from(fileName)
        end_date = df.index.tolist()
        # 获取时间序列
        end_date = list(set(end_date))  # 不能保证原有的顺序
        end_date.sort()
        print("end_date=",end_date)

        # test 获取股票代码
        first_end_date = end_date[0]
        first_quarterly = df.loc[first_end_date]
        print(first_quarterly)
        codes = first_quarterly.loc[:, '股票代码'].tolist()

        date_len = len(end_date)
        result_rate = []
        for index, obj in enumerate(end_date):
            print("index=", index)
            print("obj=", obj)

            quarterly = df.loc[obj]
            codes = quarterly.loc[:, '股票代码'].tolist()
            rates = quarterly['占净值比例'].values.round(4).tolist()
            
            if index + 1 < date_len:
                result = self.calculate_one_season_rate(codes=codes,rates=rates,start_date=obj,end_date=end_date[index + 1])
                result_rate.append(result)
            else:
                current_date = date.today().strftime('%Y-%m-%d')
                result = self.calculate_one_season_rate(codes=codes,rates=rates,start_date=obj,end_date=current_date)
                result_rate.append(result)
        print(result_rate)
        return result_rate

    
    @classmethod
    def calculate_one_season_rate(self, codes, rates, start_date, end_date):
        """
        计算时间段内的收益率
        codes:股票的代码列表
        rates:持仓占比
        start_date:开始的日期
        end_date:结束的日期
        """
        # test 只取前五个
        # codes = codes[:5]
        # rates = rates[:5]
        
        nm_codes, start_stock = self.load_data_from_jukuang_service(codes=codes, end_date=start_date)
        start_closes_price = list(map(lambda x: start_stock.loc[x,'close'], nm_codes))

        _, end_stock = self.load_data_from_jukuang_service(codes=codes, end_date=end_date)
        # 根据股票代码获取对应的收盘数据
        end_closes_price = list(map(lambda x: end_stock.loc[x,'close'], nm_codes))
        sum_rate = sum(rates)
        print("sum_rate=",sum_rate)
        real_rate = list(map(lambda x:x/sum_rate,rates))
        print("real_rate=",real_rate)
        #  计算涨跌幅并乘上持仓占比，如果为nan直接当做这个股票是不涨不跌，前后为1
        result = list(map(lambda x, y, z: (x/y*z).round(5) if not math.isnan(x/y*z) else z, end_closes_price, start_closes_price, real_rate))
        
        print("myresult===--",result)

        return sum(result)

    @classmethod
    def get_public_dates(self, fund_code: str) -> List[str]:
        """
        获取历史上更新持仓情况的日期列表
        -
        Parameters
        ---
        fund_code : 
            str 6 位基金代码
        ---
        Returns
        ---
        List[str]
            指定基金公开持仓的日期列表
        """

        params = (
            ('FCODE', fund_code),
            # ('OSVersion', '14.3'),
            # ('appVersion', '6.3.8'),
            ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
            ('plat', 'Iphone'),
            # ('plat','Android'),
            ('product', 'EFund'),
            # ('serverVersion', '6.3.6'),
            ('version', '6.3.8'),
        )
        url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNIVInfoMultiple'
        headers = {
            'User-Agent': 'EMProjJijin/6.2.8 (iPhone; iOS 13.6; Scale/2.00)',
            # 'GTOKEN': '98B423068C1F4DEF9842F82ADF08C5db',
            # 'clientInfo': 'ttjj-iPhone10,1-iOS-iOS13.6',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'fundmobapi.eastmoney.com',
            # 'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/FundHistoryNetWorth',
        }
        # headers = {}
        json_response = requests.get(
            url,
            headers=headers,
            params=params).json()
        if json_response['Datas'] is None:
            return []
        return json_response['Datas']

    @classmethod
    def get_inverst_postion(self, code: str, date=None) -> pd.DataFrame:
        '''
        根据基金代码跟日期获取基金持仓信息
        ---
        参数
        ---
            code 基金代码 \n
            date 公布日期 形如 '2020-09-31' 默认为 None，得到最新公布的数据
        返回
        ---
            持仓信息表格
        '''
        EastmoneyFundHeaders = {
            'User-Agent': 'EMProjJijin/6.2.8 (iPhone; iOS 13.6; Scale/2.00)',
            # 'GTOKEN': '98B423068C1F4DEF9842F82ADF08C5db',
            # 'clientInfo': 'ttjj-iPhone10,1-iOS-iOS13.6',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'fundmobapi.eastmoney.com',
            # 'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/FundHistoryNetWorth',
        }
        params = [
            ('FCODE', code),
            ('MobileKey', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
            ('OSVersion', '14.3'),
            ('appType', 'ttjj'),
            ('appVersion', '6.2.8'),
            ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
            ('plat', 'Iphone'),
            ('product', 'EFund'),
            ('serverVersion', '6.2.8'),
            ('version', '6.2.8'),
        ]
        if date is not None:
            params.append(('DATE', date))
        params = tuple(params)

        response = requests.get('https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition',
                                headers=EastmoneyFundHeaders, params=params)
        rows = []
        stocks = response.json()['Datas']['fundStocks']

        columns = {
            'GPDM': '股票代码',
            'GPJC': '股票简称',
            'JZBL': '持仓占比(%)',
            'PCTNVCHG': '较上期变化(%)',
        }
        if stocks is None:
            return pd.DataFrame(rows, columns=columns.values())

        df = pd.DataFrame(stocks)
        print(df)
        df = df[list(columns.keys())].rename(columns=columns)
        return df


code = '161725'
date  = '2022-03-31'
df = EastFunds.get_inverst_postion(code, date=date)
print(df)
# public_dates = EastFunds.get_public_dates(code)
# print(public_dates)
# 通过读取csv文件获取持仓数据并
# 通过聚宽平台获取每个股票的收盘价
# auth_jukuang()
# result = EastFunds.calculate_fund_earnings_rate("512660_基金历史十大持仓.csv")

# abc = [1.0286699999999998, 1.0474124038713053, 0.8196399999999999, 1.05106, 0.93913, 0.9871900000000001, 0.80694, 1.07463, 0.8642500000000001, 1.2940500000000001, 0.91686, 1.02565, 0.98722, 0.9142600000000001, 1.0839299999999998, 1.2366000000000001, 1.2593999999999999, 0.78491, 1.1071000000000002, 1.02057, 1.15743, 0.80929]

# sum = 1
# result_arr = [1]
# for obj in abc:
#     sum *= obj
#     # print(sum)
#     result_arr.append(sum)
# # print(sum)
# print(result_arr)
# x = ['2016-09-30', '2016-12-31', '2017-03-31', '2017-06-30', '2017-09-30', '2017-12-31', '2018-03-31', '2018-06-30', '2018-09-30', '2018-12-31', '2019-03-31', '2019-06-30', '2019-09-30', '2019-12-31', '2020-03-31', '2020-06-30', '2020-09-30', '2020-12-31', '2021-03-31', '2021-06-30', '2021-09-30', '2021-12-31', '2022-03-26']
# plt.plot(x,result_arr)
# plt.show()

# 通过东财的网站抓取数据并存入到csv文件中
# EastFunds.request_fund_all_data("510300")
