import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import car_sales_url, car_sales_field_dict
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *

car_type_list = {
    "1": "轿车",
    "2": "suv",
    "3": "mpv"
}

source_list = {
    "1": "太平洋汽车",
    "2": "懂车帝"
}


class CarServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def car_to_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append(car_sales_url)
        headers = {"token": self.token}
        r = requests_obj.get("".join(copy_base_url_list), data=kwargs, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        for item in data_json.get('data', []):
            item['car_type'] = car_type_list.get(item['car_type'], item['car_type'])
            item['source'] = source_list.get(item['source'], item['source'])
        df = pd.DataFrame(data_json['data'])
        return exchange_explain_new(df, is_explain)
