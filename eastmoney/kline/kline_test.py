import json
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import xlwt
import sqlite3
import re


def get_data(code="000001"):
    # url = "http://62.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery33103422893090882453_1641114428433&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt=120&_=1641114428436"
    url = "http://62.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery33103422893090882453_1641114428433&secid=1." + code + "&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt=120&_=1641114428436"
    data = request_data(url)
    splits, name, _ = convert_data_to_json(data, pre="jQuery33103422893090882453_1641114428433\(")
    print("name====",name)
    return splits, name


def convert_data_to_json(data: str, pre=""):
    print("start convert data----====")
    regular = r'%s(.*?)\)'%pre
    # find_json = re.compile(r'jQuery33103422893090882453_1641114428433\((.*?)\)')
    find_json = re.compile(regular)
    json_str = re.findall(find_json, data)[0]
    dic = json.loads(json_str)
    klines = dic["data"]["klines"]
    splits = []
    for obj in klines:
        kline = obj.split(",")
        # my_split = kline[:6]
        my_split = kline[:3]
        my_split.append(kline[4])
        my_split.append(kline[3])
        my_split.append(kline[5])
        splits.append(my_split)
    print(len(splits))
    # print(splits)
    name = dic["data"]["name"]
    print("====-=-=-=89898989")
    return splits, name, klines


def request_data(url: str):
    head = {
        "User-Agent": "Mozilla/5.0(Macintosh; Intel Mac OSX 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 96.0.4664.110 Safari / 537.36 Edg / 96.0.1054.62"
    }
    request = urllib.request.Request(url, headers=head)
    data = ""
    try:
        response = urllib.request.urlopen(request)
        data = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(e)
    return data

