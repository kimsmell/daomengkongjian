from models.db import db


class config:
    # 配置文件路径
    config_file = 'data/config.json'

    # log文件路径
    log_file = "./log/log.log"

    # log文件最大大小
    log_file_max_size = 1 * 1024 * 512

    # 错误信息路径
    err_file = "./log/err.log"

    # 错误信息文件最大大小
    err_file_max_size = 1 * 1024 * 512

    # app版本号
    d_version = '4.6.0'

    # 运行间隔 秒
    sleep_time = 2 * 60 * 60

    # 是否只报名线上
    online = True

    mysql = db()

    headers = {
        'standardUA': '{"uuid":"d0824ff00c104312acb3e91f0f6c1b89","system":"iOS","version":"4.5.8","sysVersion":"15.6","screenResolution":"1242.000000-2688.000000","JPushId":"d0824ff00c104312acb3e91f0f6c1b89","countryCode":"CN","channelName":"dmkj_iOS","createTime":"0","operator":"%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8460660","modifyTime":"0","device":"iPhone 13 Pro Max","hardware":"D64AP,iPhone14,3,arm64,255877271552,1604567040","startTime":"1695387433"}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Cookie': 'acw_tc=2f624a5016958158420312945e34eae2f925c163d6ad7b4cb28af85273fbeb',
        'Content-Length': '526',
        'Accept-Language': 'zh-Hans-CN;q=1, fr-CA;q=0.9, en-CN;q=0.8',
        'Host': 'appdmkj.5idream.net',
        'Connection': 'keep-Alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'DMKJ/4.5.8 (iPhone; iOS 15.6; Scale/3.00)',

    }