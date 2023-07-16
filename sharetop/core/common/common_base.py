import gevent
import pandas as pd
from typing import Dict, List, Union
from gevent.pool import Pool
from ...crawl.settings import *
from ..utils import get_quote_id, requests_obj, parse_obj, to_numeric
from .config import *


class CommonFunc:
    def __int__(self):
        pass

    def get_common_func(self, stock_codes: Union[str, List[str]], single_func, **kwargs):
        if isinstance(stock_codes, str):
            return getattr(DataOne, f"{single_func}_data_one")(stock_codes, **kwargs)
        elif hasattr(stock_codes, '__iter__'):
            codes = list(stock_codes)
            return self.get_quote_multi_new(
                codes, single_func=single_func, **kwargs
            )
        raise TypeError('代码数据类型输入不正确！')

    def get_quote_multi_new(self,
                            codes: List[str],
                            beg: str = '19000101',
                            end: str = '20500101',
                            klt: int = 101,
                            fqt: int = 1,
                            report_class: str = None,
                            single_func: str = None,
                            **kwargs,
                            ) -> Dict[str, pd.DataFrame]:
        """
        获取多只股票、债券历史行情信息 或者实时行情
        """
        total = len(codes)
        pool = Pool(total)
        func = getattr(DataOne, f"{single_func}_data_one")
        coroutine_list = [pool.spawn(func, x, beg=beg, end=end, klt=klt, fqt=fqt,
                                     report_class=report_class, **kwargs) for x in codes]
        gevent.joinall(coroutine_list)
        df_value = [_.value for _ in coroutine_list]
        dfs = dict(zip(codes, df_value))
        return dfs


class DataOne:
    market_dict = {"1": "sh", "0": "sz", "116": "hk"}

    @staticmethod
    @to_numeric
    def get_stock_base_info_data_one(stock_codes: str, **kwargs) -> pd.DataFrame:
        use_code_id = get_quote_id(stock_codes)
        use_code_list = use_code_id.split(".")
        use_code = '.'.join([use_code_list[1], DataOne.market_dict[use_code_list[0]]])
        url = ''.join(stock_base_info_url)
        data = {"code": use_code}
        json_response = requests_obj.get(url, data).json()
        return parse_obj.parse_stock_base_info(json_response)

    @staticmethod
    @to_numeric
    def get_stock_real_time_sum_capital_data_one(code: str, **kwargs) -> pd.DataFrame:
        quote_id = get_quote_id(code)
        params = (
            ('secids', quote_id),
            ('fields',
             'f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f64,f65,f70,f71,f76,f77,f82,f83,f252,f253,f254,f255,f256,f278,f279,f280,f281,f282'),
        )
        url = ''.join(capital_flow_real_time_url_list)
        json_response = requests_obj.get(url, params).json()
        return parse_obj.parse_capital_flow_json(json_response)

    @staticmethod
    @to_numeric
    def get_stock_real_time_sector_capital_data_one(sector: str, **kwargs) -> pd.DataFrame:
        monitor_time = kwargs.get("monitor_time")
        params_base = {"po": "1", "pz": "500", "pn": "1", "np": "1", "fltt": "2", "invt": "2"}
        params_dict = sector_dict[monitor_time]
        fields_map = params_dict.pop("fields_map")
        drop_field = params_dict.pop("drop_field")
        params_base.update(params_dict)
        params_base.update(sector_dict2[sector])
        url = ''.join(sector_url_list)
        json_response = requests_obj.get(url, params_base).json()
        return parse_obj.parse_capital_flow_json(json_response, field_map=fields_map).drop(axis=1, columns=[drop_field])
