# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 21:35
# @Author  : DELL
# @Email   : wayne_lau@aliyun.com
# @File    : main.py
# @Project : xiaoyou

from flask import Flask, request, jsonify
from common.db import db_session
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


def create_roles():
    '''创建角色'''
    pass


def get_latest_act_id():
    '''获取最近一次的活动id'''
    sql = "select a_id from activities where CHAR_LENGTH(a_id)=(SELECT max(CHAR_LENGTH(a_id)) from activities) ORDER BY a_id DESC"
    res = db_session.execute(sql).fetchone()
    return res.a_id

def get_latest_content_id():
    '''获取最近一次的活动内容id'''
    sql = "select c_id from act_content where CHAR_LENGTH(c_id)=(SELECT max(CHAR_LENGTH(c_id)) from act_content) ORDER BY c_id DESC"
    res = db_session.execute(sql).fetchone()
    return res.c_id

@app.route('/api/activities', methods=['GET', 'POST'])
def create_act():
    '''创建活动'''
    if request.method == 'POST':
        latest_id = get_latest_act_id()
        a_id = 'a' + str(int(latest_id[1:]) + 1) #自动设置最新的活动id
        print "request.get_json().get('actForm')", request.get_json().get('actForm')
        print "request.get_json().get('contForm')", request.get_json().get('contForm')
        # 活动内容列表
        cont_form = request.get_json().get('contForm')
        # 创建活动
        act_form = request.get_json().get('actForm')
        act_title = act_form.get('act_title')
        act_desc = act_form.get('act_desc')
        date_start = act_form.get('date_start').split('T')[0]
        date_end = act_form.get('date_end').split('T')[0]
        act_contact = act_form.get('act_contact')  # 活动联系人
        is_all = act_form.get('is_all')
        print 'type(a_id)', type(a_id), 'a_id',a_id
        print 'type(act_title)', type(act_title), 'act_title',act_title
        print 'type(act_desc)', type(act_desc), 'act_desc',act_desc
        print 'type(date_start)', type(date_start), 'date_start',date_start
        print 'type(date_end)', type(date_end), 'date_end',date_end
        print 'type(act_contact)', type(act_contact), 'act_contact',act_contact
        print 'type(is_all)', type(is_all), 'is_all',is_all
        try:
            # 新建活动
            sql = "insert into activities (a_id,act_title,act_desc,date_start,date_end,act_contact,is_all)" \
                  "values (:a_id,:act_title,:act_desc,:date_start,:date_end,:act_contact,:is_all)"
            db_session.execute(sql, {'a_id':a_id,'act_title':act_title,'act_desc':act_desc,'date_start':date_start,
                                     'date_end':date_end,'act_contact':act_contact,'is_all':is_all})
            db_session.commit()
            # 新建活动内容
            create_act_cont(a_id, cont_form)
            return jsonify({'code': '1', 'msg': '创建活动成功！'})
        except Exception as e:
            print 'create_act=>ERROR,str(e): ', str(e)
            return jsonify({'code': '0', 'msg': '创建活动失败，请联系管理员！'})


def create_a2c_relationship(a_id, c_ids):
    """创建活动与活动内容的关联"""
    if a_id and c_ids:
        for c_id in c_ids:
            sql = """insert into act_has_cont (a_id, c_id) values (:a_id, :c_id)"""
            try:
                db_session.execute(sql, {'a_id': a_id, 'c_id': c_id})
            except Exception as e:
                print 'create_a2c_relationship=>ERROR,str(e): ', str(e)
        db_session.commit()



def create_act_cont(a_id, cont_form):
    '''创建活动内容'''
    # 创建活动
    print 'create_act_cont=>a_id', a_id
    latest_cid = get_latest_content_id()  # 已存在的最大c_id  c4
    c_ids = []  # 此a_id的所有活动内容的id
    activates = cont_form.get('activates')
    step = 1
    for act_cont in activates:
        c_id = 'c' + str(int(latest_cid[1:])+step)
        c_ids.append(c_id)
        charger = act_cont.get('charger')
        company = act_cont.get('company')
        start_time = act_cont.get('start_time')
        end_time = act_cont.get('end_time')
        bus_station = act_cont.get('bus_station')
        gps = act_cont.get('gps')
        address = act_cont.get('address')
        print 'c_id', c_id
        print 'type(charger)', type(charger), 'charger', charger
        print 'type(company)', type(company), 'company', company
        print 'type(start_time)', type(start_time), 'start_time', start_time
        print 'type(bus_station)', type(bus_station), 'bus_station', bus_station
        print 'type(end_time)', type(end_time), 'end_time', end_time
        print 'type(gps)', type(gps), 'gps', gps
        print 'type(address)', type(address), 'address', address
        # 插入活动
        sql = """insert into act_content (c_id,charger,company,time_start,time_end,addr,gps,bus_station) 
        values (:c_id,:charger,:company,:time_start,:time_end,:addr,:gps,:bus_station)"""
        try:
            db_session.execute(sql, {
             'c_id': c_id, 'charger': charger, 'company': company, 'time_start': start_time,
                'time_end': end_time, 'addr': address, 'gps': gps, 'bus_station': bus_station
            })
        except Exception as e:
            print 'create_act_cont=>ERROR,str(e): ', str(e)
        step += 1
    # 全部插入后才提交
    db_session.commit()
    # 创建活动与活动内容的关联
    create_a2c_relationship(a_id, c_ids)


