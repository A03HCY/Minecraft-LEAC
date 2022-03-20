from auth import auth_blue
from flask import *
import requests, json
import User as DB


User = DB.UserDB('./auth/UserData.xlsx')


@auth_blue.route('/login', methods=['GET', 'POST'])
def Login():
    # If it isn't need to
    if session.get('uid'):
        return redirect('/',code=302,Response=None)
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.values.get('email')
    pwd = request.values.get('password')
    rem = request.values.get('remember')
    
    info = User.SearchBy(email, 'email')
    if info.get('password') == DB.MD5(pwd):
        session['uid'] = info.get('uid')
        session['all'] = info
        if rem == 'remember':session.permanent = True
        else:session.permanent = False
        return 'True'
    else:
        return 'False'


@auth_blue.route('/logout', methods=['GET'])
def Logout():
    try:
        session.pop('uid')
        session.pop('all')
    except:pass
    return 'True'


@auth_blue.route('/info', methods=['GET'])
def Info():
    uid = request.values.get('uid')
    if uid == None:uid = session.get('uid')
    if uid == None:return jsonify({})
    info = User.SearchBy(int(uid), 'uid')
    try:
        info.pop('password')
        info.pop('row')
    except:pass
    return jsonify(info)


@auth_blue.route('/head', methods=['GET', 'POST'])
def Head():
    uid = request.values.get("uid")
    if uid == None:
        uid = session.get('all', {}).get('uid')
    
    tar = "https://crafatar.com/avatars/{}?size=100&overlay".format(uid)
    try:req = requests.get(tar)
    except:return ''
    return req.content