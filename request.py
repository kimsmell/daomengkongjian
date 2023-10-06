import requests
import json
import login

d_version = '4.5.6'
	
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


	def post_baoming(passwd, id):
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
		return response1

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
		# 获取活动时间

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

	def apply(user, password):
		"""
		账号登陆,返回uid和token
		account  登陆账号
		pwd      加密后的密码
		:param account:
		:param pwd:
		:return:
		"""
		a_password = login.Login.get_pwd(password)
		url = 'https://appdmkj.5idream.net/v2/login/phone'
		data = {
			'pwd': a_password,
			'account': user,
			'version': d_version
		}

		response = requests.post(url=url, headers=headers, data=data).json()
		response.update(account=user, pwd=password)
		# response1 = json.dumps(response)
		# with open('token', mode='w', encoding='utf-8') as f:
		# 	f.write(response1)

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