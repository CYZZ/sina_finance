# 我的策略，该模块用于测试每个策略的收益率
import matplotlib.pyplot as plt

from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
from pandas import DataFrame, Series, DatetimeIndex
import mplfinance as fin
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

grid_etf()
