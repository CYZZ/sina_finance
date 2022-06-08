from select import kevent
from pandas import *
import pandas as pd
from typing import Dict, List
import json
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QUrl,Qt,QThread,pyqtSignal, QTimerEvent
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from pyecharts.charts import Line,Bar,Grid, Pie,Line3D
import datetime,time
import sys
import os


from pathlib import Path

from sqlalchemy import false
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import pyecharts.options as opts
from pyecharts import charts
from Stategy.mygrid import MyGrid

class MyChart(QWidget):
    def __init__(self):
        super(MyChart,self).__init__()
        self.initUI()
        self.mainLayout()

    def initUI(self):
        self.setGeometry(400, 400, 800, 600)
        self.setWindowTitle("demo1")

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        url = "https://www.baidu.com"
        # 要使用绝对地址访问文件
        self.myHtml.load(QUrl("file:///Users/yuze.chi/Desktop/jy_test/PythonDataScience/测试结果_沪深300ETF_创业板50ETF_service.html"))
        # 选择使用url打开网页
        # self.myHtml.load(QUrl(url))

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)
    
    @classmethod
    def line_base(self, x: List, fileName: str,retracement: DataFrame, trading_count: Dict, revenue_contribution: Dict, sum_rate: tuple[List,List],html_title="轮动策略", **y) -> Line:
        '''
        绘制折线图
        '''
        c = (
            Line()
            .add_xaxis(x)
            .set_global_opts(title_opts=opts.TitleOpts(title=html_title),
                             tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis', axis_pointer_type='cross'),
                             yaxis_opts=opts.AxisOpts(name="收益率"),
                             toolbox_opts=opts.ToolboxOpts(feature={'dataView': {'readOnly': False}, 'magicType': {'type': ['line', 'bar']}}),
                             axispointer_opts=opts.AxisPointerOpts(is_show=True, label=opts.LabelOpts(is_show=True, background_color='rgb(123,123,123,1)')),
                             datazoom_opts=[opts.DataZoomOpts(type_='inside', range_start=0, range_end=100, xaxis_index=[0,3]),
                             opts.DataZoomOpts(pos_bottom='50%', range_start=0, range_end=100, xaxis_index=[0,3]),
                             opts.DataZoomOpts(type_='inside', range_start=50, range_end=100, xaxis_index=1),
                             opts.DataZoomOpts(pos_bottom='0%', range_start=50, range_end=100, xaxis_index=1)],
                            #  visualmap_opts=opts.VisualMapOpts(pieces=[{"min": 2, "max": 3,'color':'green'},])
                             )
        )
        # c.width = "95%"
        # c.height = "800px"
        c.page_title = html_title
        # 遍历可变的数据，显示所有
        
        my_markpoint_data = []
        my_markarea_data = []
        for row in retracement.itertuples():
            begin_date = getattr(row, 'begin_date')
            begin_number =  getattr(row, 'begin_number')
            end_date = getattr(row, 'end_date')
            end_number = getattr(row, 'end_number')
            rate = getattr(row, 'retracement')
            my_markpoint_data.append(opts.MarkPointItem(name='test', coord=[begin_date, begin_number], value=begin_number))
            my_markpoint_data.append(opts.MarkPointItem(name='test', coord=[end_date, end_number], value=end_number))
            my_markarea_data.append(opts.MarkAreaItem(name=round(-rate*100, 2), x=(begin_date, end_date), y=(end_number, begin_number)))
            
        # 开始绘制折线
        for k, v in y.items():
            
            # color = line_colors.pop
            c.add_yaxis(k, v,label_opts=opts.LabelOpts(is_show=True,interval=10),
                        linestyle_opts=opts.LineStyleOpts(width=1.5),
                        xaxis_index=0,
                        yaxis_index=0
                        # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="test", x="2021-09-13", symbol_size=20), opts.MarkLineItem(name="test", x="2021-10-25", symbol_size=20)]),
                        # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(name='test', coord=["2021-10-25",3],value=2)])
                        )
        # 需要有数据之后设置的属性才能生效
        c.set_series_opts(markarea_opts=opts.MarkAreaOpts(itemstyle_opts=opts.ItemStyleOpts(color='rgba(20, 255, 20, 0.1)'),
                                                        #   data=[opts.MarkAreaItem(name='morning Peak', x=('2020-06-03', '2021-07-09'))]
                                                        data= my_markarea_data,
                                                        label_opts=opts.LabelOpts(color='black'),
                                                        is_silent=True
                                                          ),
                        #   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max', name='最大值'), opts.MarkPointItem(type_='min',name='最小值'), opts.MarkPointItem(name='test', value=3,x=30,y=3)])
                        # 设置显示的标签样式，
                        # label_opts=opts.LabelOpts(interval=100),
                        # tooltip_opts=opts.marklin
                          )
        # 用于计算年收益
        rate_df = DataFrame(y)
        rate_df["date"] = x
        rate_df.set_index('date')

        c1 = self.gender_bar(pos_top='75%',x=x,y=y)
        c2 = self.gender_pie(trading_count=trading_count)
        c3 = self.gender_contribution_bar(revenue_contribution=revenue_contribution,pos_top="70%",pos_left="66%")
        c4 = self.gender_sum_rate_line(x,sum_rate)
        # c.overlap(c1)
        grid = Grid(init_opts=opts.InitOpts(width="95%", height="1000px", page_title=html_title))

        c3.overlap(c2)
        
        grid.add(c, grid_opts=opts.GridOpts(pos_bottom="55%"))
        grid.add(c1, grid_opts=opts.GridOpts(pos_top="75%",pos_right="35%"))
        grid.add(c3,grid_opts=opts.GridOpts(pos_top="75%",pos_left="70%"))
        grid.add(c4, grid_opts=opts.GridOpts(pos_top="65%",pos_bottom="50%"))
        grid.render(fileName)
        # c.render(fileName)
        return c

    @classmethod
    def gender_bar(self, x: List, y:dict, pos_top='75%'):
        # 获取每年的最后一个交易日
        offset = pd.tseries.offsets.YearEnd()
        bar = (Bar()
               .set_global_opts(title_opts=opts.TitleOpts(title="年收益", pos_top=pos_top),
                                legend_opts=opts.LegendOpts(pos_top=pos_top,is_show=False),
                                tooltip_opts=opts.TooltipOpts())
               )

        has_set_xaxis = False
        for k, v in y.items():
            ser = Series(v,index=x)
            ser = ser.groupby(offset.rollforward,group_keys=False).apply(lambda t: t[t.index == t.index.max()])
            if not has_set_xaxis:
                # 只要设置一次X坐标
                bar.add_xaxis(ser.index.tolist()[1:])
                has_set_xaxis = True
            year_rate = ser/ser.shift(1)
            bar.add_yaxis(k,((year_rate-1)*100).round(3).tolist()[1:],xaxis_index=1,yaxis_index=1)
        bar.set_series_opts(label_opts=opts.LabelOpts(formatter='{c}%'))
        return bar

    @classmethod
    def gender_contribution_bar(self, revenue_contribution: Dict, pos_top='30%',pos_left="50%"):
        bar = (Bar()
               .set_global_opts(title_opts=opts.TitleOpts(title="收益贡献率", pos_top=pos_top, pos_left=pos_left),
                                legend_opts=opts.LegendOpts(type_='scroll', pos_bottom='5%', orient='vertical', pos_top='75%', pos_right='0%', is_show=True),
                                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
                                )
               )
        bar.add_xaxis(list(revenue_contribution.keys()))
        bar.add_yaxis(series_name="收益贡献率", y_axis=[round(x-1, 2) for x in revenue_contribution.values()], bar_width='50%', itemstyle_opts=opts.ItemStyleOpts())
        return bar
        

    @classmethod
    def gender_pie(self, trading_count:Dict) ->Pie:
        c = (Pie()
             .add("交易频次", data_pair=[list(z) for z in zip(trading_count.keys(), trading_count.values())],
             center=['85%', '75%'], radius='10%',
             tooltip_opts=opts.TooltipOpts(formatter='{a} <br/>{b} : {c} ({d}%)', background_color='#0000ff55'),)
             .set_global_opts(legend_opts=opts.LegendOpts(type_='scroll', pos_bottom='5%', orient='vertical', pos_top='65%', pos_right='0%', is_show=False),)
             .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='outside'))
             )
        return c
    
    @classmethod
    def gender_sum_rate_line(self,x:List,sum_rate:tuple[List,List]) -> Line:
        c = (
            Line()
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
            .add_xaxis(x)
        )
        c.add_yaxis("沪深300", sum_rate[0], label_opts=opts.LabelOpts(is_show=True),
                    linestyle_opts=opts.LineStyleOpts(width=1.5),
                    xaxis_index=3,
                    yaxis_index=3
                    )
        c.add_yaxis("创业板", sum_rate[1], label_opts=opts.LabelOpts(is_show=True),
                    linestyle_opts=opts.LineStyleOpts(width=1.5),
                    xaxis_index=3,
                    yaxis_index=3
                    )
        return c

    @classmethod
    def showChart(self):
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("soccer.ico"))
        # ex = MyChart()
        # ex.show()
        window = MyWindowFive()
        window.resize(1200,1400)
        # window.move(500,100)
        screen = QDesktopWidget().screenGeometry()
        size = window.geometry()
        # target_point = 
        window.move(int((screen.width() - size.width())/2), int((screen.height() - size.height())/2))
        window.show()
        sys.exit(app.exec_())

