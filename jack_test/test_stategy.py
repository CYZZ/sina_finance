import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from Stategy.mygrid import MyGrid
from GUI.my_chart import MyChart
from eastmoney.fetchData.stock import eastStock

# MyGrid.get_rolling_rate()
# eastStock.test_save_local()
# eastStock.test_save_minute_local()
# MyGrid.TrendStrategy()
# MyGrid.XBXRotationStrategy()


if __name__ == '__main__':
    def start_test(params:list[str]):
        """
        通过传参决定调用哪个调试代码
        """
        if len(params) <= 1:
            print("please input param !!!!!")
            return
        # 只取其中一个
        params = params[1]
        if params == "1":
            print("MyGrid.XBXRotationStrategy()")
            # MyGrid.XBXRotationStrategy()
            MyGrid.XBXTestLocalFile()
            # MyGrid.XBXTestServiceData()
        elif params == "2":
            print("start call eastStock.test_save_local()")
            MyGrid.XBXTestServiceData()
        elif params == "3":
            print("start get_rolling_rate")
            MyGrid.get_rolling_rate()
        elif params == '4':
            print("MyGrid.TrendStrategy()")
            MyGrid.TrendStrategy()
        elif params == '5':
            print("show chart")
            MyChart.showChart()
        else:
            print("test---=== non")
    start_test(sys.argv)

from pandas import *
def testSaveJson():
    with open('/Users/yuze.chi/Desktop/jy_test/PythonDataScience/2022-04-12_page_info_log.txt') as file:
        index = 0
        urls = []
        page_info_responses = []
        fetch_results = []
        for item in file:
            if item.startswith('current testurl ='):
                urls.append(item.replace('current testurl = ',''))
            elif item.startswith('page info===----'):
                page_info_responses.append(item.replace('page info===----',''))
            elif item.startswith('pageInfo->dic====---'):
                if item.startswith('pageInfo->dic====---[:]'):
                    fetch_results.append('')
                else:
                    fetch_results.append('success')
        print("urls.len",len(urls))
        print("response.len",len(page_info_responses))
        print("result.len",len(fetch_results))
        df1 = DataFrame({  
        "urls":urls,   
        "response":page_info_responses,
        "is success":fetch_results
        })

        def search_success(x):
            if x["is success"] == 'success':
                return x

        # new_df = df1.apply(search_success,axis=1)
        new_df = df1[df1["is success"] == 'success']
        # new_df.to_csv('./page_info_fetch_result_success.csv')
        new_df.to_json('./page_info_fetch_result_success.json',orient='index')
        print(new_df.count())

        # df1.to_csv('./page_info_fetch_result.csv')

import akshare as ak
def testAkShare():
    stock_sse_summary_df = ak.stock_zh_a_hist_min_em(period='60')
    print(stock_sse_summary_df)


# testAkShare()

# import os
# def get_files():
#     for filepath,direname,filenames in os.walk('/Users/yuze.chi/Desktop/jy_test/PythonDataScience/sina_finance/unused'):
#         for filename in filenames:
#             realpath = os.path.join(filepath,filename)
#             if "月K" in realpath:
#                 os.remove(realpath)
#                 print(os.path.join(filepath,filename))
# get_files()
