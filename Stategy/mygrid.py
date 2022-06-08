# 我的策略，该模块用于测试每个策略的收益率
from typing import Dict, List
import matplotlib.pyplot as plt

import sys
from pathlib import Path
import time
import datetime

from sqlalchemy import false

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
import numpy as np

from pandas import DataFrame, Series, DatetimeIndex
from plot_test import jukuang_test
from eastmoney.fetchData.stock import eastStock
# from GUI.my_chart import MyChart

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
    def get_rolling_rate(self, stock1=('000300', 1), stock2=('399006', 0),trading_days = 20):
        # 获取沪深300数据
        hushen_name, hushen300_df = eastStock.request_shangzheng_shenzheng(stock1[0], ctype=stock1[1], klt="101", fqt="2",lmt='40')
        hushen300_df.set_index('date',inplace=True)
        hushen300_sum_rate = hushen300_df['涨跌幅度'].rolling(trading_days).sum()
        print(hushen_name,hushen300_df[-1:])
        print("hushen300_sum_rate",hushen300_sum_rate[-10:])

        chuangye_name, chuangye_df = eastStock.request_shangzheng_shenzheng(stock2[0], ctype=stock2[1], klt="101", fqt="2",lmt='40')
        chuangye_df.set_index('date',inplace=True)
        chuagnye_sum_rate = chuangye_df['涨跌幅度'].rolling(trading_days).sum()
        print(chuangye_name,chuangye_df[-1:])
        print("chuagnye_sum_rate",chuagnye_sum_rate[-10:])
        return (hushen_name + str(hushen300_sum_rate[-10:].round(4).to_dict()), chuangye_name + str(chuagnye_sum_rate[-10:].round(4).to_dict()))

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

    @classmethod
    def XBXRotationStrategy(self, hushen300_df: DataFrame, chuangye_df: DataFrame, gold_df: DataFrame, test_count=100, trading_days=20, sub_rate=3.0, testRate=0.2, **kwargs):
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

        # 获取杠杆率，long是做多，short是做空,默认不加杠杆，不做空
        long_leverage = kwargs.get('long', 1)
        short_leverage = kwargs.get("short", 0)
        print("做多杠杆率={},做空杠杆率={}".format(long_leverage, short_leverage))
        
        # 先拼接起，后面用于计算是否空仓
        combo_df = pd.concat([pre_isBigger, chuangye_sum_rate, hushen300_sum_rate, chuangye_df['涨跌幅度'], hushen300_df['涨跌幅度'],gold_df['涨跌幅度']], axis=1)
        combo_df.columns = ["pre_isBigger", "chuangye_sum_rate", "hushen300_sum_rate", "chuangye_day_rate", "hushen300_day_rate","gold_day_rate"]
        combo_df.sort_index(axis=0,inplace=True)
        combo_df = combo_df[-test_count:]
        
        # 统计对各个指数看多看空
        trading_count = {"long_chuangye": 0, "short_chuangye": 0, "long_hushen300": 0, "short_hushen300": 0}
        # 计算贡献的收益率
        revenue_contribution = {"long_chuangye": 1, "short_chuangye": 1, "long_hushen300": 1, "short_hushen300": 1}
        # 修改涨跌幅，如果两个板块前20个交易日收益率为负数，后面就清仓，也就是收益率为0 ，这样可以控制回撤
        def getNew_chuanye_zdf(x):
            """
            如前20日创业板收益率大于0那么保留仓位，否则下一交易日就空仓
            """
            # return x["chuangye_day_rate"]
            if x["chuangye_sum_rate"] > sub_rate and x["chuangye_sum_rate"] < 30:
                if x["pre_isBigger"]:
                    trading_count["long_chuangye"] = trading_count["long_chuangye"] + 1
                    revenue_contribution["long_chuangye"] = revenue_contribution["long_chuangye"] * (1+x["chuangye_day_rate"]/100.0 * long_leverage)
                return x["chuangye_day_rate"] * long_leverage
            else:
                if x["pre_isBigger"]:
                    trading_count["short_hushen300"] = trading_count["short_hushen300"] + 1
                    revenue_contribution["short_hushen300"] = revenue_contribution["short_hushen300"] * (1 - x["hushen300_day_rate"]/100.0 * short_leverage)
                return 0 - x["hushen300_day_rate"] * short_leverage

        chuangye_zdf = combo_df.apply(getNew_chuanye_zdf,axis=1)

        def getNew_hushen300_zdf(x):
            """
            如前20日沪深300收益率大于0保留仓位，否则下一交易日就空仓
            """
            # return x["hushen300_day_rate"]
            if x["hushen300_sum_rate"] > sub_rate and x["hushen300_sum_rate"] < 30:
                if not x["pre_isBigger"]:
                    trading_count["long_hushen300"] = trading_count["long_hushen300"] + 1
                    revenue_contribution["long_hushen300"] = revenue_contribution["long_hushen300"] * (1+x["hushen300_day_rate"]/100.0 * long_leverage)
                return x["hushen300_day_rate"] * long_leverage
            else:
                if not x["pre_isBigger"]:
                    trading_count["short_chuangye"] = trading_count["short_chuangye"] + 1
                    revenue_contribution["short_chuangye"] = revenue_contribution["short_chuangye"] * (1 - x["chuangye_day_rate"]/100.0 * short_leverage)
                return 0 - x["chuangye_day_rate"] * short_leverage

        hushen300_zdf = combo_df.apply(getNew_hushen300_zdf,axis=1)
        print("revenue_contribution=",revenue_contribution)
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
            total_arr.append(round(total_money, 2))
        
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
            chuangye_arr.append(round(chuangye_momoney, 2))
        print("长期持有创业板：",chuangye_momoney)

        hushen300_money = 1
        hushen300_arr = []
        for rate in hushen300_df['涨跌幅度'][-test_count:]:
            hushen300_money *= (1+rate/100.0)
            hushen300_arr.append(round(hushen300_money, 2))
        print("长期持有沪深300",hushen300_money)

        # return
        x_arr = [0] + rotation_rate.index.tolist()
        print("策略最大回撤=", self.get_max_withdraw(Series(total_arr, index=x_arr)))
        # statistical_retracement_data(ser, rate=0.3)
        retracement_df = self.statistical_retracement_data(Series(total_arr, index=x_arr), rate=testRate)
        # return x_arr, total_arr
        y = (total_arr, chuangye_arr, hushen300_arr)
        # 开始存入到文件，并绘制成折线图
        # MyChart.line_base(x=x_arr, fileName=fileName,html_title=html_title, retracement=retracement_df, trading_count=trading_count, revenue_contribution=revenue_contribution, **y)
        return x_arr, y, retracement_df, trading_count, revenue_contribution, hushen300_sum_rate[-len(x_arr):].round(3).to_list(), chuangye_sum_rate[-len(x_arr):].round(3).to_list()
        
    @classmethod
    def XBXTestLocalFile(self):
        """
        从文件读取并进行回测
        """
        hushen300_df = pd.read_csv('unused/000300_沪深300后复权日K.csv', index_col=1)
        chuangye_df = pd.read_csv('unused/399006_创业板指后复权日K.csv', index_col=1)
        return self.XBXRotationStrategy(chuangye_df=chuangye_df, hushen300_df=hushen300_df, test_count=2800, trading_days=20,
                                 hushen300_name="1.沪深300", chuangye_name="2.创业板", fileName="../测试结果-创业板-沪深300_0408_1.5_0.5.html",long=1.5, short=.5)
    
    @classmethod
    def XBXTestServiceData(self, sub_rate=3.0, stocks=( (159949, "0"),(510300, "1")), test_days=1300):
        hushen_name, hushen_df = eastStock.request_shangzheng_shenzheng(stocks[0][0], ctype=stocks[0][1], klt="101", fqt=2, lmt=test_days)
        chuangye_name, chuangye_df = eastStock.request_shangzheng_shenzheng(stocks[1][0], ctype=stocks[1][1], klt="101", fqt=2, lmt=test_days)
        gold_name, gold_df = eastStock.request_shangzheng_shenzheng(518880, ctype=1, klt="101", fqt=2, lmt=test_days)
        hushen_df.set_index('date', inplace=True)
        chuangye_df.set_index('date', inplace=True)
        gold_df.set_index('date', inplace=True)

        # 保存临时数据用于人工比对交易
        # hushen_df.to_csv("../{}_短期行情数据{}.csv".format(hushen_name,date_str))
        # chuangye_df.to_csv("../{}_短期行情数据{}.csv".format(chuangye_name,date_str))

        return self.XBXRotationStrategy(chuangye_df=chuangye_df, hushen300_df=hushen_df,gold_df=gold_df, test_count=test_days-20, sub_rate=sub_rate, long=1.5, short=0.5, testRate=0.1) + (chuangye_name, hushen_name)
        return
        my_params = []
        for sub_rate in range(-30,30):
            my_rate = sub_rate/10.0
            print("myrate=",my_rate)
            x,y = self.XBXRotationStrategy(chuangye_df=chuangye_df, hushen300_df=hushen_df, test_count=test_days-20,sub_rate=my_rate, hushen300_name="1.{}".format(hushen_name), chuangye_name="2.{}".format(chuangye_name), fileName="../测试结果_{hushen}_{chuangye}_service.html".
                                    format(hushen=hushen_name, chuangye=chuangye_name),html_title="轮动策略-{xinqi}-{date}".format(xinqi=my_weak,date=date_str), long=1.5, short=.5,testRate=0.1)
            mystack = np.stack([x,y],axis=1).tolist()
            my_params += [[my_rate]+obj for obj in mystack]
        c = (
            Line3D()
            .add("test",data=my_params)
        )
        c.render("../my3dline.html")
        # print("x={},y={}".format(x,y))

    @classmethod
    def TrendStrategy(self):
        """
        趋势投资，根据前20个交易日的收益，决定是否继续持有或者空仓
        """
        roll_date = 20
        # stock = ('scm', 142)
        stock = (399006,'0')
        
        name, df = eastStock.request_shangzheng_shenzheng(stock[0], ctype=stock[1], klt="101", fqt="2", lmt='2800')
        df.set_index('date', inplace=True)
        sum_rate = df['涨跌幅度'].rolling(roll_date).sum().shift(1)  # 避免未来函数，需要用到前一天的数据

        print(df)

        sum_name, day_name = name + "sum_rate", name + "day_rate"
        combo_df = pd.concat([sum_rate, df['涨跌幅度']], axis=1)
        combo_df.columns = [sum_name, day_name]

        print(sum_rate[-1])
        print(combo_df)
        # 当前持仓状态0表示空仓，1表示持有多头，-1表示持有空投
        self.curren_status = 0
        
        self.trading_rate = 0
        def caltest(x):
            # 开始记统计交易盈亏，有误差不大
            self.trading_rate += x[day_name]
            if x[0] > 3:
                if self.curren_status != 1:
                    # 行情反转做多
                    # 先记录上次做空交易记录
                    x['short_rate'] = self.trading_rate
                    self.curren_status = 1
                    self.trading_rate = 0
            elif self.curren_status != -1:
                x['long_rate'] = self.trading_rate
                self.curren_status = -1
                self.trading_rate = 0
            # return x
            return x[1] * 1.5 if x[0] > 3  else -x[1]*.5
        result = combo_df[21:].apply(caltest, axis=1)
        print("result====",result)
        # print('long_rate==',result['long_rate'].count())
        # print('short_rate==',result['short_rate'].count())
        # print(self.KellyCriterion(-result['short_rate']))
        # print(self.KellyCriterion(result['long_rate']))
        # result.to_csv('./test_kailifunc.csv')
        # return
        sum = 1
        for obj in result:
            sum *= (1 + obj/100.0)
        print("sum=", sum)
        print("持有不动=",df['close'][-1]/df['close'][21])

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
            elif obj < history_high:
                current_rate = 1 - obj / history_high
                
                if current_rate > rate and current_rate > temp_high_rate:
                    # 如果短期回撤较大就保留
                    temp_high_rate = current_rate
                    current_number = obj
                    end_date = date
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

    @classmethod
    def IndustryRotation(self):
        # 行业轮动
        # 用于筛选的行业指数
        # indexs = ['SHSE.000910', 'SHSE.000909', 'SHSE.000911', 'SHSE.000912', 'SHSE.000913', 'SHSE.000914']
        indexs = [('000910', 1), ('000909', 1), ('000911', 1), ('000912', 1), ('000913', 1), ('000914', 1)]
        # indexs = [('000300', 1), ('399006', 0)]
        # 用于统计数据的天数
        roll_date = 20

        first = True
        for stock in indexs:
            name, df = eastStock.request_shangzheng_shenzheng(stock[0], ctype=stock[1], klt="101", fqt="2", lmt='1500')
            df.set_index('date', inplace=True)
            sum_rate = df['涨跌幅度'].rolling(roll_date).sum().shift(1)  # 避免未来函数，需要用到前一天的数据

            sum_name, day_name = name + "sum_rate", name + "day_rate"
            if first:
                combo_df = pd.concat([sum_rate, df['涨跌幅度']], axis=1)
                combo_df.columns = [sum_name, day_name]
                first = False
            else:
                combo_df[sum_name] = sum_rate
                combo_df[day_name] = df['涨跌幅度']

            print(sum_rate[-1])
        print(combo_df)

        def caltest(x):
            series1 = x[[i % 2 == 0 for i in range(len(x.index))]]
            series2 = x[[i % 2 == 1 for i in range(len(x.index))]]
            return series2[series1.argmax()] * 1.5 if series1[series1.argmax()] > 3 and series1[series1.argmax()] < 30 else -series2[series1.argmin()]*0.5
        result = combo_df[21:].apply(caltest, axis=1)
        print(result)
        sum = 1
        for obj in result:
            sum *= (1 + obj/100.0)
        print("sum=", sum)

        return
        Series().cumprod()
        Series().argmin

    @classmethod
    def KellyCriterion(self,ser):
        '''
        凯利公式
        '''
        # 计算正收益，就是胜率
        s_bool = ser > 0
        ser_count = ser.count()
        success_count = s_bool.sum()
        # 胜率p
        p = success_count/ser_count
        q = 1 - p
        sum = 0
        # Series().dropna
        sum_success = 1
        sum_failure = 1
        for obj in ser.dropna():
            if obj > 0:
                sum_success *= (1+obj/100)
            else:
                sum_failure *= (1+obj/100)
        success_rate = sum_success ** (1/success_count) - 1
        failure_rate = 1 - sum_failure ** (1/(ser_count-success_count))
        print("success_rate=",success_rate)
        print("failure_rate=",failure_rate)
        f = (p*success_rate - q*failure_rate)/(success_rate*failure_rate)
        return f
        # return sum/sum_bottom



# MyGrid.IndustryRotation()
# MyGrid.TrendStrategy()

# short
# success_rate= 0.05094742882477399
# failure_rate= 0.023801068299798667
# 12.557205571131346
# Length: 179, dtype: float64
# sum= 1.1684828325316776
            
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

