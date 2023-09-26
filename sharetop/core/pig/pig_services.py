import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import pig_warning_url, pig_fcr_url
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *
from sharetop.core.stock import get_stock_kline_data


class PigServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def pig_to_warning_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        return exchange_explain_new(self._common(pig_warning_url, kwargs), is_explain)

    def pig_to_fcr_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        return exchange_explain_new(self._common(pig_fcr_url, kwargs), is_explain)

    def _common(self, sub_url, item):
        pig_base_url_list = copy.deepcopy(base_url_list)
        pig_base_url_list.append(sub_url)
        headers = {"token": self.token}
        r = requests_obj.get("".join(pig_base_url_list), data=item, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        df = pd.DataFrame(data_json['data'])
        return df

    def pig_to_index(self, **kwargs):
        is_explain = kwargs.get("is_explain", False)
        params = {'is_explain': is_explain, "stock_codes": "BK0882", "token": self.token}
        return get_stock_kline_data(**params)