class MyWindowOne(QWidget):
    def __init__(self, parent= None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        # 第一行按钮布局管理
        hLayout1 = QHBoxLayout()
        button = QPushButton("Button1")
        button.setMinimumSize(60,30)
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        hLayout1.addWidget(button)
        button = QPushButton("Button2")
        button.setMinimumSize(60,30)
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        hLayout1.addWidget(button)
        # 第二行按钮布局管理
        hLayout2 = QHBoxLayout()
        button = QPushButton("Button3")
        button.setMinimumSize(60,30)
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        hLayout2.addWidget(button)
        button = QPushButton("Button4")
        button.setMinimumSize(60,30)
        button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        hLayout2.addWidget(button)
        # 整体垂直布局管理
        self.layout.addLayout(hLayout1)
        self.layout.addLayout(hLayout2)
        self.setLayout(self.layout)

class MyWindowTwo(QWidget):
    def __init__(self, parent=None)->None:
        super().__init__(parent)
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        
        button = getNormalButton("button1")
        self.layout.addWidget(button,0,0,1,1)
        button = getNormalButton("button2")
        self.layout.addWidget(button,0,1,1,1)
        button = getNormalButton("button3")
        self.layout.addWidget(button,1,0,1,1)
        button = getNormalButton("button4")
        self.layout.addWidget(button,1,1,1,1)
        button = getNormalButton("button5")
        # 列拓展，定位在第二行第一列位置，占1行2列
        self.layout.addWidget(button,2,0,1,2)

        self.setLayout(self.layout)

class MyWindowThree(QWidget):
    # 表单布局
    def __init__(self,parent=None)->None:
        super().__init__(parent=parent)
        self.layout = QFormLayout()
        self.layout.setSpacing(20)
        self.layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        nameEdit = QLineEdit()
        mailEdit =QLineEdit()
        vLayout = QVBoxLayout()
        vLayout.setSpacing(6)
        addrEdit1 = QLineEdit()
        addrEdit2 = QLineEdit()
        vLayout.addWidget(addrEdit1)
        vLayout.addWidget(addrEdit2)
        self.layout.addRow("Name:",nameEdit)
        self.layout.addRow("Mail:",mailEdit)
        self.layout.addRow("Address:",vLayout)

        self.setLayout(self.layout)
        self.setWindowTitle("测试")
class MyWindowFour(QWidget):
    # 栈式布局
    def __init__(self,parent=None):
        super().__init__(parent)
        # self.layoutOne()
        self.layoutTwo()
        
    def layoutOne(self):
        self.layout = QStackedLayout()
        self.layout.addWidget(QPushButton("Button1"))
        self.layout.addWidget(QPushButton("Button2"))
        self.layout.addWidget(QPushButton("Button3"))
        self.layout.addWidget(QPushButton("Button4"))

        self.setLayout(self.layout)
        self.setWindowTitle("Stack Layout")

        # 设置栈顶显示第二个组件
        self.layout.setCurrentIndex(2)
        # 栈布局管理器不能直接嵌套其他的布局管理器，但是可以使用QWidge间接嵌套
    def layoutTwo(self):
        self.layout = QStackedLayout()
        self.layout.addWidget(QPushButton("Button1"))

        # 容器型嵌套
        widge = QWidget()
        vLayout = QVBoxLayout()
        vLayout.addWidget(QPushButton("Button2"))
        vLayout.addWidget(QPushButton("Button3"))
        widge.setLayout(vLayout)
        self.layout.addWidget(widge)

        self.setLayout(self.layout)
        self.layout.setCurrentIndex(1)
class MyWindowFive(QWidget):
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
        # self.myHtml.load(QUrl("file:///Users/yuze.chi/Desktop/jy_test/PythonDataScience/测试结果_沪深300ETF_创业板50ETF_service.html"))
        self.myHtml.load(QUrl("http://localhost:8989/index.html"))
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
        register_button = QPushButton("注册")
        register_button.clicked.connect(self.register)
        change_button = QPushButton("切换指数")
        change_button.clicked.connect(self.changeIndex)
        self.has_change = False

        self.sub_rate_edit = QLineEdit()
        self.sub_rate_edit.setPlaceholderText("请输入sub_rate……")
        self.sub_rate_edit.setText("3")
        self.sub_rate_edit.setValidator(QDoubleValidator(-50, 50, 2))
        self.sub_rate_edit.returnPressed.connect(self.login)

        self.trading_day_sp = QSpinBox()
        self.trading_day_sp.setRange(40, 50000)
        self.trading_day_sp.setValue(200)
        self.trading_day_sp.setSingleStep(100)
        self.trading_day_sp.setKeyboardTracking(False)
        self.trading_day_sp.valueChanged.connect(self.login)
        self.trading_day_sp.lineEdit().returnPressed.connect(self.login)

        self.stock1_edit = QLineEdit()
        self.stock1_edit.setPlaceholderText("请输入第一个stock……")
        self.stock1_edit.setText("510300 1")
        self.stock1_edit.returnPressed.connect(self.login)

        self.stock2_edit = QLineEdit()
        self.stock2_edit.setPlaceholderText("请输入第二个stock……")
        self.stock2_edit.setText("159949 0")
        self.stock2_edit.returnPressed.connect(self.login)

        self.roll_day_sp = QSpinBox()
        self.roll_day_sp.setPrefix("rollday: ")
        self.roll_day_sp.setMinimumWidth(100)
        self.roll_day_sp.setValue(20)
        self.roll_day_sp.lineEdit().returnPressed.connect(self.logout_click)
        self.roll_day_sp.setKeyboardTracking(False) # 不响应输入的事件
        self.roll_day_sp.valueChanged.connect(self.logout_click) # 响应加减数字的事件
        
        logout_button = QPushButton("登出")
        logout_button.clicked.connect(self.logout_click)
        
        form_layout = QFormLayout()
        # 设置子控件的自动拉伸到flow的最大宽度
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.addRow("sub_rate", self.sub_rate_edit)
        form_layout.addRow("test_days", self.trading_day_sp)
        form_layout.addRow("stock1", self.stock1_edit)
        form_layout.addRow("stock2", self.stock2_edit)
        form_layout.addRow("roll_day", self.roll_day_sp)

        vLayout.addWidget(login_button)
        vLayout.addWidget(register_button)
        vLayout.addWidget(change_button)
        vLayout.addLayout(form_layout)
        vLayout.addWidget(logout_button)

        vLayout.addStretch()
        widge = QWidget()
        widge.setLayout(vLayout)

        self.mainSplitter.addWidget(widge)
        self.mainSplitter.addWidget(rightSplitter)

        # 分割比例
        self.mainSplitter.setStretchFactor(0,1)
        self.mainSplitter.setStretchFactor(1,2)

        # self.mainSplitter.show()
        self.setWindowTitle("Splitter")
        self.setLayout(self.layout)

    def login(self):
        # 在子线程刷新数据，回到主线程刷新UI
        self.thread = myQThread(self.target_func,"test11")
        self.thread.mySignal.connect(self.mytestLogin)
        self.thread.start()
    
    def register(self):
        print("开始注册了")
        # self.myHtml.load(QUrl("http://localhost:8989/index.html"))
        # self.myHtml.reload()
        
        self.myHtml.page().runJavaScript('completeAndReturnName();', self.js_callback)

    def changeIndex(self):
        if self.has_change:
            self.stock1_edit.setText("510300 1")
            self.stock2_edit.setText("159949 0")
        else:
            self.stock1_edit.setText("000300 1")
            self.stock2_edit.setText("399006 0")
        self.has_change = not self.has_change
    
    def js_callback(self,result):
        print(result)

    def logout_click(self):
        print("start logout")
        stock1 = self.stock1_edit.text().split(" ")
        stock2 = self.stock2_edit.text().split(" ")
        roll_day = self.roll_day_sp.value()
        result = MyGrid.get_rolling_rate(stock1, stock2, roll_day)
        self.textEdit.setText(result[0] + '\n\n' + result[1])
        print(result)


    def target_func(self,param):
        print("开始要执行耗时操作了！！！！！")
        print("param=",param)
        print("开始要登录:",self.sub_rate_edit.text())
        try:
            sub_rate = float(self.sub_rate_edit.text())
        except:
            sub_rate = 3
            
        test_day = self.trading_day_sp.value()
        
        stock1 = self.stock1_edit.text().split(" ")
        stock2 = self.stock2_edit.text().split(" ")
        stocks = (stock1, stock2)
        print("stocks===",stocks)

        x, y, retracement_df, trading_count, revenue_contribution,hushen_sum_rate,chuangye_sum_rate, chuangye_name, hushen_name = MyGrid.XBXTestServiceData(stocks=stocks, sub_rate=sub_rate,test_days=test_day)

        today = datetime.datetime.today()
        date_str = today.strftime('%Y-%m-%d-%H:%M')
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        my_weak = week_list[today.weekday()]

        self.fileName="../测试结果_{hushen}_{chuangye}_service.html".format(hushen=hushen_name, chuangye=chuangye_name)
        html_title="轮动策略-{xinqi}-{date}".format(xinqi=my_weak, date=date_str)

        rotate_name = "0.轮动策略"
        chuangye_name="1.{}".format(chuangye_name)
        hushen_name="2.{}".format(hushen_name)
        y = dict(zip((rotate_name,chuangye_name,hushen_name),y))
        # MyChart.line_base(x=x, fileName=self.fileName,html_title=html_title, retracement=retracement_df, trading_count=trading_count, revenue_contribution=revenue_contribution,sum_rate=[hushen_sum_rate,chuangye_sum_rate], **y)
        
        # 计算年收益
        my_year_rate = {}
        my_values = {}
        offset = pd.tseries.offsets.YearEnd()
        for k, v in y.items():
            ser = Series(v,index=x)
            ser = ser.groupby(offset.rollforward,group_keys=False).apply(lambda t: t[t.index == t.index.max()])
            year_rate = ser/ser.shift(1)
            my_year_rate["x"] = ser.index.tolist()[1:]
            my_values[k] = ((year_rate-1)*100).round(1).tolist()[1:]
        my_year_rate["values"] = my_values
        # test 写入到json文件
        myDic = {
            "x": x,
            "y": y,
            "retracement": retracement_df.to_dict('list'),
            "trading_count": trading_count,
            "revenue_contribution": revenue_contribution,
            "sum_rate": [hushen_sum_rate, chuangye_sum_rate],
            "year_rate":my_year_rate
        }
        json_str = json.dumps(myDic, ensure_ascii=False)
        with open('./MyHTMLChart/json/test_mytest.json','w') as json_file:
            json_file.write(json_str)
        print("执行完成了")
        
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """
        QWidge自带的方法，重写监听点击
        """
        print(a0)
        # 在mac上command键盘是ControlModifier，control对应的Meta
        if a0.modifiers() == Qt.KeyboardModifier.ControlModifier and a0.key() == Qt.Key.Key_R:
            print("开始按了组合键command+R")
            self.myHtml.reload()
        
        return super().keyPressEvent(a0)

    def mytestLogin(self):
        print("已经接收到信号开始刷新UI")
        # self.myHtml.reload()
        # self.myHtml.load(QUrl("http://localhost:8989/index.html"))
        self.myHtml.page().runJavaScript('completeAndReturnName();', self.js_callback)
        
        # self.myHtml.load(QUrl("file://"+os.path.abspath(self.fileName)))
        
    

class myQThread(QThread):
    mySignal = pyqtSignal()
    def __init__(self,func,param):
        super().__init__()
        self.func = func
        self.param = param
    
    def __del__(self):
        self.wait()
    a = 1
    def run(self):
        myQThread.a += 1
        print("开始运行线程----",myQThread.a)
        self.func(self.param)
        print("执行完了目标函数————")
        self.mySignal.emit()
        # return super().run()


def getNormalButton(text="Button",miniMumSize=(60,30)):
    button = QPushButton(text)
    button.setMinimumSize(miniMumSize[0],miniMumSize[1])
    button.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
    return button