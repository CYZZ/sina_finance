from decimal import Decimal
from typing import List
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from pandas import *
from Stategy.mygrid import MyGrid
from eastmoney.fetchData.stock import eastStock
import json
import datetime
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

class MyDayChart(QWidget):
    # 分割器
    def __init__(self,parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.mainSplitter = QSplitter(self)
        self.layout.addWidget(self.mainSplitter)
        self.setLayout(self.layout)
        # 水平线分割
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)

        rightSplitter = QSplitter(self)
        # 垂直分割
        rightSplitter.setOrientation(Qt.Orientation.Vertical)
        self.textEdit = QTextEdit()
        self.textEdit.setText("Window2")
        rightSplitter.addWidget(self.textEdit)
        self.myHtml = QWebEngineView()
        # 要使用绝对地址访问文件
        self.myHtml.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,False)
        self.myHtml.load(QUrl("http://localhost:8989/my_linkpage.html"))
        # QWebEngineSettings.setAttribute
        self.myHtml.settings().resetAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled)
        self.myHtml.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,True)
        self.myHtml.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled,False)
        rightSplitter.addWidget(self.myHtml)
        rightSplitter.setStretchFactor(0,1)
        rightSplitter.setStretchFactor(1,8)
        
        vLayout = QVBoxLayout()
        login_button = QPushButton("登录")
        login_button.clicked.connect(self.login)


        listWidge = MyListwidge()
        
        items = update_history_data()
        # items =  ['159949-0', '300487-0', '513050-1', '600958-1', '000999-0']
        listWidge.addItems(items)
        listWidge.clicked.connect(self.click_list_widge)
        self.listWidge = listWidge

        update_button = QPushButton("保存数据")
        update_button.clicked.connect(self.update_date)

        self.stock_edit = QLineEdit()
        self.stock_edit.setPlaceholderText("请输入关键字搜索")
        self.stock_edit.returnPressed.connect(self.startSearch)
        
        vLayout.addWidget(login_button)
        # vLayout.addLayout(form_layout)
        # vLayout.addWidget(listView)
        vLayout.addWidget(listWidge)
        vLayout.addWidget(update_button)
        vLayout.addWidget(self.stock_edit)

        vLayout.addStretch()
        widge = QWidget()
        widge.setLayout(vLayout)

        self.mainSplitter.addWidget(widge)
        self.mainSplitter.addWidget(rightSplitter)

        # 分割比例
        self.mainSplitter.setStretchFactor(0,1)
        self.mainSplitter.setStretchFactor(1,2)

        self.setWindowTitle("Splitter")
        self.setLayout(self.layout)
    
    def clicked_list(self, qmodelIndex):
        print("已经点击了list==",qmodelIndex)

    def click_list_widge(self, params: QModelIndex):
        print(params.column())
        print(params.row())
        item = self.listWidge.itemFromIndex(params)
        print("item.text",item.text())
    
    def start_drag_listWidge(self):
        print("开始拖拽了")
    
    def login(self):
        from GUI.my_chart import myQThread
        mylist = [obj.text() for obj in self.listWidge.selectedItems()]
        print(mylist)
        # 在子线程刷新数据，回到主线程刷新UI
        if type(self.thread) == myQThread:
            print("11-已经初始化thead")
        else:
            print("22-开始初始化thread")
            self.thread = myQThread(self.target_func,"test11")
            self.thread.mySignal.connect(self.login_comple)
        self.thread.start()
    
    def target_func(self,param):
        self.listWidge.selectedItems()
        myDic = {
            "status": "success",
            "data": [
                
            ]
        }
        for obj in self.listWidge.selectedItems()[-4:]:
            params = obj.text()
            name, x, y, prePrice, min, max = fetch_data(params)
            data = {
                "name": name,
                "x": get_one_day_x_data(),
                "y": y,
                "prePrice": prePrice,
                "min": min,
                "max": max
            }
            myDic["data"].append(data)
        json_str = json.dumps(myDic, ensure_ascii=False)
        with open('./MyHTMLChart/json/test.json','w') as json_file:
            json_file.write(json_str)
        
        
    def login_comple(self):
        print("请求结束")
        self.myHtml.page().runJavaScript('my_reloadData();', self.js_callback)

    def js_callback(self,result):
        print(result)

    def update_date(self):
        items = [self.listWidge.item(idx).text() for idx in range(self.listWidge.count())]
        update_history_data(items)

    def startSearch(self):
        text = self.stock_edit.text()
        result =eastStock.get_stock_info(text)
        self.textEdit.setText(str(result))


