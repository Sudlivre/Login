import requests
from lxml import etree
from config import *


class Login(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        }
        self.url_login = 'https://accounts.douban.com/login?'
        self.source = None
        self.redir = 'https://www.douban.com'
        self.form_email = EMAIL
        self.form_password = PASSWORD
        self.captcha_solution = ''
        self.captcha_id = ''
        self.login = '登录'
        self.session = requests.Session()

    def check_code(self):
        pass