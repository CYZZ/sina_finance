#! /usr/local/bin/python3
# -*- coding:utf-8 -*-
# 请求图片数据

from email import header
import re
from urllib import response
import requests

from bs4 import BeautifulSoup

def getImage():
    url = 'https://img9.doubanio.com/view/photo/l_ratio_poster/public/p2652621399.jpg'
    
    img_data = requests.get(url=url).content
    with open('./unused/aifei.jpg', 'wb') as fp:
        fp.write(img_data)

# getImage()

def regular_weibo_image():
    # 摄影主题的微博链接
    url = 'https://weibo.com/newlogin?tabtype=weibo&gid=1028034988&url=https%3A%2F%2Fweibo.com%2F'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    page_text = requests.get(url=url, headers=headers).text
    # print(page_text)
    # with open('./unused/weibo.html', 'wb') as fp:
    #     fp.write(page_text)
    # 使用聚焦爬虫进行数据解析
    ex = '<img src="(.*?)" class="woo-picture-img">'
    img_src_list = re.findall(ex,page_text,re.S)
    print(img_src_list)
   
# regular_weibo_image()


def testBeatifulSoup():
    fp = open()
    soup = BeautifulSoup(fp,'lxml')
    # soup.a 查找第一个a标签
    # soup.div 查找第一个div标签
    # soup.find('div') 等同于soup.div
    # soup.findAll('div',class_ = 'img') 查找所有符合条件的数据
    # soup.select('.tang > lu > li > a') 查找层级 > 表示一个层级 关系
    # soup.select('.tang > lu a) 空格表示多个层级

def getSanGuoYanyi():
    '''
    通过BeautifulSoup进行数据解析
    '''
    host = 'https://www.shicimingju.com'
    url = host + '/book/sanguoyanyi.html'
    # url = 'https://touduyu.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'
    }
    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    li_list = soup.select('.book-mulu > ul > li')
    fp = open('./unused/sanguo.txt','w',encoding='utf-8')
    for li in li_list:
        title = li.a.string
        detail_url = host + li.a['href']
        # 对详情页发起请求，解析出章节内容
        detail_response = requests.get(url=detail_url,headers=headers)
        detail_response.encoding = detail_response.apparent_encoding
        # 解析出详情内容
        detail_soup = BeautifulSoup(detail_response.text,'lxml')
        # detail_content = detail_soup.select('.chapter_content')[0]
        div_tag = detail_soup.find('div', class_='chapter_content')
        detail_content = div_tag.text

        fp.write(title + ':' + detail_content + '\n')
        print(title + '爬取成功')
# getSanGuoYanyi()

# xpath解析：最常用且最便捷高效的一种解析方式。通用性较高
