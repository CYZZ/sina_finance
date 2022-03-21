from mimetypes import init
import sys 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("加载本地网页")
        self.setGeometry(70, 70, 555, 330)  # 设置窗口大小
        self.browser = QWebEngineView()
        # 记载本地的文件要使用file:///User/page.html
        # 相对路径 ./page.html
        self.browser.load(QUrl('file:///Users/cyz/Desktop/PythonTest/sina_finance/render.html'))
        # self.browser.load(QUrl("https://www.baidu.com"))
        self.setCentralWidget(self.browser)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())
        