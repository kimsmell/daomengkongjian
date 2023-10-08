# 到梦空间自动报名:

liunx服务器可进行全自动账号托管报名 



#### 实现功能

- 多用户报名活动
- 自动登录账号
- 自动获取活动
- 循环检测活动 进行自动报名 可自定义检测间隔
- 活动只会报名一次 不会重复报名



#### 运行方式（配置文件路径必须要与main.py相同）

- win
  - 安装 pyDes requests 第三方库
  - 到当前目录运行main.exe或者到当前目录cmd运行 python main.py
- liunx
  - 安装 pyDes requests 第三方库
  - cd至当前目录 python main.py

`运行时间可以在main.py中79行进行修改 默认是30分钟`



#### 多用户报名配置文件：config.json

```json
{
    //name为当前用户的自己命名（必填 不可重复）
    "用户1":'{	
        "user":"",	//登录的账号（必填）
        "password":"",	//登录账号的密码（必填）
        "token":"",	//用户的token 登录后自动填充 写入（可以不填）
        "account_huodong_msg":"",	//用于保存的报名信息 登录成功 并且报名成功后会自动写入（不填）
        "server酱":""	//server酱 用于通知 发送推送（具体获取key自行百度）
    }'
	//不需要多账号 可以删除以下配置
	,"用户2":'{
        "user":"",
        "password":"",
        "token":"",
        "account_huodong_msg":"",
        "server酱":""
    }'
}
```

