from lxml import etree
import requests


def getCities():
    '''
    获取城市列表数据
    '''
    url = 'http://www.aqistudy.cn/historydata/'
    headers = headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }

    response = requests.get(url,headers=headers)
    tree = etree.HTML(response.text)
    ul_list = tree.xpath('body/div[@class="container"]/div[@class="row"]/div[1]/div[@class="all"]/div[@class="bottom"]/ul[@class="unstyled"]')
    fp = open('./unused/cities.txt','w',encoding='utf-8')
    for ul in ul_list:
        index_name = ul.xpath('./div[1]/b/text()')[0]
        fp.write(index_name + '\n')
        city_name_li_list = ul.xpath('./div[2]/li')
        for li in city_name_li_list:
            city_name = li.xpath('./a/text()')[0]
            fp.write(city_name + ' ')
        fp.write('\n')
        # print(index_name)
    # print(ul_list)
getCities()
