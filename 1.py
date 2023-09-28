import json
import os
from pyDes import des, ECB, PAD_PKCS5
import binascii
import requests
import time, datetime
import account

d_version = '4.5.6'
account_huodong_msg = {} #key：活动id value：所报名的活动 是否报名过 报名的账号uid

headers = {
    'standardUA': '{"uuid":"d0824ff00c104312acb3e91f0f6c1b89","system":"iOS","version":"4.5.8","sysVersion":"15.6","screenResolution":"1242.000000-2688.000000","JPushId":"d0824ff00c104312acb3e91f0f6c1b89","countryCode":"CN","channelName":"dmkj_iOS","createTime":"0","operator":"%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8460660","modifyTime":"0","device":"iPhone 13 Pro Max","hardware":"D64AP,iPhone14,3,arm64,255877271552,1604567040","startTime":"1695387433"}',
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Cookie':'acw_tc=2f624a5016958158420312945e34eae2f925c163d6ad7b4cb28af85273fbeb',
    'Content-Length': '526',
    'Accept-Language': 'zh-Hans-CN;q=1, fr-CA;q=0.9, en-CN;q=0.8',
    'Host': 'appdmkj.5idream.net',
    'Connection': 'keep-Alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'DMKJ/4.5.8 (iPhone; iOS 15.6; Scale/3.00)',

}


def Apply(user, pwd):
    """
    账号登陆,返回uid和token
    account  登陆账号
    pwd      加密后的密码
    :param account:
    :param pwd:
    :return:
    """
    pwd_ = get_pwd(pwd)
    url = 'https://appdmkj.5idream.net/v2/login/phone'
    data = {
        'pwd': pwd_,
        'account': user,
        'version': d_version
    }

    response = requests.post(url=url, headers=headers, data=data).json()
    response.update(account=user, pwd=pwd)
    response1 = json.dumps(response)
    with open('token', mode='w', encoding='utf-8') as f:
        f.write(response1)

    return response

def get_pwd(s):
    """
    获取密码加密结果
    :param s:
    :return:
    """
    KEY = '51434574'
    secret_key = KEY
    k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).upper().decode('utf-8')


def get_huodong_xiangxi(accounts_data, id):
    """
    获取活动开始时间
    :param accounts_data:
    :param id:
    :return:
    """
    url = 'https://appdmkj.5idream.net/v2/activity/detail'
    token = accounts_data['token']
    uid = accounts_data['uid']
    data_get_time = {
        'uid': uid,  # 登陆接口获取
        'token': token,  # 登陆接口获取
        'activityId': int(id),  # 活动ID
        'version': d_version,
    }

    huodong = requests.post(url=url, headers=headers, data=data_get_time).json()
    return huodong


def get_activit(accounts_data):
    """
    获取可以报名的活动
    uid     每个账号不同的uid
    token   账号的token
    :param accounts_data
    :return:
    """
    activitys = []
    url = 'https://appdmkj.5idream.net/v2/activity/activities'
    token = accounts_data['token']
    uid = accounts_data['uid']
    data = {
        'joinStartTime': '',
        'token': token,  # 登陆接口获取
        'startTime': '',
        'endTime': '',
        'joinFlag': '1',
        'collegeFlag': '',
        'catalogId': '',
        'joinEndTime': '',
        'specialFlag': '',
        'status': '',
        'keyword': '',
        'version': d_version,
        'uid': uid,  # 登陆接口获取
        'sort': '',
        'page': '1',
        'catalogId2': '',
        'level': '',
    }
    response = requests.post(url=url, headers=headers, data=data).json()
    lists_data = response['data']['list']
    for data_ in lists_data:
        activityId = data_['activityId']
        name = data_['name']
        statusText = data_['statusText']
        activity = {'activityId': activityId, 'name': name, 'statusText': statusText}
        activitys.append(activity)
    return activitys

# def get_token():
#     account = "15170041151" #account
#     pwd = "Kimsmell001" #password
    
#     if os.path.exists('token'):
#         with open('token', mode='r', encoding='utf-8') as f:
#             datas = f.readlines()[0]
#             if datas != []:
#                 data_s = json.loads(datas)
#                 account = data_s['account']
#                 pwd = data_s['pwd']
    
#     return account, pwd

def get_huodong_time():
    # time_ = huodong['data']['joindate'].split('-')[0]
    # time_data = [time_[0:4], time_[5:7], time_[8:10], time_[11:13], time_[14:16], set_data['data']['activityName']]
    # print(huodong['data']['activityName'])
    return huodong['data']['activityName']

