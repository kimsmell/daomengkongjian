# coding=utf-8
import os
import json
import http_.request
import os_.out_log
import datetime

out_log = os_.out_log.out_log()
log_file = out_log.get_log_file()
err_file = out_log.get_err_file()

config_file = './config.json'
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
		except :
			out_log.out_txt(err_file, "{}: 配置文件错误".format(datetime.datetime.now()))
		
		return data_s

	#更新account.ini
	def out_account_ini(datas):
		if os.path.exists(config_file):
			with open(config_file, mode='w', encoding='utf-8') as f:
				f.write(json.dumps(datas))

	#更新读取后 指定name中的数据 
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

	#获取account_huodong_msg
	def huodong_ini(huodong, passwd):
		list = []
		for i in huodong: #活动id 活动名称 活动状态
			activityId = i['activityId'] #活动id
			data = http_.request.request.get_huodong_xiangxi(passwd['data'], activityId) #获取活动详细信息
			if data == None:
				return list
			
			try:
				if data['data']['statusText'] == '报名中':
					activityName = data['data']['activityName'] #活动名称
					address = data['data']['address'] #活动地址
					unableJoinReason = data['data']['countdownText'] #结束倒计时  如果报名人数已满 那么会显示报名人数已满否则显示倒计时
					isbaoming = 0 #是否报名过
					list.append([activityId, activityName, address, unableJoinReason, isbaoming])
			except :
				out_log.out_txt(err_file, "{}: 活动信息错误：{}".format(datetime.datetime.now(), data))
		
		return list
	