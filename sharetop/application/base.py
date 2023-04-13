import pandas as pd
import math
from typing import Any, Callable, Dict, List, TypeVar, Union
from jsonpath import jsonpath


class BaseApplication:
    def __init__(self, json_data, *args, **kwargs):
        self.json_data = json_data

    def parse_json(self, json_par):
        json_r: List[str] = jsonpath(self.json_data, json_par)
        return json_r

    def deal_k_data(self, columns, quote_id, json_par='$..klines[:]'):
        k_lines = self.parse_json(json_par)
        if not k_lines:
            columns.insert(0, '代码')
            columns.insert(0, '名称')
            return pd.DataFrame(columns=columns)
        rows = [kline.split(',') for kline in k_lines]
        name = self.json_data['data']['name']
        code = quote_id.split('.')[-1]
        df = pd.DataFrame(rows, columns=columns)
        df.insert(0, '代码', code)
        df.insert(0, '名称', name)
        return df

    def deal_fields(self, data, fields_list):
        f59 = data['f59']
        for _ in fields_list:
            item = data[_] / math.pow(10, f59)
            data[_] = item
        return data

    def deal_real_time_data(self, columns, fields_k_v):
        data = self.json_data['data']
        if not data:
            columns.insert(0, '代码')
            columns.insert(0, '名称')
            return pd.DataFrame(columns=columns)
        deal_fields_list = ["f43", "f169", "f44", "f45", "f46", "f60", "f71", "f164", "f167", "f169", "f170", "f171"]
        data = self.deal_fields(data, deal_fields_list)
        r = {v: data[k] for k, v in fields_k_v.items() if data.get(k)}
        return pd.DataFrame([r])
