
# post 翻译

import requests
import json
def getTransformData():
    # 指定请求的URL
    post_url = "https://fanyi.baidu.com/sug"
    word = input('enter a word:')
    data = {
        'kw': word
    }
    # UA伪装
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    response = requests.post(url=post_url,data=data,headers=headers)
    # 如果确认服务器返回的obj是json数据才能使用.json()
    dic_obj = response.json()
    # print(dic_obj)
    # 持久化数据存储
    fp = open('./unused/'+ word+ '.json','w',encoding='utf-8')
    json.dump(dic_obj,fp=fp,ensure_ascii=False)

getTransformData()