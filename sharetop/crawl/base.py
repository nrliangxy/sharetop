import requests
from random import choice
from sharetop.crawl.settings import *

class CustomException(BaseException):
    pass

class BaseRequest:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, url, data, user_agent=False, headers=None, *args, **kwargs):
        if user_agent:
            headers = {
                'User-Agent': choice(user_agent_list)
            }
        try:
            if headers.get("token"):
                if len(headers.get("token")) != 16:
                    return {"msg": "token有误，请先确认token是否正确"}
            r = requests.get(url, data, headers=headers)
            r_code = r.status_code
            if r_code == 401:
                return {"msg": "您还没有权限，请先开通权限"}
            return r
        except:
            raise CustomException("request error and contact author")

    def post(self, url, data, user_agent=False, headers=None, *args, **kwargs):
        if user_agent:
            headers = {
                'User-Agent': choice(user_agent_list)
            }
        try:
            return requests.post(url, data, headers=headers)
        except:
            raise "request error and contact author"

