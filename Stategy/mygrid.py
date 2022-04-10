# 我的策略，该模块用于测试每个策略的收益率
from typing import List
import matplotlib.pyplot as plt

import sys
from pathlib import Path

from sqlalchemy import false, true

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import Line
import pyecharts.options as opts
from pandas import DataFrame, Series, DatetimeIndex
from plot_test import jukuang_test
from eastmoney.fetchData.stock import eastStock

class MyChart(QWidget):
    def __init__(self):
        super(MyChart,self).__init__()
        self.initUI()
        self.mainLayout()

    def initUI(self):
        self.setGeometry(400, 400, 800, 600)
        self.setWindowTitle("demo1")

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        url = "https://www.baidu.com"
        # 要使用绝对地址访问文件
        self.myHtml.load(QUrl("file:///Users/yuze.chi/Downloads/bar-gradient.html"))
        # 选择使用url打开网页
        # self.myHtml.load(QUrl(url))

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)
    
    @classmethod
    def line_base(self,x: List, **y) -> Line:
        '''
        绘制折线图
        '''
        c = (
            Line()
            .add_xaxis(x)
            .set_global_opts(title_opts=opts.TitleOpts(title="收益曲线"),
                             tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
                             yaxis_opts=opts.AxisOpts(name="收益率"),
                             toolbox_opts=opts.ToolboxOpts(feature={'dataView':{'readOnly':False},'magicType':{'type':['line','bar']}}),
                             axispointer_opts=opts.AxisPointerOpts(is_show=True, label=opts.LabelOpts(is_show=True, background_color='rgb(123,123,123,1)')))
            
        )
        # 遍历可变的数据，显示所有
        for k, v in y.items():
            c.add_yaxis(k, v,label_opts=opts.LabelOpts(is_show=False))
        c.render("../测试折线图-创业板-沪深300.html")
        return c

    @classmethod
    def showChart(self):
        app = QApplication(sys.argv)
        ex = MyChart()
        ex.show()
        sys.exit(app.exec_())




