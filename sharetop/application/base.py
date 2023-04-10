from typing import Any, Callable, Dict, List, TypeVar, Union
from jsonpath import jsonpath
import pandas as pd


class BaseApplication:
    def __init__(self, json_data, *args, **kwargs):
        self.json_data = json_data

    def parse_json(self, json_par='$..klines[:]'):
        json_r: List[str] = jsonpath(self.json_data, json_par)
        return json_r

    def deal_k_data(self, columns, quote_id):
        k_lines = self.parse_json()
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

