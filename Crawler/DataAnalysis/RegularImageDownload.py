# 图片下载
import requests
from lxml import etree

def getPic():
    host = 'https://pic.netbian.com'
    url = host + '/4kmeinv/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    response = requests.get(url=url,headers=headers)
    # 使用网页原始的编码方式
    print('原始编码' + response.apparent_encoding)
    response.encoding = response.apparent_encoding
    page_text = response.text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('body/div[@class="wrap clearfix"]/div[@id="main"]/div[@class="slist"]/ul/li')
    # li_list = tree.xpath('body/div[@class="wrap clearfix"]/div[@id="main"]/div[@class="slist"]/lu')
    print(li_list)
    # return
    for li in li_list:
        img_src = host + li.xpath('./a/img/@src')[0]
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        # print(img_src)
        print(img_name + "加载")
        # 请求图片
        img_data = requests.get(img_src,headers=headers).content
        with open('./unused/meinv/'+img_name,'wb') as fp:
            fp.write(img_data)
getPic()