def check(phone, a_id):
    '''传入电话，活动id，查看该电话是否已经报名本次活动'''
    text = "select * from join_act_details where phone=:phone and act_id=:a_id"
    print 'text: ', text
    res = None
    try:
        result = db_session.execute(text, {'phone': phone, 'a_id': a_id}).fetchone()
        res = {'title': result.act_title, 'phone': result.phone, 'acr_id': result.act_id}
    except Exception as e:
        print 'check(%s,%s)==>str(e):%s' % (phone, a_id, str(e))
        return False
    else:
        return res

def curtime():
    cur = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return cur

@app.route('/', methods=['GET'])
def index():
    return jsonify({'code':'XXX','msg':'test'})

@app.route('/api/login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        pwd = request.get_json().get('pwd')
        name = request.get_json().get('name')
        sql = "select * from roles"
        res = db_session.execute(sql).fetchone()
        db_name = res.account
        db_pwd = res.pwd
        if db_name == name and db_pwd == pwd:
            return jsonify({'result': '登录成功', 'status': '0'})
        if db_pwd != pwd and db_name != name:
            return jsonify({'result': '密码，密码都不正确', 'status': '-3'})
        if db_name != name:
            return jsonify({'result': '账号不正确', 'status': '-1'})
        if db_pwd != pwd:
            return jsonify({'result': '密码不正确', 'status': '-2'})


@app.route('/api/actdetail', methods=['GET'])
def get_act_details():
    """最新id的活动内容"""
    latest_a_id = get_latest_act_id()
    sql = "select * from act_details where act_id='%s'" %latest_a_id
    res = db_session.execute(sql).fetchall()
    print 'get_act_details,res: ', res
    a_id = ''
    act_contact = ''
    act_desc = ''
    act_title = ''
    act_start = ''
    act_end = ''
    is_all = ''
    act_contents = []
    for r in res:
        act_contents.append({'cont_id': r.cont_id, 'addr':r.addr,'bus_station':r.bus_station,'charger':r.charger,
                             'company':r.company,'gps':r.gps,'time_start':r.time_start,'time_end':r.time_end})
        a_id = r.act_id
        act_contact = r.act_contact
        act_desc = r.act_desc
        act_title = r.act_title
        act_start = r.act_start
        act_end = r.act_end
        is_all = r.is_all
    return jsonify({'a_id':a_id,'act_contact':act_contact,'act_desc':act_desc,
                    'act_title':act_title,'act_start':act_start,'act_end':act_end,'is_all':is_all,
                    'act_contents':act_contents})

# 添加登录视图，如果是GET方法，返回一个简单的表单
@app.route('/api/insetdata', methods=['GET', 'POST'])
def insert_data():
    print 'request',request
    if request.method == 'POST':
        c_ids = request.get_json().get('c_ids')  #数组
        name = request.get_json().get('name')
        phone = request.get_json().get('telphone')
        departure = request.get_json().get('departure')
        a_id = request.get_json().get('a_id')
        # time = request.get_json().get('time')
        insert_time = curtime()
        passenger = request.get_json().get('passenger')
        print 'c_ids',c_ids
        # r = True
        r = check(phone,a_id)
        print 'r', r
        if r:
            return jsonify({'code': '0', 'msg': '该号码 '+phone+' 已经参加此次活动！'})
        #以下未完成，
        #更新person_info表（有则按phone更新，无则插入）
        text = "insert into person_info (name,phone,start_position) values ('%s','%s','%s') on conflict(phone) do update set name=EXCLUDED.name , start_position=EXCLUDED.start_position"  % (name,phone,departure)
        db_session.execute(text)
        db_session.commit()
        #插入join_content表
        has_car = ''
        if passenger != '无':
            has_car = 'yes'
        else:
            has_car = 'no'
        for c_id in c_ids:
            text = "insert into join_act_cont (phone,c_id,drive_people,drive_car,insert_time) " \
                   "values ('%s','%s','%s','%s','%s')" % (phone,c_id,passenger,has_car,insert_time)
            db_session.execute(text)
            db_session.commit()
        return jsonify({'code':'1', 'msg':'报名成功！'})

@app.route('/api/getall/<aid>',methods=['GET', 'POST'])
def get_all(aid):
    # text = "select * from xiaoyou_person_info"
    text = "select * from table_review where act_id=:a_id"
    res = db_session.execute(text,{'a_id':aid}).fetchall()
    ret = []
    tmp = {}
    for r in res:
        tmp['name'] = r.name
        tmp['phone'] = r.phone
        tmp['departure'] = r.start_position
        tmp['act_title'] = r.act_title
        tmp['act_content'] = r.chargers
        tmp['passengers'] = r.drive_people
        tmp['time'] = r.insert_time
        ret.append(tmp)
        tmp = {}
    return jsonify({'result': ret})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='8765', debug=False)  # pycharm2018坑
    app.run(host='127.0.0.1', port='8765', debug=False)  # pycharm2018坑
    # app.run(debug=False)  # pycharm2018坑
    # app.run()
    # r = check('13242309894')
    # r = check('www')
    # print type(r)
    # print r
    # print len(r)
    # print check('13232464678', 'a0')
    # # print check('12222222', 'a0')
    # create_act()

