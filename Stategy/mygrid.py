# 我的策略，该模块用于测试每个策略的收益率
from typing import List
import matplotlib.pyplot as plt

import sys
from pathlib import Path
import time
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.charts import Line,Bar,Grid, Pie
import pyecharts.options as opts
from pyecharts import charts
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
    def line_base(self, x: List, fileName: str, retracement: DataFrame, **y) -> Line:
        '''
        绘制折线图
        '''
        c = (
            Line()
            .add_xaxis(x)
            .set_global_opts(title_opts=opts.TitleOpts(title="收益曲线"),
                             tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
                             yaxis_opts=opts.AxisOpts(name="收益率"),
                             toolbox_opts=opts.ToolboxOpts(feature={'dataView': {'readOnly': False}, 'magicType': {'type': ['line', 'bar']}}),
                             axispointer_opts=opts.AxisPointerOpts(is_show=True, label=opts.LabelOpts(is_show=True, background_color='rgb(123,123,123,1)')),
                             datazoom_opts=[opts.DataZoomOpts(type_='inside', range_start=0, range_end=100, xaxis_index=0),
                             opts.DataZoomOpts(pos_bottom='50%', range_start=0, range_end=100, xaxis_index=0),
                             opts.DataZoomOpts(type_='inside', range_start=0, range_end=100, xaxis_index=1),
                             opts.DataZoomOpts(pos_bottom='0%', range_start=0, range_end=100, xaxis_index=1)],
                             )
        )
        # c.width = "95%"
        # c.height = "800px"
        c.page_title = "收益曲线"
        # 遍历可变的数据，显示所有
        
        my_markpoint_data = []
        my_markarea_data = []
        for row in retracement.itertuples():
            begin_date = getattr(row, 'begin_date')
            begin_number =  getattr(row, 'begin_number')
            end_date = getattr(row, 'end_date')
            end_number = getattr(row, 'end_number')
            rate = getattr(row, 'retracement')
            my_markpoint_data.append(opts.MarkPointItem(name='test', coord=[begin_date, begin_number], value=begin_number))
            my_markpoint_data.append(opts.MarkPointItem(name='test', coord=[end_date, end_number], value=end_number))
            my_markarea_data.append(opts.MarkAreaItem(name=round(-rate*100, 2), x=(begin_date, end_date), y=(end_number, begin_number)))
            
        # 开始绘制折线
        for k, v in y.items():
            
            # color = line_colors.pop
            c.add_yaxis(k, v,label_opts=opts.LabelOpts(is_show=True,interval=10),
                        linestyle_opts=opts.LineStyleOpts(width=1.5),
                        xaxis_index=0,
                        yaxis_index=0
                        # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="test", x="2021-09-13", symbol_size=20), opts.MarkLineItem(name="test", x="2021-10-25", symbol_size=20)]),
                        # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name='test', coord=["2021-10-25",3],value=2)])
                        )
        # 需要有数据之后设置的属性才能生效
        c.set_series_opts(markarea_opts=opts.MarkAreaOpts(itemstyle_opts=opts.ItemStyleOpts(color='rgba(20, 255, 20, 0.1)'),
                                                        #   data=[opts.MarkAreaItem(name='morning Peak', x=('2020-06-03', '2021-07-09'))]
                                                        data= my_markarea_data,
                                                        label_opts=opts.LabelOpts(color='black'),
                                                        is_silent=True
                                                          ),
                        #   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max', name='最大值'), opts.MarkPointItem(type_='min',name='最小值'), opts.MarkPointItem(name='test', value=3,x=30,y=3)])
                        # 设置显示的标签样式，
                        # label_opts=opts.LabelOpts(interval=100),
                        # tooltip_opts=opts.marklin
                          )
        # 用于计算年收益
        rate_df = DataFrame(y)
        rate_df["date"] = x
        rate_df.set_index('date')

        c1 = self.gender_mi(pos_top='55%',x=x,y=y)
        # c.overlap(c1)
        grid = Grid(init_opts=opts.InitOpts(width="95%", height="1200px", page_title="轮动策略"))

        grid.add(c, grid_opts=opts.GridOpts(pos_bottom="55%"))
        grid.add(c1, grid_opts=opts.GridOpts(pos_top="55%"))

        grid.render(fileName)
        # c.render(fileName)
        return c

    @classmethod
    def gender_mi(self, x: List, y:dict, pos_top='60%'):
        # 获取每年的最后一个交易日
        print("开始获取月份第一个交易日数据：---=====---")
        offset = pd.tseries.offsets.YearEnd()
        
        bar = (Bar()
               .set_global_opts(title_opts=opts.TitleOpts(title="年收益", pos_top=pos_top),
                                legend_opts=opts.LegendOpts(pos_top=pos_top),
                                # 目前发现只能在第一个图标设置缩放属性
                                # datazoom_opts=[opts.DataZoomOpts(type_='inside', range_start=0, range_end=100, xaxis_index=[0, 1, 2], yaxis_index=[0, 1, 2]),
                                #                opts.DataZoomOpts(pos_bottom='50%', range_start=0, range_end=100, xaxis_index=1, yaxis_index=1)],
                                )
               )

        has_set_xaxis = False
        for k, v in y.items():
            ser = Series(v,index=x)
            ser = ser.groupby(offset.rollforward,group_keys=False).apply(lambda t: t[t.index == t.index.max()])
            if not has_set_xaxis:
                # 只要设置一次X坐标
                bar.add_xaxis(ser.index.tolist()[1:])
                has_set_xaxis = True
            year_rate = ser/ser.shift(1)
            bar.add_yaxis(k,((year_rate-1)*100).round(3).tolist()[1:],xaxis_index=1,yaxis_index=1)
        bar.set_series_opts(label_opts=opts.LabelOpts(formatter='{c}%'))
        return bar

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
    def XBXRotationStrategy(self, hushen300_df: DataFrame, chuangye_df: DataFrame, test_count=100, trading_days=20,
                            hushen300_name="1.沪深300", chuangye_name="2.创业板", fileName="../测试折线图-创业板-沪深300.html", testRate=0.2, **kwargs):
        '''
        邢不行的轮动策略：
        在两个品种之间轮动，通过比较过去的N个交易日的涨跌幅，如果大盘涨幅大于小盘则下日持有大盘，否则持有小盘；
        这个策略的思路是，通过观察过去的交易日强者恒强，如果反转就转到另一个品种。
        params:
        hushen300_df: 第一个行情数据
        chuangye_df: 第二个行情数据
        test_count: 回测的天数
        trading_days: 短期的涨跌幅计算周期
        '''
        # hushen300_df = pd.read_csv('unused/000300_沪深300后复权日K.csv', index_col=1)
        # chuangye_df = pd.read_csv('unused/399006_创业板指后复权日K.csv', index_col=1)
        
        print(hushen300_df.head())
        print(chuangye_df.head())
        # 计算过去的20个交易日的 涨跌幅
        # trading_days = 20 # 周期
        # ⚠️ 通过累加得到的数据有偏差，涨跌的基准数据会有变化
        chuangye_sum_rate = chuangye_df['涨跌幅度'].rolling(trading_days).sum()
        hushen300_sum_rate = hushen300_df['涨跌幅度'].rolling(trading_days).sum()

        print("chuangye_sum_rate=",chuangye_sum_rate)
        print("hushen300_sum_rate=",hushen300_sum_rate)

        # 由于有些板块会存在同一日期有空的情况
        combo_sum_rate_df = pd.concat([chuangye_sum_rate, hushen300_sum_rate], axis=1)
        combo_sum_rate_df.columns = ["chuangye_sum_rate", "hushen300_sum_rate"]
        # 按照日期索引排序，防止部分年份出现穿插的情况。
        combo_sum_rate_df.sort_index(axis=0,ascending=True,inplace=True)
        
        chuangye_sum_rate = combo_sum_rate_df["chuangye_sum_rate"]
        hushen300_sum_rate = combo_sum_rate_df["hushen300_sum_rate"]

        # 加入短期的10日涨跌幅
        chuangye_ten_rate = chuangye_df['涨跌幅度'].rolling(10).sum()
        hushen300_ten_rate = hushen300_df['涨跌幅度'].rolling(10).sum()

        chuangye_ten_rate = chuangye_ten_rate.shift(1)
        hushen300_ten_rate = hushen300_ten_rate.shift(1)

        # 回撤的天数
        # test_count = 1160

        # 比较过去20个交易日大小盘的涨跌幅
        isBigger = chuangye_sum_rate[-test_count:] > hushen300_sum_rate[-test_count:] 
        print("isBiggertype",type(isBigger))
        print("chuangye_sum_rate.type",type(chuangye_sum_rate))
        # 通过shift进行错开，用于判断前一日，防止出现未来函数的情况。
        pre_isBigger = isBigger.shift(1)
        pre_isBigger.dropna(axis=0,inplace=True)

        chuangye_sum_rate = chuangye_sum_rate.shift(1)
        hushen300_sum_rate = hushen300_sum_rate.shift(1)

        # 计算均线,不一定会用到
        averages_five = chuangye_df["涨跌幅度"].rolling(5).mean()
        averages_ten = chuangye_df["涨跌幅度"].rolling(10).mean()
        chuangye_average_bigger = averages_five < averages_ten
        chuangye_average_bigger = chuangye_average_bigger.shift(1)

        averages_five = hushen300_df["涨跌幅度"].rolling(5).mean()
        averages_ten = hushen300_df["涨跌幅度"].rolling(10).mean()
        hushen300_arerage_bigger = averages_five < averages_ten
        hushen300_arerage_bigger = hushen300_arerage_bigger.shift(1)
        # 获取杠杆率，long是做多，short是做空,默认不加杠杆，不做空
        long_leverage = kwargs.get('long', 1)
        short_leverage = kwargs.get("short", 0)
        print("做多杠杆率={},做空杠杆率={}".format(long_leverage, short_leverage))
        
        # 先拼接起，后面用于计算是否空仓
        combo_df = pd.concat([pre_isBigger, chuangye_sum_rate, hushen300_sum_rate, chuangye_df['涨跌幅度'],
                             hushen300_df['涨跌幅度'], chuangye_ten_rate, hushen300_ten_rate, chuangye_average_bigger, hushen300_arerage_bigger], axis=1)
        combo_df.columns = ["pre_isBigger", "chuangye_sum_rate", "hushen300_sum_rate",
                            "chuangye_day_rate", "hushen300_day_df", "chuangye_ten_rate", "hushen300_ten_rate", "chuangye_average_bigger", "hushen300_arerage_bigger"]
        # 修改涨跌幅，如果两个板块前20个交易日收益率为负数，后面就清仓，也就是收益率为0 ，这样可以控制回撤
        def getNew_chuanye_zdf(x):
            """
            如前20日创业板收益率大于0那么保留仓位，否则下一交易日就空仓
            """
            # return x["chuangye_day_rate"]
            return x["chuangye_day_rate"] * long_leverage if x["chuangye_sum_rate"] > 3.0 and x["chuangye_sum_rate"] < 30 else 0 - x["hushen300_day_df"] * short_leverage
        chuangye_zdf = combo_df.apply(getNew_chuanye_zdf,axis=1)

        def getNew_hushen300_zdf(x):
            """
            如前20日沪深300收益率大于0保留仓位，否则下一交易日就空仓
            """
            # return x["hushen300_day_df"]
            return x["hushen300_day_df"] * long_leverage if x["hushen300_sum_rate"] > 3.0 and x["hushen300_sum_rate"] < 30 else 0 - x["chuangye_day_rate"] * short_leverage
        hushen300_zdf = combo_df.apply(getNew_hushen300_zdf,axis=1)
        
        chuangye_rate = pre_isBigger * chuangye_zdf
        
        hushen300_rate = pre_isBigger.apply(lambda x: not x) * hushen300_zdf 
        

        rotation_rate = chuangye_rate + hushen300_rate
        # test
        combo_df["rotation_rate"] = rotation_rate
        # print("combo_df=",combo_df)
        combo_df.sort_index(axis=0, ascending=True, inplace=True)
        combo_df.to_csv("../testcombo_df.csv")
        print("rotation_rate=",rotation_rate)
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
        
        print("策略收益率:",total_money)

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
            chuangye_arr.append(round(chuangye_momoney, 4))
        print("长期持有创业板：",chuangye_momoney)

        hushen300_money = 1
        hushen300_arr = []
        for rate in hushen300_df['涨跌幅度'][-test_count:]:
            hushen300_money *= (1+rate/100.0)
            hushen300_arr.append(round(hushen300_money, 3))
        print("长期持有沪深300",hushen300_money)

        # return
        x_arr = [0] + rotation_rate.index.tolist()
        print("策略最大回撤=", self.get_max_withdraw(Series(total_arr, index=x_arr)))
        # statistical_retracement_data(ser, rate=0.3)
        retracement_df = self.statistical_retracement_data(Series(total_arr, index=x_arr), rate=testRate)
        
        y = {"3.轮动策略": total_arr, chuangye_name: chuangye_arr, hushen300_name: hushen300_arr}
        # 开始存入到文件，并绘制成折线图
        MyChart.line_base(x=x_arr, fileName=fileName, retracement=retracement_df, **y)
        
    @classmethod
    def XBXTestLocalFile(self):
        """
        从文件读取并进行回测
        """
        hushen300_df = pd.read_csv('unused/000300_沪深300后复权日K.csv', index_col=1)
        chuangye_df = pd.read_csv('unused/399006_创业板指后复权日K.csv', index_col=1)
        self.XBXRotationStrategy(chuangye_df=chuangye_df, hushen300_df=hushen300_df, test_count=2800, trading_days=20,
                                 hushen300_name="1.沪深300", chuangye_name="2.创业板", fileName="../测试结果-创业板-沪深300_0408_1.5_0.5.html",long=1.5, short=.5)
    
    @classmethod
    def XBXTestServiceData(self):
        
        test_days = 1300
        hushen_name, hushen_df = eastStock.request_shangzheng_shenzheng(510300, ctype=1, klt="101", fqt="2", lmt=test_days)
        chuangye_name, chuangye_df = eastStock.request_shangzheng_shenzheng(159949, ctype=0, klt="101", fqt="2", lmt=test_days)
        hushen_df.set_index('date', inplace=True)
        chuangye_df.set_index('date', inplace=True)

        today = datetime.datetime.today()
        date_str = today.strftime('%Y-%m-%d')
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        my_weak = week_list[today.weekday()]
        # 保存临时数据用于人工比对交易
        # hushen_df.to_csv("../{}_短期行情数据{}.csv".format(hushen_name,date_str))
        # chuangye_df.to_csv("../{}_短期行情数据{}.csv".format(chuangye_name,date_str))

        self.XBXRotationStrategy(chuangye_df=chuangye_df, hushen300_df=hushen_df, test_count=test_days-20, hushen300_name="1.{}".format(hushen_name), chuangye_name="2.{}".format(chuangye_name), fileName="../测试结果_{hushen}_{chuangye}_{xinqi}_{date}.html".
                                 format(hushen=hushen_name, chuangye=chuangye_name, xinqi=my_weak, date=date_str), long=1.5, short=.5,testRate=0.1)

    @classmethod
    def TrendStrategy(self):
        """
        趋势投资，根据前20个交易日的收益，决定是否继续持有或者空仓
        """
        stock_df = pd.read_csv('unused/300059_东方财富后复权日K.csv', index_col=1)
        # stock_df.set_index('date',inplace=True)
        # 计算过去的20个交易日的 涨跌幅
        trading_days = 20 # 周期
        # 回测的交易天数
        test_count = 1300
        # ⚠️ 通过累加得到的数据有偏差，涨跌的基准数据会有变化
        stock_sum_rate = stock_df['涨跌幅度'].rolling(trading_days).sum()
        stock_sum_rate = stock_sum_rate.shift(1)

        # 计算金叉
        averages_five = stock_df["涨跌幅度"].rolling(5).mean()
        averages_ten = stock_df["涨跌幅度"].rolling(10).mean()
        average_bigger = averages_five > averages_ten
        average_bigger = average_bigger.shift(1)

        # 先拼接起，后面用于计算是否空仓
        combo_df = pd.concat([stock_sum_rate, stock_df['涨跌幅度'], average_bigger], axis=1)
        combo_df.columns = ["stock_sum_rate", "stock_day_rate", 'average_bigger']
        # 修改涨跌幅，如果两个板块前20个交易日收益率为负数，后面就清仓，也就是收益率为0 ，这样可以控制回撤
        
        print("combo_df==",combo_df)
        def getNew_stock_zdf(x):
            """
            如前20日创业板收益率大于0那么保留仓位，否则下一交易日就空仓
            """
            # return x["stock_day_rate"]
            return x["stock_day_rate"] if x["stock_sum_rate"] > 2 and not x["average_bigger"] else 0
        
        stock_zdf = combo_df.apply(getNew_stock_zdf,axis=1)
        stock_zdf = stock_zdf[-test_count:]
        stock_zdf.dropna(inplace=True)
        print("stock_zdf==",stock_zdf)
        total_money = 1
        total_arr = []
        for rate in stock_zdf:
            total_money *= (1+rate/100.0)
            total_arr.append(round(total_money, 3))
        
        origin_money = 1
        origin_arr = []
        for rate in stock_df['涨跌幅度'][-test_count:]:
            origin_money *= (1+rate/100.0)
            origin_arr.append(origin_money)
        
        print("趋势收益",total_money)
        print("长期持有收益",origin_money)

        x_arr = stock_zdf.index.tolist()
        y={"1.趋势": total_arr, "2.长期持有": origin_arr}
        # 开始存入到文件，并绘制成折线图
        MyChart.line_base(x=x_arr,fileName="../趋势策略收益.html", **y)

    @classmethod
    def MaxDrawdown(self,return_list):
        """
        最大回撤函数,
        该函数不是最大回撤率，而是计算最大回撤的数,是和计算账户的金额回撤
        """
        i = np.argmax(np.maximum.accumulate(return_list) - return_list)
        if i == 0:
            return 0, 0, 0, 0
        j = np.argmax(return_list[:i])
        drawdown_max = return_list[j] - return_list[i]
        drawdown_rate = (return_list[j] - return_list[i]) / return_list[j]
        days = i - j
        return drawdown_rate, drawdown_max, days, j,i
    
    @classmethod
    def get_max_withdraw(self,indexs):
        '''
        计算最大回撤率
        return:
        max_withdraw：最大回撤率
        max_leading_index:开始下跌时间
        max_trailing_index:下跌截止时间
        '''
        max_withdraw = 0
        max_leading_index = 0
        max_trailing_index = 0
        last_high = indexs[0]
        last_high_index = 0
        for index, current in indexs.items() if isinstance(indexs, Series) else enumerate(indexs):
            # 遍历所有的数据
            if current > last_high:
                last_high = current
                last_high_index = index
                continue
            if (last_high - current)/last_high > max_withdraw:
                # 找到一个最大值时，保存其位置
                max_withdraw = (last_high - current)/last_high
                max_leading_index = last_high_index
                max_trailing_index = index
        return max_withdraw, max_leading_index, max_trailing_index

    @classmethod
    def statistical_retracement_data(self, datas:Series, rate=0.2):
        """
        统计出所有数据从历史高点回撤超过20%的数据
        """
        history_high = datas[0]
        history_high_date = datas.index[0]
        temp_high_rate = 0
        current_number = 0
        end_date = datas.index[0]
        print("第一个数据date={},obj={}".format(history_high_date, history_high))
        
        # history_df = DataFrame(columns=["begin_date", "end_date", "retracement",
        #                         "begin_number", "end_number"])
        # print("history_df_test=",history_df)

        begin_dates = []
        end_dates = []
        retracements = []
        begin_numbers = []
        end_numbers = []
        
        for date, obj in datas[:].items():
                
            if obj > history_high:
                # 找到历史高点，先保存上次的
                if temp_high_rate > rate:
                    # print("开始记录数据")
                    begin_dates.append(history_high_date)
                    end_dates.append(end_date)
                    retracements.append(temp_high_rate)
                    begin_numbers.append(history_high)
                    end_numbers.append(current_number)

                history_high_date = date
                history_high = obj
                temp_high_rate = 0 # 重置
                current_number = 0
                # print('history_high_date=',history_high_date)
            
            elif obj < history_high:
                current_rate = 1 - obj / history_high
                
                if current_rate > rate and current_rate > temp_high_rate:
                    # 如果短期回撤较大就保留
                    temp_high_rate = current_rate
                    current_number = obj
                    end_date = date
                    # print("获取回撤大于上次且大于:",rate)
                    # print("date={},temp_high_rate={},rate={}".format(date, temp_high_rate, rate))
        # 如果最后一次回撤也满足条件，也要加入
        if temp_high_rate > rate:
            begin_dates.append(history_high_date)
            end_dates.append(end_date)
            retracements.append(temp_high_rate)
            begin_numbers.append(history_high)
            end_numbers.append(current_number)

        history_df = DataFrame({"begin_date": begin_dates, "end_date": end_dates, "retracement": retracements,
                                "begin_number": begin_numbers, "end_number": end_numbers})
        # print("history_df=\n",history_df)
        return history_df



                

            
# abc = [1,2,5,1,4,1,5,8,5,2,3,9,4,3,4]

# dates = ['2022-03-31','2022-04-01','2022-04-06','2022-04-07','2022-04-08','2022-04-09','2022-04-10','2022-04-11','2022-04-12','2022-04-13','2022-04-14','2022-04-15','2022-04-16','2022-04-17','2022-04-18']

# ser = Series(abc,dates)

# # aaa = MyGrid.get_max_withdraw(ser)
# # aaa = MyGrid.MaxDrawdown(ser)
# print(ser)
# aaa = np.maximum.accumulate(ser)
# print(aaa)
# bbb = aaa - abc
# print('bbb=',bbb/aaa)

# MyGrid.statistical_retracement_data(ser, rate=0.3)

