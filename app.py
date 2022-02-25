from flask import Flask, render_template, request
from database import DB_CONN
from eastmoney.kline.kline_test import get_data
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!123'


# 表单提交
@app.route("/search")
def search():
    return render_template("search_code.html")


@app.route('/index')
def index():
    splits, name = get_data()
    return render_template('index.html', splits=splits, name=name)


@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        value = request.form
        code = value.getlist("code")[0]
        if len(code) != 6:
            return "请输入六位代码"
        splits, name = get_data(code=code)
        return render_template("index.html", splits=splits, name=name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
