import sys
from pathlib import Path
from datetime import datetime
from datetime import date
from pandas import *
import pandas as np
import clipboard

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from plot_test.jukuang_test import *
from eastmoney.fetchData.stock import eastStock

codes = ["1.601012", "0.000776", "0.300750"]

obj = eastStock.request_ulist_stocks(codes)

out_str = "每日统计：\n"
ninde_highest = 692
ninde_close = obj[2]
ninde_str = "  跌的跟狗一样只值350乌云盖顶新能源宁德时代距历史最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
ninde_str = ninde_str.format(high=ninde_highest, close=ninde_close,
                             rate=(ninde_highest - ninde_close) / ninde_highest * 100)

longji_highest = 73.6
longji_close = obj[0]
longji_str = "  严重破位快逃命隆基股份距历史最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
longji_str = longji_str.format(high=longji_highest, close=longji_close,
                               rate=(longji_highest - longji_close) / longji_highest * 100)

guangfa_highest = 26.72
guangfa_close = obj[1]
guangfa_str = "  广● 横盘代替下跌●铁底跌无可跌●券商蛇王●足足七年没有行情●北交所圣经之子●全面注册制大利好●庄家跟杰克做对手盘●发证券距去年最高点回撤：({high:.2f}-{close:.2f})/{high:.2f}={rate:.2f}%\n"
guangfa_str = guangfa_str.format(high=guangfa_highest, close=guangfa_close,
                                 rate=(guangfa_highest - guangfa_close) / guangfa_highest * 100)
end_str = "  待广发超越宁隆十个点两个月后便不再统计。\n  (请●所有券商人起立，在评论区集合，二十万粉丝联名杰克清仓剩下持仓！)\n"
clipboard.copy(out_str + ninde_str + longji_str + guangfa_str + end_str)
print(clipboard.paste())


# 每日统计：
#        跌的跟狗一样只值350乌云盖顶新能源宁德时代距历史最高点回撤：（692-493.55）/692=28.67%
#        严重破位快逃命隆基股份距历史最高点回撤：（103.3-80.51）/103.3=22.06%
#       广● 横盘代替下跌●铁底跌无可跌●券商蛇王●足足七年没有行情●北交所圣经之子●全面注册制大利好●庄家跟杰克做对手盘●发证券距去年最高点回撤：（27.22-17.14）/27.22=37.03%
#      待广发超越宁隆十个点两个月后便不再统计。
#   （请●所有券商人起立，在评论区集合，二十万粉丝联名杰克清仓剩下持仓！
