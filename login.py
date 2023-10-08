# coding=utf-8
import request
from pyDes import des, ECB, PAD_PKCS5
import binascii

class Login:
    
    def login(user, password):
        return request.request.apply(user=user, password=password)
    
    #密码加密
    def get_pwd(s):
        
        KEY = '51434574'
        secret_key = KEY
        k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return binascii.b2a_hex(en).upper().decode('utf-8')