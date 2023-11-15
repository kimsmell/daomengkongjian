from utils.iostream import iostream
from utils.request import Request
from utils.out_log import out_log
from config import config
import datetime


class Account:
    config_user_name = ''  # 配置文件中的name
    name = ''  # 姓名
    user = ''  # 账号
    password = ''  # 密码
    uid = ''  # uid
    token = ''  # token
    account_huodong_msg = []  # 活动信息
    account_xinxi = ''  # 账号信息
    server_tongzhi = ''  # 报名了活动的通知推送 server酱 key

    def __init__(self, data):
        self.name = data['data']['name']
        self.user = data['data']['account']
        self.uid = data['data']['uid']
        self.token = data['data']['token']
        self.password = data['pwd']
        self.account_xinxi = data['data']

        config.mysql.update_one('update user set token=%s where `name`=%s', (self.token, self.name))
        config.mysql.update_one('update user set uid=%s where `name`=%s', (self.uid, self.name))

    def set_user(self, user):
        self.user = user

    def set_password(self, password):
        self.password = password

    def set_uid(self, uid):
        self.uid = uid

    def set_token(self, token):
        self.token = token

    def set_server_tongzhi(self, server_tongzhi):
        self.server_tongzhi = server_tongzhi

    def set_config_user_name(self, config_user_name):
        self.config_user_name = config_user_name

    # 更新account.ini的状态 主要是更新 token account_huodong_msg account_huodong_msg
    def update_file_account_huodong_msg(self, name):
        iostream.updata_ini(self=self, uid=self.uid, token=self.token, account_xinxi=self.account_xinxi, name=name)
        for i in self.account_huodong_msg:
            phone = i['phone']
            id = i['huodong_id']
            tmp = config.mysql.select_all('select * from msg where phone=%s and huodong_id=%s', (phone, id))
            if len(tmp) == 0:
                config.mysql.insert_one(
                    'insert into `msg` (`phone`, `huodong_id`, `huodong_name`, `huodong_position`, `huodong_state`, `huodong_shifou_baoming`, `huodong_shifou_kebaoming`, `huodong_time`) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (phone, id, i['huodong_name'], i['huodong_position'], i['huodong_state'],
                     i['huodong_shifou_baoming'], i['huodong_shifou_kebaoming'], i['huodong_time']))
            else:
                config.mysql.update_one('update `msg` set huodong_state=%s where phone=%s and huodong_id=%s',
                                        (i['huodong_state'], phone, id))
                config.mysql.update_one('update `msg` set huodong_shifou_baoming=%s where phone=%s and huodong_id=%s',
                                        (i['huodong_shifou_baoming'], phone, id))
                config.mysql.update_one('update `msg` set huodong_shifou_kebaoming=%s where phone=%s and huodong_id=%s',
                                        (i['huodong_shifou_kebaoming'], phone, id))
                config.mysql.update_one('update `msg` set huodong_time=%s where phone=%s and huodong_id=%s',
                                        (i['huodong_time'], phone, id))

    # 更新是否报名的状态
    def update_account_huodong_msg(self, id, data):
        j = 0
        for i in self.account_huodong_msg:
            if i['huodong_id'] == id:
                self.account_huodong_msg[j] = data
                break
            j += 1

    def update_huodong(self):
        i = 0
        for j in self.account_huodong_msg:  # 活动id 活动名称 活动状态
            activityId = self.account_huodong_msg[i]['huodong_id']  # 活动id
            data = Request.get_huodong_xiangxi(self.account_xinxi, activityId)  # 获取活动详细信息
            if data == None:
                continue

            try:
                data_t = data['data']
                self.account_huodong_msg[i]['huodong_state'] = data_t['countdownText']
            except Exception as e:
                out_log().out_txt(config.err_file, "{}: 更新活动状态信息错误：{}\n {}".format(datetime.datetime.now(), data, e))
            i += 1

        i = 0
        for j in self.account_huodong_msg:
            if j['huodong_state'] == '活动已结束，请去瞧瞧其他活动' or j['huodong_state'] == '学校管理关闭了该活动':
                self.account_huodong_msg.remove(j)
                config.mysql.delete_one('delete from msg where `phone`=%s and `huodong_id`=%s',
                                        (self.user, j['huodong_id']))
                out_log().out_txt(1, f"已移除：{j}")

    def add_account_huodong_msg(self, account_huodong_msg):
        tmp = self.account_huodong_msg

        for i in account_huodong_msg:  # 遍历一遍活动信息
            bo = False
            for k in tmp:
                if i['huodong_id'] == k['huodong_id']:
                    bo = True

            if bo == False:  # 如果没有信息 那么就追加进去
                self.account_huodong_msg.append(i)

    def set_account_xinxi(self, account_xinxi):
        self.account_xinxi = account_xinxi

    def get_user(self):
        return self.user

    def get_config_user_name(self):
        return self.config_user_name

    def get_server_tongzhi(self):
        return self.server_tongzhi

    def get_account_xinxi(self):
        return self.account_xinxi

    def set_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_uid(self):
        return self.uid

    def get_token(self):
        return self.token

    def get_account_huodong_msg(self):
        return self.account_huodong_msg
