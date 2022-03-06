# from selenium import webdriver
from time import sleep
from selenium.webdriver.edge.webdriver import WebDriver
from lxml import etree
# edgewebdrive
# webdriver.WebDriver.e

# 实例化一个浏览器对象（传入浏览器驱动程序）
# bro = webdriver.edge(executable_path='./unused/edgedriver_mac64/msedgedriver')
bro = WebDriver(executable_path='./unused/edgedriver_mac64/msedgedriver')

bro.get('https://www.taobao.com/')

# page_text = bro.page_source
# tree = etree.HTML(page_text)
# 获取搜索框，定位到标签
search_input = bro.find_element_by_id('q')
# 标签交互
search_input.send_keys('iphone')

# 开始执行js代码
bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')

# search_button = bro.find_element_by_class_name('')
btn = bro.find_element_by_css_selector('.btn-search')

sleep(2)

# 点击搜索按钮
btn.click()

bro.get('https://www.baidu.com')
sleep(2)
# 返回上一页
bro.back()
sleep(2)
# 重新跳转下一个页面
bro.forward()

# first_company = tree.xpath('body/div[@')
# print(page_text)
sleep(5)
bro.quit()