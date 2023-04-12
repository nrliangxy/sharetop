import multitasking
import gevent
from gevent.pool import Pool
import pandas as pd
from .config import EM_KLINE_FIELDS, MagicConfig, EASTMONEY_REQUEST_HEADERS, EM_REAL_TIME_FIELDS_PARAMS, EM_REAL_TIME_FIELDS
from ..utils import get_quote_id, to_numeric, requests_obj
from typing import Any, Callable, Dict, List, TypeVar, Union
from retry import retry
from tqdm import tqdm
from ...application import BaseApplication
from ...crawl.settings import *


def quote_id_process(params, quote_id):
    quote_id_key = ''.join(quote_id_key_list)
    params.update(
        {quote_id_key: quote_id}
    )
    return params


def get_real_time(
        stock_codes: Union[str, List[str]],
):
    if isinstance(stock_codes, str):
        return get_real_time_data_one(stock_codes)
    raise TypeError('代码数据类型输入不正确！')


def get_real_time_data_one(
        code: str
) -> pd.DataFrame:
    fields = list(EM_REAL_TIME_FIELDS.keys())
    columns = list(EM_REAL_TIME_FIELDS.values())
    quote_id = get_quote_id(code)
    params = {
        "fields": EM_REAL_TIME_FIELDS_PARAMS
    }
    params = quote_id_process(params, quote_id)
    url = ''.join(real_time_url_list)
    print("url:", url)
    print("params:", params)
    json_response = requests_obj.get(
        url, params, user_agent=False
    ).json()
    application_obj = BaseApplication(json_response)
    return application_obj.deal_real_time_data(columns, quote_id, EM_REAL_TIME_FIELDS)


@to_numeric
def get_history_data_one(
        code: str,
        beg: str = '19000101',
        end: str = '20500101',
        klt: int = 101,
        fqt: int = 1,
        **kwargs,
) -> pd.DataFrame:
    """
    获取单只股票、债券 K 线数据
    """
    fields = list(EM_KLINE_FIELDS.keys())
    columns = list(EM_KLINE_FIELDS.values())
    fields2 = ",".join(fields)
    if kwargs.get(MagicConfig.QUOTE_ID_MODE):
        quote_id = code
    else:
        quote_id = get_quote_id(code)
    params = {
        'fields1': ','.join(fields1_list),
        'fields2': fields2,
        'beg': beg,
        'end': end,
        'rtntype': '6',
        'klt': f'{klt}',
        'fqt': f'{fqt}',
    }
    params = quote_id_process(params, quote_id)
    url = ''.join(k_url_list)
    json_response = requests_obj.get(
        url, params, user_agent=True
    ).json()
    application_obj = BaseApplication(json_response)
    return application_obj.deal_k_data(columns, quote_id)


def get_history(
        codes: Union[str, List[str]],
        beg: str = '19000101',
        end: str = '20500101',
        klt: int = 101,
        fqt: int = 1,
        **kwargs,
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    获取股票、ETF、债券的 K 线数据

    Parameters
    ----------
    codes : Union[str,List[str]]
        股票、债券代码 或者 代码构成的列表
    beg : str, optional
        开始日期，默认为 ``'19000101'`` ，表示 1900年1月1日
    end : str, optional
        结束日期，默认为 ``'20500101'`` ，表示 2050年1月1日
    klt : int, optional
        行情之间的时间间隔，默认为 ``101`` ，可选示例如下

        - ``1`` : 分钟
        - ``5`` : 5 分钟
        - ``15`` : 15 分钟
        - ``30`` : 30 分钟
        - ``60`` : 60 分钟
        - ``101`` : 日
        - ``102`` : 周
        - ``103`` : 月

    fqt : int, optional
        复权方式，默认为 ``1`` ，可选示例如下

        - ``0`` : 不复权
        - ``1`` : 前复权
        - ``2`` : 后复权

    Returns
    -------
    Union[DataFrame, Dict[str, DataFrame]]
        股票、债券的 K 线数据

        - ``DataFrame`` : 当 ``codes`` 是 ``str`` 时
        - ``Dict[str, DataFrame]`` : 当 ``codes`` 是 ``List[str]`` 时

    """

    if isinstance(codes, str):
        return get_history_data_one(
            codes, beg=beg, end=end, klt=klt, fqt=fqt, **kwargs
        )

    elif hasattr(codes, '__iter__'):
        codes = list(codes)
        return get_quote_history_multi(
            codes, beg=beg, end=end, klt=klt, fqt=fqt, **kwargs
        )
    raise TypeError('代码数据类型输入不正确！')


def get_quote_history_multi(
        codes: List[str],
        beg: str = '19000101',
        end: str = '20500101',
        klt: int = 101,
        fqt: int = 1,
        tries: int = 3,
        **kwargs,
) -> Dict[str, pd.DataFrame]:
    """
    获取多只股票、债券历史行情信息
    """
    total = len(codes)
    pool = Pool(total)
    coroutine_list = [pool.spawn(get_history_data_one, x, beg=beg, end=end, klt=klt, fqt=fqt) for x in codes]
    gevent.joinall(coroutine_list)
    df_value = [_.value for _ in coroutine_list]
    dfs = dict(zip(codes, df_value))
    return dfs
