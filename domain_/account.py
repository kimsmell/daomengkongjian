import os_.iostream

class Account:
    config_user_name = '' #配置文件中的name
    name = '' #姓名
    user = '' #账号
    password = '' #密码
    uid = '' #uid
    token = '' #token
    account_huodong_msg  = [] #活动信息
    account_xinxi = '' #账号信息
    server_tongzhi = '' #报名了活动的通知推送 server酱 key

    def __init__(self, data):
        self.name = data['data']['name']
        self.user = data['data']['account']
        self.uid = data['data']['uid']
        self.token = data['data']['token']
        self.password = data['pwd']
        self.account_xinxi = data['data']

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

    #更新account.ini的状态 主要是更新 token account_huodong_msg
    def update_file_account_huodong_msg(self, name):
        os_.iostream.iostream.updata_ini(user = self.user, password  = self.password, token = self.token, account_huodong_msg = self.account_huodong_msg, name = name)
        

    #更新是否报名的状态
    def update_account_huodong_msg(self, id, data): 
        j = 0
        for i in self.account_huodong_msg:
            if i[0] == id:
                self.account_huodong_msg[j] = data
                break
            j += 1

    def add_account_huodong_msg(self, account_huodong_msg):
        for i in account_huodong_msg: #遍历一遍活动信息
            bo = False
            for k in self.account_huodong_msg:
                if i[0] == k[0]:
                    bo = True
            if bo == False: #如果没有信息 那么就追加进去
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