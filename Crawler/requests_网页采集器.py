from email import header
from fileinput import filename
import requests
# 搜索测试


def testSearch():

    headers = {
        # https://www.sogou.com/web?query=%E6%B5%8B%E8%AF%95
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }

    url = "https://www.sogou.com/web"
    kw = input('enter a word:')
    param = {
        'query': kw
    }
    response = requests.get(url=url, params=param,headers=headers)
    page_txt = response.text
    fileName = './unused/'+ kw + '.html'
    with open(fileName, 'w',encoding='utf-8') as fp:
        fp.write(page_txt)
    print(fileName, "保存成功！！")

testSearch()
# 网页有UA检测，所以爬虫需要进行UA伪装，伪装成某一款浏览器。
    