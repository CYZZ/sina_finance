# 异步线程给方式进行数据的爬取。

# 高性能异步爬虫
#

import time
# 导入线程池对应的类
from multiprocessing.dummy import Pool
import requests
from lxml import etree
import random
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
}

video_urls = []

def get_LIVideos():
    # 对这个链接进行请求并解析出详情页的链接。
    host = 'https://www.pearvideo.com/'
    url = host + 'category_5'
    response = requests.get(url=url,headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('body/div[@class="category-main cmmain"]/div[@class="category-top"]/div/ul/li[@class="categoryem "]')
    
    for li in li_list:
        name = li.xpath('./div[@class="vervideo-bd"]/a/div[@class="vervideo-title"]/text()')[0]
        href = li.xpath('./div[@class="vervideo-bd"]/a/@href')[0]
        video_id = href.split('_')[1]
        json_url = host + 'videoStatus.jsp'
        body = {
            'contId': video_id,
            'mrd': random.random()
        }
        jsp_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
            'Referer': host + href
            # 'Referer': 'https://www.pearvideo.com/video_1752818'
        }
        response = requests.get(url=json_url,headers=jsp_headers,params=body)
        video_json = response.json()
        systemTime = video_json['systemTime']
        srcUrl = video_json['videoInfo']['videos']['srcUrl']
        srcUrl = srcUrl.replace(systemTime, "cont-"+video_id)
        # video_response = requests.get(srcUrl,headers=headers)
        # print(srcUrl,"正在下载")
        # with open('./unused/'+name+'.mp4','wb') as fp:
        #     fp.write(video_response.content)
        # print(name)
        dic = {
            'name':name,
            'url':srcUrl
        }
        video_urls.append(dic)

def downloadVideo(dic):
    url = dic['url']
    name = dic['name']
    print(url,"正在下载")
    data = requests.get(url=url,headers=headers).content
    with open('./unused/'+name+'.mp4','wb') as fp:
        fp.write(data)

# 使用线程池的方式进行数据的下载
def downLoadWithPool():
    # 先获取视频url
    get_LIVideos()
    # 使用线程池进行数据加载
    pool = Pool(4)
    pool.map(downloadVideo,video_urls)
    pool.close()
    pool.join()

from Async_my_network import MyNetwork
startime = time.time()
def getResponseFromMyNetwork(data,name):
    print('下载视频完成：',name)
    with open('./unused/'+name+'.mp4','wb') as fp:
        fp.write(data)
    endTime = time.time()
    print('总耗时',endTime - startime)
def downloadWithAsync():
    '''
    使用自定义的异步线程网络进行请求
    '''
    # 先获取视频url
    get_LIVideos()
    
    for dic in video_urls:
        name = dic['name']
        url = dic['url']

        print('开始下载视频：',name)
        MyNetwork.asyncRequest(url=url,callBack=getResponseFromMyNetwork,other=name,type='data')
    # MyNetwork.startDownload()

downloadWithAsync()




def test_loadVideo():
    testurl = 'https://www.pearvideo.com/videoStatus.jsp'
    body = {
        'contId':'1752818',
        'mrd': random.random()
    }
    myHeaders = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
        'Referer': 'https://www.pearvideo.com/video_1752818'
    }
    response = requests.get(url=testurl,headers=myHeaders,params=body)
    print(response.request.url)
    print(response.json())
    # https://video.pearvideo.com/mp4/third/20220225/cont-1752818-13498179-170840-hd.mp4
    # https://video.pearvideo.com/mp4/third/20220225/1645950104307-13498179-170840-hd.mp4
# test_loadVideo()
# random.random()
# print(random.random())
# 0.3247941219257138

# ************ 分割线 ************************************************************

def get_page(url: str):
    print("正在下载：", url)
    time.sleep(2)  # 模拟线程阻塞2s
    print('下载成功：', url)


name_list = ['xiaozi', '华为', '荣耀', 'Apple']


def test_Sync():
    print("开始模拟同步的线程操作")

    start_time = time.time()
    # 模拟同步操作，只有一个线程
    for url in name_list:
        get_page(url)
    end_time = time.time()

    print('%d second' % (end_time - start_time))
# test_Sync()


def test_Async():
    # 通过创建线程池的方式进行数据的多线程加载
    start_time = time.time()
    pool: Pool = Pool(4)
    # 将列表中的每一个元素传递给函数，当做参数

    pool.map(get_page, name_list)
    end_time = time.time()
    print('%d second' % (end_time - start_time))
# test_Async()
