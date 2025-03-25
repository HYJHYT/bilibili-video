from flask import Flask, render_template, jsonify
from function import find_echarts4, find_echarts1, find_echarts3, find_echarts2, find_echarts5,find_table,find_echarts6
from admin import Admin
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  #设置密钥
app.register_blueprint(Admin, url_prefix='/admin')

#主页
@app.route('/')
def hello_world():
    return render_template("index.html")


#表1接口
@app.route('/echarts1', methods=['get', 'post'])
def echarts1():
    data1, data2, data3 = find_echarts1()
    data1.reverse()
    data2.reverse()
    data3.reverse()
    return jsonify({'data1': data1, 'data2': data2, 'data3': data3})

#表2接口
@app.route('/echarts2', methods=['get', 'post'])
def echarts2():
    data1, data2 = find_echarts2()
    return jsonify({'data1': data1, 'data2': data2})

#表3接口
@app.route('/echarts3', methods=['get', 'post'])
def echarts3():
    data, words = find_echarts3()
    return jsonify({"words": words, "data": data})

#表4接口
@app.route('/echarts4', methods=['get', 'post'])
def echarts4():
    data, words = find_echarts4()
    return jsonify({"words": words, "data": data})

#表5接口
@app.route('/echarts5', methods=['get', 'post'])
def echarts5():
    data, words = find_echarts5()
    return jsonify({"words": words, "data": data})

#表格数据接口
@app.route('/table', methods=['get', 'post'])
def table():
    data,words = find_table()
    return jsonify({"words": words, "data": data})

#表6接口
@app.route('/echarts6', methods=['get', 'post'])
def echarts6():
    data,sum = find_echarts6()
    return jsonify({"data": data,"sum": sum})


if __name__ == '__main__':
    app.run()
