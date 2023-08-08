import traceback
import gevent
from gevent.pool import Pool
import pandas as pd
from jsonpath import jsonpath
from .config import (EM_KLINE_FIELDS,
                     MagicConfig,
                     EASTMONEY_REQUEST_HEADERS,
                     EM_REAL_TIME_FIELDS_PARAMS,
                     EM_REAL_TIME_FIELDS,
                     EASTMONEY_QUOTE_FIELDS,
                     QUARTERLY_DICT,
                     EASTMONEY_HISTORY_BILL_FIELDS
                     )
from ..utils import get_quote_id, to_numeric, requests_obj
from typing import Dict, List, Union
from ...application import BaseApplication
from ...crawl.settings import *
from .config import EASTMONEY_BASE_INFO_FIELDS, BASE_INFO_CACHE


@to_numeric
def get_real_time_bill_data_one(code: str) -> pd.DataFrame:
    """
    获取单只股票最新交易日的日内分钟级单子流入流出数据
    Parameters
    ----------
    code : str
        股票、债券代码

    Returns
    -------
    DataFrame
        单只股票、债券最新交易日的日内分钟级单子流入流出数据
    """
    quote_id = get_quote_id(code)
    params = (
        ('lmt', '0'),
        ('klt', '1'),
        ('secid', quote_id),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63'),
    )
    url = 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get'
    json_response = requests_obj.get(url, params).json()
    columns = ['时间', '主力净流入', '小单净流入', '中单净流入', '大单净流入', '超大单净流入']
    name = jsonpath(json_response, '$..name')[0]
    code = quote_id.split('.')[-1]
    klines: List[str] = jsonpath(json_response, '$..klines[:]')
    if not klines:
        columns.insert(0, '股票代码')
        columns.insert(0, '股票名称')
        return pd.DataFrame(columns=columns)
    rows = [kline.split(',') for kline in klines]
    df = pd.DataFrame(rows, columns=columns)
    df.insert(0, '股票代码', code)
    df.insert(0, '股票名称', name)
    return df


@to_numeric
def get_history_bill(code: str) -> pd.DataFrame:
    """
    获取单支股票、债券的历史单子流入流出数据

    Parameters
    ----------
    code : str
        股票、债券代码

    Returns
    -------
    DataFrame
        沪深市场单只股票、债券历史单子流入流出数据

    """
    fields = list(EASTMONEY_HISTORY_BILL_FIELDS.keys())
    columns = list(EASTMONEY_HISTORY_BILL_FIELDS.values())
    fields2 = ",".join(fields)
    quote_id = get_quote_id(code)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', quote_id),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),
    )
    json_response = requests_obj.get("".join(bill_url_list), params).json()
    application_obj = BaseApplication(json_response)
    return application_obj.deal_bill(columns, quote_id)


@to_numeric
def get_company_report_data_one(code: str, report_class: str = None, **kwargs) -> pd.DataFrame:
    columns = QUARTERLY_DICT
    params = {
        'sortColumns': 'REPORTDATE',
        'sortTypes': '-1',
        'pageSize': '200',
        'columns': 'ALL',
        'filter': f'(SECURITY_CODE={code})(DATEMMDD="{report_class}")' if report_class else f'(SECURITY_CODE={code})',
        'reportName': 'RPT_LICO_FN_CPD',
    }
    json_response = requests_obj.get(
        ''.join(one_quarterly_report_url_list), params, user_agent=False
    ).json()
    application_obj = BaseApplication(json_response)
    return application_obj.deal_quarterly_report(columns)


def get_company_report(stock_codes: Union[str, List[str]],
                       report_class: str = None, **kwargs):
    if isinstance(stock_codes, str):
        return get_company_report_data_one(stock_codes, report_class)
    elif hasattr(stock_codes, '__iter__'):
        codes = list(stock_codes)
        return get_quote_multi(
            codes, report_class=report_class, **kwargs
        )
    raise TypeError('代码数据类型输入不正确！')


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
    application_obj = BaseApplication(json_response)
    return application_obj.deal_market_realtime(columns)


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
        report_class: str = None,
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
    print("base_func_name========:", base_func_name)
    print("report_class===============:", report_class)
    func = globals()[f"{base_func_name}_data_one"]
    coroutine_list = [pool.spawn(func, x, beg=beg, end=end, klt=klt, fqt=fqt, report_class=report_class, **kwargs) for x
                      in codes]
    gevent.joinall(coroutine_list)
    df_value = [_.value for _ in coroutine_list]
    dfs = dict(zip(codes, df_value))
    return dfs


@to_numeric
def get_base_info(quote_id: str) -> pd.Series:
    fields = ",".join(EASTMONEY_BASE_INFO_FIELDS.keys())
    params = (
        ('ut', 'fa5fd1943c7b386f172d6893dbfba10b'),
        ('invt', '2'),
        ('fltt', '2'),
        ('fields', fields),
        ('secid', quote_id),
    )
    url = 'http://push2.eastmoney.com/api/qt/stock/get'
    json_response = requests_obj.get(url, params, headers=EASTMONEY_REQUEST_HEADERS).json()
    items = json_response['data']
    if not items:
        return pd.Series(index=EASTMONEY_BASE_INFO_FIELDS.values(), dtype='object')
    s = pd.Series(items, dtype='object').rename(index=EASTMONEY_BASE_INFO_FIELDS)
    return s


@to_numeric
def get_deal_detail(quote_id: str, max_count: int = 1000000) -> pd.DataFrame:
    """
    获取股票、期货、债券的最新交易日成交情况
    Parameters
    ----------
    quote_id : str
        包含市场编号的股票、期货、债券代码
    max_count : int, optional
        最大数据条数, 默认为 ``1000000``
    Returns
    -------
    DataFrame
        股票、期货、债券的最新交易日成交情况
    Notes
    ------
    返回的数据表头: ``['名称', '代码', '时间', '昨收', '成交价', '成交量', '单数']``
    """
    base_info = BASE_INFO_CACHE.get(quote_id, get_base_info(quote_id))
    BASE_INFO_CACHE[quote_id] = base_info
    columns = ['名称', '代码', '时间', '昨收', '成交价', '成交量', '单数']
    if str(base_info['代码']).lower() == 'nan':
        return pd.DataFrame(columns=columns)
    code = base_info['代码']
    name = base_info['名称']
    params = (
        ('secid', quote_id),
        ('fields1', 'f1,f2,f3,f4,f5'),
        ('fields2', 'f51,f52,f53,f54,f55'),
        ('pos', f'-{int(max_count)}'),
    )
    url = 'https://push2.eastmoney.com/api/qt/stock/details/get'
    json_response = requests_obj.get(url, params).json()
    # print("json_response==================:", json_response)
    lines: List[str] = json_response['data']['details']
    rows = [line.split(',')[:4] for line in lines]
    df = pd.DataFrame(columns=columns, index=range(len(rows)))
    df.loc[:, '代码'] = code
    df.loc[:, '名称'] = name
    detail_df = pd.DataFrame(rows, columns=['时间', '成交价', '成交量', '单数'])
    detail_df.insert(1, '昨收', json_response['data']['prePrice'])
    df.loc[:, detail_df.columns] = detail_df.values
    return df
