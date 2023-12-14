import datetime
import copy
import pandas as pd
from ..utils import requests_obj
from .config import a_stock_list_url, a_stock_trade_date_url, a_stock_index_url, \
    stock_intl_index_url, index_stock_composition_url, stock_bonus_url, stock_repurchase_url
from ..common.explain_change import exchange_explain_new
from ...crawl.settings import *


class StockServices:
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

    def stock_to_kline_data(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, a_stock_list_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_trade_date_list(self, **kwargs):
        """
        交易日历数据
        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, a_stock_trade_date_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_index_list(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, a_stock_index_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_intl_index_list(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, stock_intl_index_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_index_stock_composition(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, index_stock_composition_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_stock_bonus(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, stock_bonus_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json

    def stock_to_stock_repurchase(self, **kwargs):
        is_explain = kwargs.pop("is_explain", False)
        data_json = self.common_func(kwargs, stock_repurchase_url)
        if data_json['data'] and isinstance(data_json['data'], list):
            df = pd.DataFrame(data_json['data'])
            return exchange_explain_new(df, is_explain)
        else:
            return data_json
