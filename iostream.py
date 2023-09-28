import os
import json
import request
config_file = 'config.ini'
class iostream:
	


	# 解析account.ini文件
	def get_account():

		if os.path.exists(config_file):
			with open(config_file, mode='r', encoding='utf-8') as f:
				datas = f.readlines()
				s = ''
				for i in datas:
					s += i.replace('\n', '').replace(' ', '')
				data_s = eval(s)
		return data_s

	#更新account.ini
	def out_account_ini(datas):
		if os.path.exists(config_file):
			with open(config_file, mode='w', encoding='utf-8') as f:
				f.write(json.dumps(datas))

	#更新读取后 指定name中的数据 
	def updata_ini(user, password, token, account_huodong_msg, name):
		data = iostream.get_account()
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
			data = request.request.get_huodong_xiangxi(passwd['data'], activityId) #获取活动详细信息
		
			activityName = data['data']['activityName'] #活动名称
			address = data['data']['address'] #活动地址
			unableJoinReason = data['data']['countdownText'] #结束倒计时  如果报名人数已满 那么会显示报名人数已满否则显示倒计时
			isbaoming = 'false' #是否报名过
			list.append([activityId, activityName, address, unableJoinReason, isbaoming])
		return list
	