class MyListwidge(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        # 设置之后拖拽不会有赋值的情况，只会移动
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # 右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.custom_right_menu)
    
    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        print("已经停止了拖拽==",self.items(event.mimeData()))
        print(self.model().children())
        return super().dropEvent(event)
    
    def selectionChanged(self, selected: QtCore.QItemSelection, deselected: QtCore.QItemSelection) -> None:
        print("已经选中了改变")
        # print("selected=",selected.)
        return super().selectionChanged(selected, deselected)
    
    def custom_right_menu(self, pos: QPoint):
        menu = QtWidgets.QMenu()
        menu_items = ["新增","删除","排序","清空"]
        [menu.addAction(text) for text in menu_items]

        action = menu.exec_(self.mapToGlobal(pos))
        if action is None:
            print("action==None")
            text = None
        else:
            text = action.text()
        if text == "新增":
            mytext, ok = QInputDialog.getText(self, '新增代码',"请输入代码:")
            if ok and mytext:
                self.addItem(mytext)
        elif text == "删除":
            print("点击了删除")
            for idx in [self.indexFromItem(obj).row() for obj in self.selectedItems()]:
                self.takeItem(idx)
        elif text == "排序":
            print("开始排序")
        elif text == "清空":
            print("清空")
            self.clear()
    
def fetch_data(params:str):
    arr = params.split("-")
    code = arr[0]
    ctype = arr[1]
    name, df, prePrice = eastStock.request_day_trends(code, ctype)
    df.set_index('date', inplace=True)
    x = df.index.tolist()
    close = df['close']
    y = close.tolist()
    max_price = close.max()
    min_price = close.min()
    delt = max(abs(prePrice-max_price), abs(prePrice-min_price))
    top_price = prePrice + delt
    bottom_price = prePrice - delt

    print("max_price==",max_price)
    print("min_price==",min_price)
    print("delt==",delt)
    print("prePrice==",prePrice)
    top_price = Decimal(top_price).quantize(Decimal('.00'), rounding=ROUND_CEILING)
    bottom_price = Decimal(bottom_price).quantize(Decimal('.00'), rounding=ROUND_FLOOR)
    return name, x, y, prePrice, float(bottom_price), float(top_price)


def update_history_data(items: List=None):
    if items is None:
        try:
            with open('./MyHTMLChart/json/fetch_history.json', 'r') as json_file:
                json_data = json.load(json_file)
                return json_data["items"]
        except:
            return []
    else:
        myDic = {"items": items}
        json_str = json.dumps(myDic, ensure_ascii=False)
        with open('./MyHTMLChart/json/fetch_history.json', 'w') as json_file:
            json_file.write(json_str)

def get_one_day_x_data():
    start = '09:30'
    end = '11:30'
    datestart = datetime.datetime.strptime(start, '%H:%M')
    dateend = datetime.datetime.strptime(end,'%H:%M')

    data_list = list()

    while datestart <= dateend:
        data_list.append(datestart.strftime('%H:%M'))
        datestart+=datetime.timedelta(minutes=1)
    
    start = '13:01'
    end = '15:00'
    datestart = datetime.datetime.strptime(start, '%H:%M')
    dateend = datetime.datetime.strptime(end,'%H:%M')
    while datestart <= dateend:
        data_list.append(datestart.strftime('%H:%M'))
        datestart+=datetime.timedelta(minutes=1)
    return data_list