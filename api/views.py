from api import api_blue
from flask import *
import requests, json
import time, datetime
import LTDB, UCache


db = LTDB.LTDB(host, user, password, database)
uc = UCache.UC()


@api_blue.route('/', methods=['GET'])
def Fin():
    return 'OK'

@api_blue.route('/tables', methods=['GET'])
def Table():
    return jsonify(db.tables)

@api_blue.route('/req/<table>', methods=['GET'])
def Req_table(table=''):
    try:
        limit = int(request.values.get('limit', '0'))
        where = json.loads(request.values.get('where', '{}'))
        ntype = request.values.get('ntype', 'list')
        if ntype == 'dict': ntype = dict
        else: ntype = list
    except:return jsonify([])
    data = db.GetData(table, where=where, limit=limit, ntype=ntype, nopin=True)
    return jsonify(data)

@api_blue.route('/uc/uuid/<uuid>', methods=['GET'])
def SearchByuuid(uuid=''):
    data = uc.SearchBy('uuid', uuid)
    return jsonify(data)

@api_blue.route('/uc/name/<name>', methods=['GET'])
def SearchByName(name=''):
    data = uc.SearchBy('name', name)
    return jsonify(data)

@api_blue.route('/newbans', methods=['GET', 'POST'])
def Newbans():
    if not session.get('uid'):return jsonify({'info':'account_error'})
    level = session['all'].get('level', 'player')
    if level != 'manager': return jsonify({'info':'level_error'})

    target_uuid = request.values.get('target_uuid')
    reason = request.values.get('reason', '')
    until = int(request.values.get('until', '-1'))
    if None in [target_uuid, reason, until]: return jsonify({'info':'info_error'})

    ntime = int(round(time.time() * 1000))
    if until != -1:etime = ntime
    else:etime = -1

    req = {
        'uuid':target_uuid,
        "ip":None,
        "reason":reason,
        "banned_by_uuid":session['uid'], 
        "banned_by_name":uc.SearchBy('uuid', session['uid']).get('name'), 
        "removed_by_uuid":None,
        "removed_by_name":None,
        'removed_by_date':str( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(ntime/1000))) ),
        "server_scope":'*', 
        "server_origin":'Minecraft-LEAC',
        'time':ntime,
        'until':etime,
        'active':1,
    }

    res = db.NewData('litebans_bans', req, fore_load=False)

    return str(res)

@api_blue.route('/delbans', methods=['POST'])
def Deletebans():
    if not session.get('uid'):return jsonify({'info':'account_error'})
    return ''