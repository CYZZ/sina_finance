
import requests
import json
# url：http://scxk.nmpa.gov.cn:81/xk/

def getNmpaData():
    '''
    获取网页的html数据
    '''
    url = 'http://scxk.nmpa.gov.cn:81/xk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }

    page_text = requests.get(url=url,headers=headers).text
    # 抓取网页数据存储到指定的文件中。
    with open('./unused/huazhuangping.html','w',encoding='utf-8') as fp:
        fp.write(page_text)

# getNmpaData()

def getNmpaJsonData():
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    body = {
        'on': True,
        'page': 1,
        'pageSize': 15,
        'productName': '',
        'conditionType': 1,
        'applyname': '',
        'applysn': ''
    }
    response = requests.post(url=url,headers=headers,data=body)
    # print(response.json())
    with open('./unused/huazhuangping.json','w',encoding='utf-8') as fp:
        json.dump(obj=response.json(),fp=fp,ensure_ascii=False)
        # fp.write(page_text)
    # pass
getNmpaJsonData()

def getNmpaDetail(id:str):
    pass
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portal/dzpz.jsp?id=a6674298a4ac474ba76a7bccbe0ebad5'