# from selenium import webdriver
from time import sleep
from numpy import ediff1d
from selenium.webdriver.edge.webdriver import WebDriver
from lxml import etree
# from selenium.webdriver.edge.webdriver import action
# formatter
from selenium.webdriver.common.action_chains import ActionChains


# 实例化一个浏览器对象（传入浏览器驱动程序）
bro = WebDriver(executable_path='./unused/edgedriver_mac64/msedgedriver')

bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

#  如果定位的标签是存在于iframe标签之中的则必须通过如如下操作才能进行标签定位
bro.switch_to.frame('iframeResult') # 切换到指定的iframe
div = bro.find_element_by_id('draggable')



# 开始拖拽标签，点击长按然后滑动
# 动作链
action = ActionChains(bro)
# 点击长按指定的标签
action.click_and_hold(div)
for i in range(5):
    # 立即执行动作链操作
    # 有两个参数，水平和竖直
    action.move_by_offset(17,0).perform()
    sleep(0.3)
action.release()


bro.quit()

# print(div)

# https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable