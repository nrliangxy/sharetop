import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import news_normal_url
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *


class NewsServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def common_func(self, params, item_url):
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append(item_url)
        headers = {"token": self.token}
        r = requests_obj.get("".join(copy_base_url_list), data=params, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        return data_json

    def news_to_normal(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, news_normal_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json
