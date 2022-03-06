
import requests

def getShougouData():
    url = 'https://www.sogou.com/'
    response = requests.get(url=url)
    # 获取页面的字符串数据
    page_txt = response.text
    print(page_txt)

    with open('./sougou.html','w',encoding='utf-8') as fp:
        fp.write(page_txt)
getShougouData()