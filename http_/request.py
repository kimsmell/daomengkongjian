# coding=utf-8
import requests
import json
import util_.login
import os_.out_log

d_version = '4.5.6'

out_log = os_.out_log.out_log()
log_file = out_log.get_log_file()
err_file = out_log.get_err_file()

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

class request:

	#获取可报名的活动
	def get_activit(accounts_data):
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

		response = None
		lists_data = None

		try:
			response = requests.post(url=url, headers=headers, data=data).json()
		except :
			out_log.out_txt(err_file, "获取活动的请求失败！")
		
		try:
			lists_data = response['data']['list']
		except :
			out_log.out_txt(err_file, "获取活动列表的key异常：{}".format(response))
		
		if lists_data == None:
			return None

		for data_ in lists_data:
			activityId = data_['activityId']
			name = data_['name']
			statusText = data_['statusText']
			activity = {'activityId': activityId, 'name': name, 'statusText': statusText}
			activitys.append(activity)
		return activitys

	#进行报名
	def post_baoming(passwd, id):
		info = [{"conent": "", "content": "", "fullid": "79857", "key": 1, "notList": "false", "notNull": "false",
					"system": 0,
					"title": "姓名"}]
		data1 = {
			'uid': passwd['uid'],  # 登陆接口获取
			'token': str(passwd['token']),  # 登陆接口获取
			'remark': '',
			'data': str(info),  # 活动报名参数
			'activityId': id,  # 活动ID
			'version': d_version,	#版本号
		}

		response1 = None
		try:
			response1 = requests.post(url='https://appdmkj.5idream.net/v2/signup/submit', data=data1,
										headers=headers).json()
		except :
			out_log.out_txt(err_file, "报名的请求失败！")
		
		return response1

	#获取活动时间
	def get_huodong_xiangxi(accounts_data, id):

		url = 'https://appdmkj.5idream.net/v2/activity/detail'
		token = accounts_data['token']	#获取token
		uid = accounts_data['uid']	#获取uid
		data_get_time = {
			'uid': uid,  # 登陆接口获取
			'token': token,  # 登陆接口获取
			'activityId': int(id),  # 活动ID
			'version': d_version,	#版本号
		}
		huodong = None
		try:
			huodong = requests.post(url=url, headers=headers, data=data_get_time).json()
		except :
			out_log.out_txt(err_file, "获取活动时间的请求失败！")

		return huodong

	#登录账号
	def apply(user, password):

		a_password = util_.login.Login.get_pwd(password)	#获取加密后的密码
		url = 'https://appdmkj.5idream.net/v2/login/phone'
		data = {
			'pwd': a_password,	#加密后的密码
			'account': user,	#登录账号
			'version': d_version	#版本号
		}
		print(a_password)
		response = None
		try:
			response = requests.post(url=url, headers=headers, data=data).json()	#发送登录的请求
			response.update(account=user, pwd=password)	#更新账号以及密码
		except :
			out_log.out_txt(err_file, "登录账号的请求失败！")
		return response
	
	#推送通知
	def server_jiang(title, desp, key):
		if key != '':
			url = 'https://sctapi.ftqq.com/{}.send?'.format(key)
			data = {
				'text': title,
				'desp': desp
			}
			requests.post(url, data)