class MyGrid:

    @classmethod
    def grid_etf(self):
        etf: DataFrame = jukuang_test.read_data_from_local('../../jukuang_data/512880_证券ETF.csv')
        etf = etf.dropna()

        p0 = etf.loc[etf.index[0]]['Open']
        print(p0)
        print(len(etf))

        print(etf)
        first_money = 100000  # 初始本金
        now_money = 0  # 当前剩余的本金
        hold = 0  # 持仓数量
        hold = first_money / 2 // (100 * p0)
        now_money = first_money - (p0 * hold * 100)
        print('hold=', hold)
        print("start_Now_money=",now_money)
        tack_series = pd.Series([first_money], index=[etf.index[0]])
        for i in range(1, len(etf)):
            p_open = etf.loc[etf.index[i]]['Open']
            p_low = etf.loc[etf.index[i]]['Low']
            p_close = etf.loc[etf.index[i]]['Close']
            if p_open > p_low + 0.005:
                new_hold = now_money // (100 * (p_open - 0.005))  # 新增持仓
                now_money -= new_hold * (100 * (p_open - 0.005))  # 可用金额更新
                hold += new_hold
                half_hold = hold // 2  # 拿出当前持仓卖出半仓
                now_money += half_hold * (100 * p_close)
                hold -= half_hold
                # 开始计算当前总金额存入到Series中
                total_money = now_money + hold * (p_close * 100)
                tack_series.loc[etf.index[i]] = total_money
                # print("index=",etf.index[i])



        now_money = now_money + hold * (etf.loc[etf.index[-1]]['Close'] * 100)
        print(now_money)
        plt.plot(etf['Open'] / etf['Open'][0] * 100000, label="123")
        # (etf['ma30']/etf['Open'][0]*100000).plot()
        plt.plot(tack_series, label='abc')
        plt.legend(loc='best')
        plt.show()
        print(tack_series)

    @classmethod
    def get_rolling_rate(self):
        trading_days = 20
        # 获取沪深300数据
        name, hushen300_df = eastStock.request_shangzheng_shenzheng('000300', ctype=1, klt="101", fqt="2",lmt='40')
        hushen300_df.set_index('date',inplace=True)
        hushen300_sum_rate = hushen300_df['涨跌幅度'].rolling(trading_days).sum()
        print(name,hushen300_df[-1:])
        print("hushen300_sum_rate",hushen300_sum_rate[-10:])

        name, chuangye_df = eastStock.request_shangzheng_shenzheng('399006', ctype=0, klt="101", fqt="2",lmt='40')
        chuangye_df.set_index('date',inplace=True)
        chuagnye_sum_rate = chuangye_df['涨跌幅度'].rolling(trading_days).sum()
        print(name,chuangye_df[-1:])
        print("chuagnye_sum_rate",chuagnye_sum_rate[-10:])

    @classmethod
    def RotationStrategy(self):
        '''
        轮动策略，测试每个月轮动一次，如果A的涨幅超过B，那么下个月就卖出A买入B，否则相反。
        '''
        # 从文件中读取数据
        zhongxin_df = pd.read_csv("unused/300015_爱尔眼科后复权周K.csv",index_col=1)
        dongcai_df = pd.read_csv("unused/300059_东方财富后复权周K.csv",index_col=0)

        # zhongxin_df.set_index('date',inplace=True)
        dongcai_df.set_index('date',inplace=True)
        print(zhongxin_df.head())
        print(dongcai_df.head())
        # print(zhongxin_df.loc['2003-01-29'])
        # print(zhongxin_df.index.tolist())

        dongcai_indexs = dongcai_df.index.tolist()
        zhongxin_index = zhongxin_df.index.tolist()
        test_indexs = dongcai_indexs[-300:]

        rotation_sum = 1  # 初始资金默认为1
        zhongxin_sum = 1
        dongcai_sum = 1
        rotation_arr = [1]
        zhongxin_arr = [1]
        dongcai_arr = [1]
        plt_x_arr = [0]
        for index, date in enumerate(test_indexs):
            if index == 0:
                continue
            pre_date = test_indexs[index - 1]
            if date in dongcai_indexs and date in zhongxin_index and pre_date in dongcai_indexs and pre_date in zhongxin_index:
                pass
            else:
                continue
            # 计算上个月的涨跌幅
            pre_zhongxin_rate = zhongxin_df.loc[pre_date]['涨跌幅度']
            pre_dongcai_rate = dongcai_df.loc[pre_date]['涨跌幅度']
            
            zhongxin_rate = zhongxin_df.loc[date]['涨跌幅度']
            dongcai_rate = dongcai_df.loc[date]['涨跌幅度']

            # 如果三个月的涨幅较大，就切换到另一只股票
            if pre_zhongxin_rate > pre_dongcai_rate:
                rotation_sum *= (1 + dongcai_rate / 100.0)
            else:
                rotation_sum *= (1 + zhongxin_rate / 100.0)
            zhongxin_sum *= (1 + zhongxin_rate / 100.0)
            dongcai_sum *= (1 + dongcai_rate / 100.0)

            rotation_arr.append(rotation_sum)
            zhongxin_arr.append(zhongxin_sum)
            dongcai_arr.append(dongcai_sum)
            plt_x_arr.append(date)
            print(date)
            print(index)
            print("zhongxin_sum=",zhongxin_sum)
            print("dongcai_sum",dongcai_sum)
            print("Rotation_sum=",rotation_sum)
            #前复权 7.21 20.71
            # 后复权 33.85 80.43
        plt.plot(plt_x_arr,rotation_arr,label='rotation')
        plt.plot(plt_x_arr,dongcai_arr,label='dongcai')
        plt.plot(plt_x_arr,zhongxin_arr,label='zhongxin')
        plt.legend()
        plt.show()
        # close = zhongxin_df.loc['2003-01-29']['close']
        # print(close)
        # print(type(close))

    @classmethod
    def XBXRotationStrategy(self):
        '''
        邢不行的轮动策略：
        在两个品种之间轮动，通过比较过去的N个交易日的涨跌幅，如果大盘涨幅大于小盘则下日持有大盘，否则持有小盘；
        这个策略的思路是，通过观察过去的交易日强者恒强，如果反转就转到另一个品种。
        '''
        hushen300_df = pd.read_csv('unused/000300_沪深300后复权日K.csv', index_col=1)
        chuangye_df = pd.read_csv('unused/399006_创业板指后复权日K.csv', index_col=1)
        
        print(hushen300_df.head())
        print(chuangye_df.head())
        # 计算过去的20个交易日的 涨跌幅
        trading_days = 20 # 周期
        # ⚠️ 通过累加得到的数据有偏差，涨跌的基准数据会有变化
        chuangye_sum_rate = chuangye_df['涨跌幅度'].rolling(trading_days).sum()
        hushen300_sum_rate = hushen300_df['涨跌幅度'].rolling(trading_days).sum()
        print("chuangye_sum_rate=",chuangye_sum_rate)
        
        # 回撤的天数
        test_count = 2800
        

        # 比较过去20个交易日大小盘的涨跌幅
        isBigger = chuangye_sum_rate[-test_count:] > hushen300_sum_rate[-test_count:] 
        print("isBiggertype",type(isBigger))
        print("chuangye_sum_rate.type",type(chuangye_sum_rate))
        # 通过shift进行错开
        pre_isBigger = isBigger.shift(1)
        pre_isBigger.dropna(axis=0,inplace=True)

        chuangye_sum_rate = chuangye_sum_rate.shift(1)
        hushen300_sum_rate = hushen300_sum_rate.shift(1)
        # 先拼接起，后面用于计算是否空仓
        combo_df = pd.concat([pre_isBigger, chuangye_sum_rate, hushen300_sum_rate, chuangye_df['涨跌幅度'], hushen300_df['涨跌幅度']], axis=1)
        combo_df.columns = ["pre_isBigger","chuangye_sum_rate","hushen300_sum_rate","chuangye_day_rate","hushen300_day_df"]
        # 修改涨跌幅，如果两个板块前20个交易日收益率为负数，后面就清仓，也就是收益率为0 ，这样可以控制回撤
        def getNew_chuanye_zdf(x):
            """
            如前20日创业板收益率大于0那么保留仓位，否则下一交易日就空仓
            """
            # return x["chuangye_day_rate"]
            return x["chuangye_day_rate"] if x["chuangye_sum_rate"] > 0  else 0
        chuangye_zdf = combo_df.apply(getNew_chuanye_zdf,axis=1)

        def getNew_hushen300_zdf(x):
            """
            如前20日沪深300收益率大于0保留仓位，否则下一交易日就空仓
            """
            # return x["hushen300_day_df"]
            return x["hushen300_day_df"] if  x["hushen300_sum_rate"] > 0 else 0
        hushen300_zdf = combo_df.apply(getNew_hushen300_zdf,axis=1)
        
        chuangye_rate = pre_isBigger * chuangye_zdf
        
        hushen300_rate = pre_isBigger.apply(lambda x: not x) * hushen300_zdf 
        

        rotation_rate = chuangye_rate + hushen300_rate
        rotation_rate.dropna(inplace=True)
        # test
        print("hushen300_rate.len=", len(hushen300_rate))
        print("chuangye_rate.len=", len(chuangye_rate))
        print("rotation_rate.len=", len(rotation_rate))

        print("hushen300_rate.count=", hushen300_rate.count())
        print("chuangye_rate.count=", chuangye_rate.count())
        print("rotation_rate.count=", rotation_rate.count())

        print("chuangye_sum_rate.count=", chuangye_sum_rate.count())
        print("hushen300_sum_rate.count=", hushen300_sum_rate.count())
        total_money = 1
        total_arr = [1]
        for rate in rotation_rate:
            total_money *= (1+rate/100.0)
            total_arr.append(round(total_money, 3))
        
        print(total_money)

        chuangye_momoney = 1
        chuangye_rate.dropna(inplace=True)
        for rate in chuangye_rate:
            chuangye_momoney *= (1+rate/100.0)
        print("单调并网格创业板",chuangye_momoney)

        hushen300_money = 1
        hushen300_rate.dropna(inplace=True)
        for rate in hushen300_rate:
            hushen300_money *= (1+rate/100.0)
        print("单调网格沪深300",hushen300_money)

        print("----====----")
        chuangye_momoney = 1
        chuangye_arr = []
        for rate in chuangye_df['涨跌幅度'][-test_count:]:
            chuangye_momoney *= (1+rate/100.0)
            chuangye_arr.append(chuangye_momoney)
        print("长期持有创业板：",chuangye_momoney)

        hushen300_money = 1
        hushen300_arr = []
        for rate in hushen300_df['涨跌幅度'][-test_count:]:
            hushen300_money *= (1+rate/100.0)
            hushen300_arr.append(hushen300_money)
        print("长期持有沪深300",hushen300_money)

        # return
        x_arr = [0] + rotation_rate.index.tolist()
        # plt.plot(x_arr,total_arr,label='rotation')
        # plt.plot(x_arr,chuangye_arr,label='chuangye')
        # plt.plot(x_arr,hushen300_arr,label='hushen300')
        # plt.legend()
        # plt.show()
        y={"1.轮动策略": total_arr, "2.创业板": chuangye_arr, "3.沪深300": hushen300_arr}
        # 开始存入到文件，并绘制成折线图
        MyChart.line_base(x=x_arr, **y)


# MyGrid.XBXRotationStrategy()

# MyGrid.get_rolling_rate()

# MyChart.showChart()
# python3 Stategy/mygrid.py



# 分割线
# hushen300_df = pd.read_csv('unused/000300_沪深300后复权日K.csv', index_col=1)

# def testF(x):
#     print(x)
#     return x


# abc = hushen300_df[-10:]
# print(abc)
# abc.apply(testF,axis=1)