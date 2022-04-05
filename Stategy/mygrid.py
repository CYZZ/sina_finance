# 我的策略，该模块用于测试每个策略的收益率
from cProfile import label
import matplotlib.pyplot as plt

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
from pandas import DataFrame, Series, DatetimeIndex
from plot_test import jukuang_test


def grid_etf():
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

# grid_etf()

def RotationStrategy():
    '''
    轮动策略，测试每个月轮动一次
    '''
    # 从文件中读取数据
    zhongxin_df = pd.read_csv("unused/601012_隆基股份后复权月K.csv",index_col=1)
    dongcai_df = pd.read_csv("unused/600438_通威股份后复权月K.csv",index_col=0)

    # zhongxin_df.set_index('date',inplace=True)
    dongcai_df.set_index('date',inplace=True)
    print(zhongxin_df.head())
    print(dongcai_df.head())
    # print(zhongxin_df.loc['2003-01-29'])
    # print(zhongxin_df.index.tolist())

    dongcai_indexs = dongcai_df.index.tolist()
    zhongxin_index = zhongxin_df.index.tolist()
    test_indexs = dongcai_indexs[-43:]

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




RotationStrategy()
# python3 Stategy/mygrid.py