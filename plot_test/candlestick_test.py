import matplotlib.pyplot as plt

from eastmoney.kline.kline_test import get_data
from matplotlib.dates import date2num
import pandas as pd
from pandas import DataFrame, Series, DatetimeIndex
import mplfinance as fin
import jukuang_test

# parse_dates 是把指定的列设置为日期格式
etf: DataFrame = jukuang_test.read_data_from_local('../../jukuang_data/513050_中概无互联网.csv')
print(etf)

'''
print(etf.resample("M").all())
df_monthly: DataFrame = etf.resample("M").first()
df_yearly: DataFrame = etf.resample("A").last()
# print(df_monthly)
# print(df_yearly)

const_money = 0
hold = 0
for year in range(2017, 2021):
    cost_money = df_monthly.loc[str(year)]["Open"].sum() * 100
    print('cost_money=', cost_money)
    hold += len(df_monthly.loc[str(year)]) * 100
    sell_money = df_yearly.loc[str(year)]['Close'][0] * hold
    cost_money -= sell_money
    hold = 0
print("cost_money=", cost_money)
'''

etf['ma5'] = etf["Open"].rolling(1).mean()
etf['ma30'] = etf["Open"].rolling(2).mean()

# print(etf[0:100])

# etf[['Close', 'ma5', 'ma30']][-100:].plot()  # 绘制最后100日的图
# plt.show()

etf = etf.dropna()
# etf = etf[-200:]

'''
golden_cross = []
death_cross = []
for i in range(len(etf)):
    if etf['ma5'][i] >= etf['ma30'][i] and etf['ma5'][i-1] < etf['ma30'][i-1]:
        golden_cross.append(etf.index[i])
    elif etf['ma5'][i] <= etf['ma30'][i] and etf['ma5'][i-1] > etf['ma30'][i-1]:
        death_cross.append(etf.index[i])

print("golden=",golden_cross)
print("death",death_cross)
'''
'''
策略模型，通过位移的方式进行筛选交叉点
TTTTTFFFFFTTTTT
 FFFFFTTTTTFFFFF
'''
sr1 = etf['ma5'] < etf['ma30']
sr2 = etf['ma5'] >= etf['ma30']
death_cross = etf[sr1 & sr2.shift(1)].index
gold_cross = etf[-(sr1 | sr2.shift(1))].index
print("death_cross=", death_cross)
print("gold_cross=", gold_cross)

first_money = 100000
money = first_money
hold = 0
df1 = pd.Series(1, index=gold_cross)
df2 = pd.Series(0, index=death_cross)
df = df1.append(df2).sort_index()
print(df)
offset_price = 0.00
tack_series = pd.Series([money], index=[df1.index[0]])
for i in range(0, len(df)):
    index = df.index[i]
    p = etf['Open'][index]
    if df.iloc[i] == 0:
        # 金叉
        p1 = etf['Low'][index] + offset_price
        if p1 < p:
            p -= offset_price
            buy = (money // (100 * p))
            hold += buy * 100
            print("买入日期=", df.index[i])
            print("买入前剩余本金=", money)
            money -= buy * 100 * (p - 0.0)
    else:
        p2 = etf['High'][index] - offset_price
        if p2 > p:
            p += offset_price
            money += hold * p
            hold = 0

            tack_series.loc[df.index[i]] = money
            print("卖出日期=", df.index[i])
            print("卖出后剩余本金=", money)
p = etf['Open'][-1]
now_money = hold * p + money
tack_series.loc[etf.index[-1]] = now_money

print(now_money - first_money)
print("策略收益率=", (now_money - first_money) / first_money)
print("首次买入时间和价格=", df1.index[0], etf['Open'][df1.index][0])
print("最后卖出时间和价格=", df2.index[-1], etf['Open'][df2.index][-1])
print("持有不动收益率=", etf['Open'][df2.index[-1]] / etf['Open'][df1.index[0]] - 1)

plt.plot(etf['Open'] / etf['Open'][0] * 100000, label="123")
# (etf['ma30']/etf['Open'][0]*100000).plot()
plt.plot(tack_series, label='abc')
plt.legend(loc='best')
plt.show()
