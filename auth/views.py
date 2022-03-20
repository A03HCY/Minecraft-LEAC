from auth import auth_blue
from flask import *
import requests, json
import User as DB


User = DB.UserDB('./auth/User.xlsx')


@auth_blue.route('/login', methods=['GET', 'POST'])
def Login():
    # If it isn't need to
    if session.get('uid'):
        return redirect('/',code=302,Response=None)
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    pwd = request.form.get('password')
    
    info = User.SearchBy(email, 'email')
    if info.get('password') == DB.MD5(pwd):
        session['uid'] = info.get('uid')
        session['all'] = info
        return 'True'
    else:
        return 'False'


@auth_blue.route('/logout', methods=['GET'])
def Logout():
    try:
        session.pop('uid')
        session.pop('all')
    except:pass
    return redirect('/auth/login',code=302,Response=None)


@auth_blue.route('/info', methods=['GET'])
def Info():
    uid = session.get('uid')
    if not uid:return json.dumps({})
    info = session.get('all')
    info.pop('password')
    info.pop('row')
    return json.dumps(info)


@auth_blue.route('/head', methods=['GET'])
def Head():
    uid = request.values.get("uid")
    if not uid:
        head = session.get('all').get('head')
    else:
        head = User.SearchBy(uid, 'uid').get('head')
    
    tar = "http://q1.qlogo.cn/g?b=qq&nk={}&s=640".format(str(head))
    try:req = requests.get(tar)
    except:return ''
    return req.content