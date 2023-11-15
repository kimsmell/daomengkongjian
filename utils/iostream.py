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
    def updata_ini(self, uid, token, account_xinxi, name):
        config.mysql.update_one("update `user` set uid=%s where `name`=%s", (uid, name))  # 更新token
        config.mysql.update_one("update `user` set token=%s where `name`=%s", (token, name))  # 更新token
        config.mysql.update_one("update `user` set account_msg=%s where `name`=%s",
                                (account_xinxi, name))  # 更新account_huodong_msg


    # 获取account_huodong_msg
    def huodong_ini(huodong, passwd, phone):
        list = []
        for i in huodong:  # 活动id 活动名称 活动状态
            activityId = i['activityId']  # 活动id
            data = Request.get_huodong_xiangxi(passwd['data'], activityId)  # 获取活动详细信息
            if int(data['code']) != 100:
                continue
            # print(data['data']['joindate'])
            # out_log().out_txt(log_file, "活动详细信息：{}".format(data))
            data_t = None
            try:
                if data['data']['statusText'] == '规划中' or data['data']['statusText'] == '报名中':
                    data_t = data['data']

            except Exception as e:
                out_log().out_txt(err_file,
                                  "{}: 获取活动状态信息错误：{}\n {}{}".format(datetime.datetime.now(), data, e, data['code']))

            if data_t == None:
                continue
            dic = {}
            dic['phone'] = phone
            dic['huodong_id'] = activityId
            dic['huodong_name'] = data_t['activityName']  # 活动名称
            dic['huodong_position'] = data_t['address']  # 活动地址
            dic['huodong_state'] = data_t['countdownText']  # startdate 活动持续时间
            # 活动状态 活动开始倒计时 活动结束倒计时 活动结束等
            dic['huodong_shifou_baoming'] = 0  # 是否报名过

            if data_t['statusText'] == '报名中':
                dic['huodong_shifou_kebaoming'] = 0
                dic['huodong_time'] = 'null'
            if data_t['statusText'] == '规划中':
                dic['huodong_shifou_kebaoming'] = 1
                dic['huodong_time'] = data_t['joindate'].replace(' ', '')
            list.append(dic)
        return list