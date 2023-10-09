import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import a_stock_list_url
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *


class StockServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def common_func(self, params, item_url):
        is_explain = params.pop("is_explain", False)
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append(item_url)
        headers = {"token": self.token}
        r = requests_obj.get("".join(copy_base_url_list), data=params, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_kline_data(self, **kwargs):
        return self.common_func(kwargs, a_stock_list_url)

    def stock_to_trade_date_list(self, **kwargs):
        pass
