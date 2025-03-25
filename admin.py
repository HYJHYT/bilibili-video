# -*- coding: UTF-8 -*- #

from flask import Blueprint, render_template, jsonify, request, redirect, session
from function import save_echart,save_admin,check_admin,save_echart3,save_echart5
Admin = Blueprint('admin', __name__)


@Admin.before_request
def before_request():
    if request.path == '/admin/login':
        return None
    if session.get("user"):
        return None
    return redirect("/admin/login")


@Admin.route('/',methods=['GET','POST'])
def admin():
    return render_template('admin.html')

@Admin.route('/register',methods=['get', 'post'])
def register():
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    save_admin(user,pwd)
    return redirect('/admin/login')

@Admin.route('/login',methods=['get', 'post'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    res = check_admin(user)
    if res:
        if res[0] == pwd:
            session["user"] = user
            return redirect('/admin')
        else:
            return render_template("login.html",pwd_error="密码错误")
    return render_template("login.html",user_error="用户不存在")

@Admin.route('/1',methods=['GET','POST'])
def admin1():
    return render_template('echarts1.html')

@Admin.route('/echart1',methods=['GET','POST'])
def admin_echart1():
    try:
        min = request.form.get("min")
        max = request.form.get("max")
        save_echart(min,max,'echart1','colemin','colemax')
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})

@Admin.route('/2',methods=['GET','POST'])
def admin2():
    return render_template('echarts2.html')

@Admin.route('/echart2',methods=['GET','POST'])
def admin_echart2():
    try:
        min = request.form.get("min")
        max = request.form.get("max")
        save_echart(min,max,'echart2','fansmin','fansmax')
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})

@Admin.route('/3',methods=['GET','POST'])
def admin3():
    return render_template('echarts3.html')

@Admin.route('/echart3',methods=['GET','POST'])
def admin_echart3():
    try:
        form = request.form.to_dict()
        save_echart3(form)
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})


@Admin.route('/4',methods=['GET','POST'])
def admin4():
    return render_template('echarts4.html')

@Admin.route('/echart4',methods=['GET','POST'])
def admin_echart4():
    try:
        min = request.form.get("min")
        max = request.form.get("max")
        save_echart(min,max,'echart4','watchmin','watchmax')
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})


@Admin.route('/5',methods=['GET','POST'])
def admin5():
    return render_template('echarts5.html')

@Admin.route('/echart5',methods=['GET','POST'])
def admin_echart5():
    try:
        form = request.form.to_dict()
        save_echart5(form)
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})

@Admin.route('/6',methods=['GET','POST'])
def admin6():
    return render_template('echarts6.html')


@Admin.route('/echart6',methods=['GET','POST'])
def admin_echart6():
    try:
        min = request.form.get("min")
        max = request.form.get("max")
        save_echart(min,max,'echart6','barragemin','barragemax')
        return jsonify({"msg":True})
    except:
        return jsonify({"msg":True,"data":"刷新失败"})