def read_huodong_txt():
    if os.path.exists('huodong'):
        with open('huodong', mode='r', encoding='utf-8') as f:
            datas = f.readlines()
            if datas != []:
                for i in datas:
                    data = json.loads(i)
                    for j in data:
                        lis = data[j]
                        account_huodong_msg[j] = lis
    #读取文件内容到list 

def out_huodong_txt():
    with open('huodong', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(account_huodong_msg))
            
    #输出list到文件中去

def huodong_ini(huodong, passwd):
    if os.path.exists('huodong'):
        with open('huodong', mode='r', encoding='utf-8') as f:
            if account_huodong_msg == {} and f.readlines() == []:
                list_ini(huodong, passwd)
            else:
                read_huodong_txt()
    #如果list中没有数据 文件中没有数据 那就写入数据到list中去

def get_huodong(passwd, id):
    info = [{"conent": "", "content": "", "fullid": "79857", "key": 1, "notList": "false", "notNull": "false",
                "system": 0,
                "title": "姓名"}]

    data1 = {
        'uid': passwd['uid'],  # 登陆接口获取
        'token': str(passwd['token']),  # 登陆接口获取
        'remark': '',
        'data': str(info),  # 活动报名参数
        'activityId': id,  # 活动ID
        'version': d_version,
    }
    response1 = requests.post(url='https://appdmkj.5idream.net/v2/signup/submit', data=data1,
                                headers=headers).json()
    return response1

def list_ini(huodong, passwd):
    for i in huodong: #活动id 活动名称 活动状态
        activityId = i['activityId'] #活动id
        data = get_huodong_xiangxi(passwd['data'], activityId)
        activityName = data['data']['activityName'] #活动名称
        address = data['data']['address'] #活动地址
        unableJoinReason = data['data']['countdownText'] #结束倒计时  如果报名人数已满 那么会显示报名人数已满否则显示倒计时
        isbaoming = 'false' #是否报名过
        account_huodong_msg[activityId] = [activityId, activityName, address, unableJoinReason, isbaoming]
    #将可报名的活动加入到list中去
    out_huodong_txt()
    #写入到文件中

def main(passwd, id):
    """
    提交报名函数
    :param passwd:
    :param id:
    :return:
    """
    info = [{"conent": "", "content": "", "fullid": "79857", "key": 1, "notList": "false", "notNull": "false",
                "system": 0,
                "title": "姓名"}]

    data1 = {
        'uid': passwd['uid'],  # 登陆接口获取
        'token': str(passwd['token']),  # 登陆接口获取
        'remark': '',
        'data': str(info),  # 活动报名参数
        'activityId': id,  # 活动ID
        'version': d_version,
    }
    response1 = requests.post(url='https://appdmkj.5idream.net/v2/signup/submit', data=data1,
                                headers=headers).json()
    print(response1)

def baoming(passwd, huodong):
    for i in huodong:
        id = huodong['activityId']
        if account_huodong_msg[id][3] == 'false':
            main(passwd, id)
            account_huodong_msg[id][3] = 'true'
            out_huodong_txt() #更新list状态到文件中去

if __name__ == '__main__':
    user, pwd = account.Account.get_token() #先获取token
    print(user, pwd)
    passwd = Apply(account=user, pwd=pwd)  #登录
    print(passwd)
    if passwd['code'] == 100:
        print("login error！")
        sys.exit()
    #检查是否登录成功

    huodong = get_activit(passwd['data']) #获取活动id 活动名称 活动状态
    print(huodong)
    huodong_ini(huodong, passwd) #保证list中有数据

    #进行报名
    # baoming(passwd, huodong)

    # list_ini(huodong)   #初始化list

    # passwd1['token'] = passwd['data']['token']
    # passwd1['uid'] = passwd['data']['uid']


    # huodong = get_huodong_xiangxi(passwd['data'], ID)

    # startTime = datetime.datetime(int(time_[0]), int(time_[1]), int(time_[2]), int(time_[3]), int(time_[4]), 00)

    # print(f'登陆成功,活动名为{time_[5]}\n开抢时间为{startTime}\n等待中...')
    # print('延迟为:', float(time_sleep))
    # while datetime.datetime.now() < startTime:
    #     time.sleep(float(time_sleep))
    # print('开始抢...')

    # main(passwd1, ID)
    # input('按回车退出程序')
