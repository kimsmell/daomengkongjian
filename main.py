import domain_.account
import os_.iostream
import os_.out_log
import util_.login
import http_.request
import json
import datetime
import time


account_list = []
out_log = os_.out_log.out_log()
log_file = out_log.get_log_file()
err_file = out_log.get_err_file()

def baoming(a_account, name):
    account_huodong_msg = a_account.get_account_huodong_msg() #获取已保存的活动信息
    account_xinxi = a_account.get_account_xinxi() #获取登录信息
    server_tuisong_desp = '' #推送text
    server_tuisong_title = '活动报名通知'

    out_log.out_txt(log_file, "报名前活动信息：{}".format(account_huodong_msg))  #打印活动信息日志
    for i in account_huodong_msg:   #遍历一遍活动信息

        if int(i[4]) == 0:
            out_log.out_txt(log_file, "开始报名")   #打印日志
            id = i[0] #获取活动id
            requests1 = http_.request.request.post_baoming(account_xinxi, id) #进行报名 发送报名的请求
            if requests1 == None:
               return
            out_log.out_txt(log_file, "报名请求发送状态：{}".format(requests1)) #打印报名状态日志

            if requests1['code'] == '100' or requests1['code'] != '100' and requests1.get('msg') !=None : #如果报名成功 那么就进行更新推送消息的信息
                i[4] = 1    #将活动信息状态更改
                a_account.update_account_huodong_msg(i[0], i) #更新目前活动信息状态
                server_tuisong_desp += '活动id为：{}已报名，活动名称为：{}，活动地点为{}\n\n\n'.format(i[0], i[1], i[2]) #更新将要推送的消息文本
                out_log.out_txt(log_file, "报名后活动信息：{}".format(a_account.get_account_huodong_msg()))  #打印报名后活动信息的日志

    if server_tuisong_desp != '':   #如果报名成功 那么推送消息的文本不为空
        http_.request.request.server_jiang(server_tuisong_title, server_tuisong_desp, a_account.get_server_tongzhi()) #进行推送消息
        out_log.out_txt(log_file, "name:{}, {}".format(name, server_tuisong_desp))  #打印推送消息的信息到日志中
    a_account.update_file_account_huodong_msg(name) #更新account.ini的文件 将token account_huodong_msg更新

def main(data, name):
    user_login = util_.login.Login.login(user=data['user'], password=data['password']) #登录    
    if user_login == None:
        return
    
    a = domain_.account.Account(user_login) #创建一个账号的对象 进行初始化 将登录信息传入进行初始化
    a.set_server_tongzhi(data['server酱'])  #设置server酱的key
    a.set_config_user_name(name)    #设置当前用户的自定用户名

    account_huodong = http_.request.request.get_activit(user_login['data']) #获取活动id 活动名称 活动状态
    if account_huodong == None:
        return

    huodong = os_.iostream.iostream.huodong_ini(account_huodong, user_login) #获取可报名的活动列表
    if huodong != []:
        a.add_account_huodong_msg(data['account_huodong_msg'])  #添加报名过的活动信息给账号
        a.add_account_huodong_msg(huodong) #将活动添加进去
        
        baoming(a, name)    #开始报名
        account_list.append(a)  #将账号添加到list中去

def do_main(a):
    tmp = a # 备份一个账号副本
    user_login = util_.login.Login.login(user=a.get_user(), password=a.get_password()) #登录    
    if user_login == None:
        return
    
    a.set_token(user_login['data']['token']) #更新token
    a.set_account_xinxi(user_login['data']) #更新登录信息
    
    account_huodong = http_.request.request.get_activit(user_login['data']) #获取活动id 活动名称 活动状态
    if account_huodong == None:
        return

    huodong = os_.iostream.iostream.huodong_ini(account_huodong, user_login) #获取可报名的活动列表
    
    if huodong != []:
        a.add_account_huodong_msg(huodong)#将活动添加进去
        #开始报名
        baoming(a, a.get_config_user_name())

        #将list中的账号更新
        account_list.remove(tmp)   
        account_list.append(a)


if __name__ == '__main__':
    data = os_.iostream.iostream.get_account() #获取账号信息
    if data != None:

        for i in data: #遍历每个用户 
            a_data = json.loads(data[i])
            out_log.out_txt(log_file, "目前用户：{}：".format(i))
            main(a_data, i)
        for i in account_list:
            out_log.out_txt(log_file, "{}   user:{}".format(datetime.datetime.now(), domain_.account.Account.get_user(i)))
        
        sleep_time = 30 * 60  #运行间隔
        while True:
            time.sleep(sleep_time)

            for i in account_list:
                out_log.out_txt(log_file, "目前用户：{}：".format(i.get_config_user_name()))
                do_main(i)
            for i in account_list:
                out_log.out_txt(log_file, "{}   user:{}".format(datetime.datetime.now(), domain_.account.Account.get_user(i)))
            #每隔多久运行一次
    else:
        print("未检测到用户配置")

    