import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import url, bond_yield_url, headers
from ..common.explain_change import exchange_explain, exchange_explain_new
from ...crawl.settings import *


class BondYieldServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.__url = url
        self.__headers = headers

    def bond_yield_to_real_time(self, **kwargs):
        is_explain = kwargs.get("is_explain", False)
        bond_name = kwargs.get("bond_name")
        bond_url = self.__url.format(bond_name=bond_name)
        r = requests_obj.get(bond_url, data={}, headers=self.__headers)
        data = r.text
        data = data.replace(f'var hq_str_globalbd_{bond_name}="', "").replace('";', "")
        data_list = data.split(",")
        bond_name = data_list[0]
        open_price = data_list[1]
        previous_close = data_list[2]
        now_price = data_list[3]
        high_price = data_list[4]
        low_price = data_list[5]
        percentage_change = float(data_list[7]) * 100
        price_change = data_list[8]
        update_time = datetime.datetime.fromtimestamp(int(data_list[11]))
        item = {"bond_name": bond_name, "open_price": open_price, "previous_close": previous_close,
                "now_price": now_price,
                "high_price": high_price, "low_price": low_price,
                "percentage_change": percentage_change, "price_change": price_change, "update_time": update_time}
        df = pd.DataFrame([item])
        return exchange_explain_new(df, is_explain)

    def bond_yield_to_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        bond_yield_base_url_list = copy.deepcopy(base_url_list)
        bond_yield_base_url_list.append(bond_yield_url)
        headers = {"token": self.token}
        r = requests_obj.get("".join(bond_yield_base_url_list), data=kwargs, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        df = pd.DataFrame(data_json['data'])
        return exchange_explain_new(df, is_explain)
