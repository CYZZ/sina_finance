import tushare as ts
import jqdatasdk
from pandas import DataFrame, Series

# ts.set_token('ab80ac349baf1b58f4ed5eb9acd8730ad7bcbe96dacec44af087d918')
# pro = ts.pro_api()
# data = pro.stock_basic()
# print(data)

df = DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print(df.shift(1))
