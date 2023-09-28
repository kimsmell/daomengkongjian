import account
import iostream
import login
import request
import json
import time

account_list = []

def baoming(a_account, name):
    account_huodong_msg = a_account.get_account_huodong_msg()
    account_xinxi = a_account.get_account_xinxi()
    server_tuisong_desp = '' #推送text
    server_tuisong_title = '活动报名通知'
    for i in account_huodong_msg:
        if bool(i[4]) == False:
            id = i[0]
            requests1 = request.request.post_baoming(account_xinxi, id)
            if requests1['code'] == '100' or requests1['code'] == '2000011' and requests1.get('msg') !=None and requests1['msg'] == '此活动你已经报名,不能重复报名':
                i[4] = 'true'
                a_account.update_account_huodong_msg(i[0], i)
                server_tuisong_desp += '活动id为：{}已报名，活动名称为：{}，活动地点为{}\n\n\n'.format(i[0], i[1], i[2])
    request.request.server_jiang(server_tuisong_title, server_tuisong_desp, a_account.get_server_tongzhi())
    a_account.update_file_account_huodong_msg(name) #更新account.ini的文件 将token account_huodong_msg更新

def main(data, name):
    user_login = login.Login.login(user=data['user'], password=data['password']) #登录    

    a = account.Account(user_login)
    a.set_server_tongzhi(data['server酱'])
    a.set_config_user_name(name)

    account_huodong = request.request.get_activit(user_login['data']) #获取活动id 活动名称 活动状态

    huodong = iostream.iostream.huodong_ini(account_huodong, user_login) #获取可报名的活动列表
    a.add_account_huodong_msg(huodong) #将活动添加进去
    #开始报名
    baoming(a, name)
    account_list.append(a)
    print(a)

def do_main(a):
    tmp = a
    user_login = login.Login.login(user=a.get_user(), password=a.get_password()) #登录    
    
    a.set_token(user_login['data']['token'])
    a.set_account_xinxi(user_login['data']['account_xinxi'])
    
    account_huodong = request.request.get_activit(user_login['data']) #获取活动id 活动名称 活动状态

    huodong = iostream.iostream.huodong_ini(account_huodong, user_login) #获取可报名的活动列表
    a.add_account_huodong_msg(huodong)#将活动添加进去
    #开始报名
    baoming(a, a.get_config_user_name())

    account_list.remove(tmp)
    account_list.append(a)


if __name__ == '__main__':
    data = iostream.iostream.get_account() #获取账号信息
    
    for i in data: #遍历每个用户 
        a_data = json.loads(data[i])
        main(a_data, i)
    
    sleep_time = 30 * 60
    while True:
        time.sleep(sleep_time)

        for i in account_list:
            do_main(i)
    #每隔多久运行一次

    