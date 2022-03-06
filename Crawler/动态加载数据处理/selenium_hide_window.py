# 无可视化的浏览器
from time import sleep
from selenium.webdriver.edge.webdriver import WebDriver
from lxml import etree
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# 实现无可视化界面的操作
# 配置成无头无界面的浏览器
edge_options = Options()
edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')

# 以下代码添加之后，可以防止 被检测出来
edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])
edge_options.add_experimental_option('useAutomationExtension', False)

# 有的门户网站会检测到是selenium，会有反爬技术

# 实例化一个浏览器对象（传入浏览器驱动程序）
bro = WebDriver(executable_path='./unused/edgedriver_mac64/msedgedriver',options=edge_options)



# 无可视化界面
bro.get('https://www.baidu.com')
# print(bro.page_source)

sleep(3)

bro.quit()