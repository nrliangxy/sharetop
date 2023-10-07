import datetime
import copy
import pandas as pd
from ..utils import requests_obj
<<<<<<< HEAD
from .config import a_stock_list_url
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *

=======
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

>>>>>>> d0c315827eaf6d41c45e1747a71879a6a5b08bcb

class StockServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

<<<<<<< HEAD
    def stock_to_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append(a_stock_list_url)
=======
    def a_stock_to_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append(car_sales_url)
>>>>>>> d0c315827eaf6d41c45e1747a71879a6a5b08bcb
        headers = {"token": self.token}
        r = requests_obj.get("".join(copy_base_url_list), data=kwargs, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
<<<<<<< HEAD
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json
=======
        for item in data_json.get('data', []):
            item['car_type'] = car_type_list.get(item['car_type'], item['car_type'])
            item['source'] = source_list.get(item['source'], item['source'])
        df = pd.DataFrame(data_json['data'])
        return exchange_explain_new(df, is_explain)
>>>>>>> d0c315827eaf6d41c45e1747a71879a6a5b08bcb
