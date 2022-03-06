from lxml import etree
import requests
def testEtree():
    # 爬取到页面源码数据
    # 获取58同城的二手房信息，
    url = 'https://bj.58.com/ershoufang/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    response = requests.get(url=url,headers=headers)
    page_text = response.text
    # 数据解析
    tree: etree = etree.HTML(page_text)
    # tree.xpath
    house_div_list = tree.xpath('body/div[@id="__nuxt"]/div[@id="__layout"]/div[@class="list"]/section[@class="list-body"]/section[@class="list-main"]/section[@class="list-left"]/section[2]/div')
    fp = open('./unused/58.txt','w',encoding='utf-8')
    for div in house_div_list:
        title = div.xpath('./a/div[@class="property-content"]/div[@class="property-content-detail"]/div[@class="property-content-title"]/h3/text()')[0]
        fp.write(title + '\n')
        print(title)
    # print(page_text)

testEtree()

'''
xpath中的/表示的是根层级
// 表示多个层级，跳跃了一个层级
//div[@class="song"] 表示的是属性定位，该例子是指的class为song的div标签
索引定位：  //div[@class="song"]/p[3] 索引的定位是从1开始的，不是0
取文本：div/text(),可以拿到对应的文本数据
'''