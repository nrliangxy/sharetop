import requests
from random import choice
from sharetop.crawl.settings import *


class BaseRequest:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, url, data, user_agent=False, headers=None, *args, **kwargs):
        if user_agent:
            headers = {
                'User-Agent': choice(user_agent_list)
            }
        try:
            return requests.get(url, data, headers=headers)
        except:
            raise "request error and contact author"

    def post(self, url, data, user_agent=False, headers=None, *args, **kwargs):
        if user_agent:
            headers = {
                'User-Agent': choice(user_agent_list)
            }
        try:
            return requests.post(url, data, headers=headers)
        except:
            raise "request error and contact author"

