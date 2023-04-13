import traceback
import gevent
from datetime import datetime
from gevent.pool import Pool
import pandas as pd
from .config import (EM_KLINE_FIELDS,
                     MagicConfig,
                     EASTMONEY_REQUEST_HEADERS,
                     EM_REAL_TIME_FIELDS_PARAMS,
                     EM_REAL_TIME_FIELDS,
                     EASTMONEY_QUOTE_FIELDS,
                     MARKET_NUMBER_DICT
                     )
from ..utils import get_quote_id, to_numeric, requests_obj
from typing import Any, Callable, Dict, List, TypeVar, Union
from ...application import BaseApplication
from ...crawl.settings import *


@to_numeric
def get_market_realtime_by_fs(fs: str, **kwargs) -> pd.DataFrame:
    """
    获取沪深市场最新行情总体情况

    Returns
    -------
    DataFrame
        沪深市场最新行情信息（涨跌幅、换手率等信息）

    """
    columns = {**EASTMONEY_QUOTE_FIELDS, **kwargs.get(MagicConfig.EXTRA_FIELDS, {})}
    fields = ",".join(columns.keys())
    params = (
        ('pn', '1'),
        ('pz', '1000000'),
        ('po', '1'),
        ('np', '1'),
        ('fltt', '2'),
        ('invt', '2'),
        ('fid', 'f3'),
        ('fs', fs),
        ('fields', fields),
    )
    url = ''.join(market_real_time_url_list)
    json_response = requests_obj.get(
        url, params, user_agent=False
    ).json()
    df = pd.DataFrame(json_response['data']['diff'])
    df = df.rename(columns=columns)
    df: pd.DataFrame = df[columns.values()]
    df['行情ID'] = df['市场编号'].astype(str) + '.' + df['代码'].astype(str)
    df['市场类型'] = df['市场编号'].astype(str).apply(lambda x: MARKET_NUMBER_DICT.get(x))
    df['更新时间'] = df['更新时间戳'].apply(lambda x: str(datetime.fromtimestamp(x)))
    df['最新交易日'] = pd.to_datetime(df['最新交易日'], format='%Y%m%d').astype(str)
    tmp = df['最新交易日']
    del df['最新交易日']
    df['最新交易日'] = tmp
    del df['更新时间戳']
    return df


def quote_id_process(params, quote_id):
    quote_id_key = ''.join(quote_id_key_list)
    params.update(
        {quote_id_key: quote_id}
    )
    return params


def get_real_time(
        stock_codes: Union[str, List[str]],
        **kwargs
):
    if isinstance(stock_codes, str):
        return get_real_time_data_one(stock_codes)
    elif hasattr(stock_codes, '__iter__'):
        codes = list(stock_codes)
        return get_quote_multi(
            codes, **kwargs
        )
    raise TypeError('代码数据类型输入不正确！')


@to_numeric
def get_real_time_data_one(
        code: str,
        **kwargs
) -> pd.DataFrame:
    """
        获取单只股票、债券 实时的基本数据
    """
    columns = list(EM_REAL_TIME_FIELDS.values())
    quote_id = get_quote_id(code)
    params = {
        "fields": EM_REAL_TIME_FIELDS_PARAMS
    }
    params = quote_id_process(params, quote_id)
    url = ''.join(real_time_url_list)
    json_response = requests_obj.get(
        url, params, user_agent=False
    ).json()
    application_obj = BaseApplication(json_response)
    return application_obj.deal_real_time_data(columns, EM_REAL_TIME_FIELDS)


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
        return get_quote_multi(
            codes, beg=beg, end=end, klt=klt, fqt=fqt, **kwargs
        )
    raise TypeError('代码数据类型输入不正确！')


def get_quote_multi(
        codes: List[str],
        beg: str = '19000101',
        end: str = '20500101',
        klt: int = 101,
        fqt: int = 1,
        tries: int = 3,
        **kwargs,
) -> Dict[str, pd.DataFrame]:
    """
    获取多只股票、债券历史行情信息 或者实时行情
    """
    s = traceback.extract_stack()
    base_func_name = s[-2][2]
    total = len(codes)
    pool = Pool(total)
    func = globals()[f"{base_func_name}_data_one"]
    coroutine_list = [pool.spawn(func, x, beg=beg, end=end, klt=klt, fqt=fqt) for x in codes]
    gevent.joinall(coroutine_list)
    df_value = [_.value for _ in coroutine_list]
    dfs = dict(zip(codes, df_value))
    return dfs
