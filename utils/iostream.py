# coding=utf-8
from config import config
from utils.request import Request
from utils.out_log import out_log

import os
import json
import datetime

log_file = 1
err_file = 2

config_file = config.config_file


class iostream:

    # 解析account.ini文件
    def get_account():
        s = ''
        if os.path.exists(config_file):
            with open(config_file, mode='r', encoding='utf-8') as f:
                datas = f.readlines()
                for i in datas:
                    s += i.replace('\n', '').replace(' ', '')
        data_s = None
        try:
            data_s = eval(s)
        except Exception as e:
            out_log().out_txt(err_file, "{}: 配置文件错误\n{}".format(datetime.datetime.now(), e))

        return data_s

    # 更新account.ini
    def out_account_ini(datas):
        if os.path.exists(config_file):
            with open(config_file, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(datas))

    # 更新读取后 指定name中的数据
    def updata_ini(user, password, token, account_huodong_msg, name):
        data = iostream.get_account()
        if data != None:
            datas = json.loads(data[name])
            datas['user'] = user
            datas['password'] = password
            datas['token'] = token
            datas['account_huodong_msg'] = account_huodong_msg
            data[name] = json.dumps(datas)
            iostream.out_account_ini(data)

    # 获取account_huodong_msg
    def huodong_ini(huodong, passwd):
        list = []
        for i in huodong:  # 活动id 活动名称 活动状态
            activityId = i['activityId']  # 活动id
            data = Request.get_huodong_xiangxi(passwd['data'], activityId)  # 获取活动详细信息
            # print(data)
            if data == None:
                continue
            # print(data['data']['joindate'])
            # out_log().out_txt(log_file, "活动详细信息：{}".format(data))
            data_t = None
            if data['code'] != '100':
            	continue
            try:
                if data['data']['statusText'] == '规划中' or data['data']['statusText'] == '报名中':
                    data_t = data['data']

            except Exception as e:
                out_log().out_txt(err_file, "{}: 获取活动状态信息错误：{}\n {}".format(datetime.datetime.now(), data, e))

            if data_t == None:
                continue
            list_t = []
            activityName = data_t['activityName']  # 活动名称
            address = data_t['address']  # 活动地址
            unableJoinReason = data_t['countdownText']  # 活动状态 活动开始倒计时 活动结束倒计时 活动结束等
            isbaoming = 0  # 是否报名过

            if data_t['statusText'] == '报名中':
                list_t = [activityId, activityName, address, unableJoinReason, isbaoming, 0, 'null']

            if data_t['statusText'] == '规划中':
                list_t = [activityId, activityName, address, unableJoinReason, isbaoming, 1, data_t['joindate'].replace(' ', '')]
            list.append(list_t)
        return list
