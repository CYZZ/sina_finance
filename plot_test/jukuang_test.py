from jqdatasdk import *
import jqdatasdk as jq
from jqdatasdk.utils import Security
from pandas import DataFrame, Series
import pandas as pd
import json

# print(get_query_count())
# df = get_ticks('000001.XSHE', start_dt='2021-01-01', end_dt='2021-12-31')
# df = stock
# print(df)
# info: Security = get_security_info('000001.XSHE')
# print(info.start_date)
# print(info.name)
# print(info.end_date)
# print(info.code)
# info.display_name
# aier = get_price('300015.XSHE', end_date='2021-12-31', count=5)
# print(aier)


def auth_jukuang():
    """
    登录聚宽平台,通过读取json文件，获取账号和密码
    """
    # Opening JSON file
    f = open('account.json')
    # read JSON object
    data = json.load(f)
    f.close()
    auth(data['account'], data['password'])


def load_data_from_jukuang_service():
    """
    从聚宽平台获取数据，并存储到指定的文件中
    :return:
    """
    auth_jukuang()
    # 获取etf的数据
    fields = ['open', 'close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit', 'low_limit', 'avg',
              'pre_close',
              'paused']
    df_ETF: DataFrame = get_price('513100.XSHG', start_date='2017-01-01', end_date='2022-01-01', fields=fields,
                                  panel=False)
    path = "513100_纳指ETF.csv"
    df_ETF.to_csv(path)

# load_data_from_jukuang_service()


def read_data_from_local(path: str) -> DataFrame:
    """
    从本地的csv文件读取数据
    :param path: 文件路径
    :return: 获取数据之后转换层DataFrame 表头为 ['Date', 'Open', 'Close', 'Low', 'High', 'Volume']
    """
    etf: DataFrame = pd.read_csv(path, parse_dates=['Unnamed: 0'])
    # etf = etf[['Unnamed: 0', 'open', 'close', 'low', 'high', 'volume']]
    etf = etf.iloc[:, 0:6]
    etf.columns = ['Date', 'Open', 'Close', 'Low', 'High', 'Volume']
    etf.set_index('Date', inplace=True)
    return etf


def test_fundamentals():
    '''
    测试聚宽的接口
    :return:
    '''
    auth_jukuang()
    # 获取聚宽的财务数据,选出所有的总市值大于1000亿元，市盈率小于10，营业收入大于200亿元的股票
    df = get_fundamentals(
        query(valuation.code, valuation.market_cap, valuation.pe_ratio, income.total_operating_revenue).filter(
            valuation.market_cap > 1000,
            valuation.pe_ratio < 10,
            income.total_operating_revenue > 2e10
        ), date='2022-01-15')
    print(df)
    


# test_fundamentals()
# auth_jukuang()
# # jq.get_query_count
# print(get_query_count())
# 交易市场	代码后缀	示例代码	证券简称
# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行
# 中金所	.CCFX	IC9999.CCFX	中证500主力合约
# 大商所	.XDCE	A9999.XDCE	豆一主力合约
# 上期所	.XSGE	AU9999.XSGE	黄金主力合约
# 郑商所	.XZCE	CY8888.XZCE	棉纱期货指数
# 上海国际能源期货交易所	.XINE	SC9999.XINE	原油主力合约
# 场外基金	.OF	398051.OF	中海环保新能源混合
