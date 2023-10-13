# coding=utf-8
from utils.login import Login
from utils.out_log import out_log
from config import config

import requests
import json


d_version = config.d_version
log_file = 1
err_file = 2
headers = config.headers

class Request:

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
		except Exception as e:
			out_log().out_txt(err_file, '获取活动的请求失败！\n{}'.format(e))
		
		try:
			lists_data = response['data']['list']
		except Exception as e:
			out_log().out_txt(err_file, "获取活动列表的key异常：{}\n{}".format(response, e))
		
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
		except Exception as e:
			out_log().out_txt(err_file, "报名的请求失败！\n{}".format(e))
		
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
		except Exception as e:
			out_log().out_txt(err_file, "获取活动时间的请求失败！\n{}".format(e))

		return huodong

	#登录账号
	def apply(user, password):

		a_password = Login.get_pwd(password)	#获取加密后的密码
		url = 'https://appdmkj.5idream.net/v2/login/phone'
		data = {
			'pwd': a_password,	#加密后的密码
			'account': user,	#登录账号
			'version': d_version	#版本号
		}

		response = None
		try:
			response = requests.post(url=url, headers=headers, data=data).json()	#发送登录的请求
			response.update(account=user, pwd=password)	#更新账号以及密码
		except Exception as e:
			out_log().out_txt(err_file, "登录账号的请求失败！\n{}".format(e))
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