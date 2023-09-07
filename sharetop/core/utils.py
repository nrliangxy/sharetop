import time
import rich
import json
import re
import copy
from retry.api import retry
from typing import Any, Callable, Dict, List, TypeVar, Union
from .cache import SEARCH_RESULT_DICT
from .config import Quote
from .config import SEARCH_RESULT_CACHE_PATH
import pandas as pd
from functools import wraps
from ..crawl import BaseRequest
from ..parser import BaseParse
from ..crawl.settings import base_url_list


F = TypeVar('F')
requests_obj = BaseRequest()
parse_obj = BaseParse()


def to_numeric(func: F) -> F:
    """
    将 DataFrame 或者 Series 尽可能地转为数字的装饰器
    Parameters
    ----------
    func : Callable
        返回结果为 DataFrame 或者 Series 的函数
    Returns
    -------
    Union[DataFrame, Series]
    """

    ignore = ['股票代码', '基金代码', '代码', '市场类型', '市场编号', '债券代码', '行情ID', '正股代码']

    @wraps(func)
    def run(*args, **kwargs):
        values = func(*args, **kwargs)
        if isinstance(values, pd.DataFrame):
            for column in values.columns:
                if column not in ignore:
                    values[column] = values[column].apply(convert)
        elif isinstance(values, pd.Series):
            for index in values.index:
                if index not in ignore:
                    values[index] = convert(values[index])
        return values

    def convert(o: Union[str, int, float]) -> Union[str, float, int]:
        if not re.findall('\d', str(o)):
            return o
        try:
            if str(o).isalnum():
                o = int(o)
            else:
                o = float(o)
        except:
            pass
        return o

    return run


def validate_request(func):
    def wrapper(*args, **kwargs):
        # 执行校验逻辑，可以是任何你需要的操作
        if len(args) == 0:
            return {"msg": "请填写有效token"}
        token = args[0]
        headers = {"token": token}
        data = {}
        copy_base_url_list = copy.deepcopy(base_url_list)
        copy_base_url_list.append("/a_stock/base_data/detection")
        r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
        if isinstance(r, dict):
            return r
        data_json = r.json()
        msg = data_json['data'].get('msg', "")
        if msg == "success":
            # 执行被装饰的函数
            return func(*args, **kwargs)
        else:
            return {"msg": "校验失败，请确认token是否最新或者稍后再试或者联系管理员"}
    return wrapper




def search_quote_locally(keyword: str) -> Union[Quote, None]:
    """
    在本地里面使用搜索记录进行关键词搜索

    Parameters
    ----------
    keyword : str
        搜索词

    Returns
    -------
    Union[Quote,None]

    """
    q = SEARCH_RESULT_DICT.get(keyword)
    # NOTE 兼容旧版本 给缓存加上最后修改时间
    if q is None or not q.get('last_time'):
        return None
    last_time: float = q['last_time']
    # 缓存过期秒数
    max_ts = 3600 * 24 * 3
    now = time.time()
    # 缓存过期，在线搜索
    if (now - last_time) > max_ts:
        return None
    # NOTE 一定要拷贝 否则改变源对象
    _q = q.copy()
    # NOTE 一定要删除它 否则会构造错误
    del _q['last_time']
    quote = Quote(**_q)
    return quote


def search_quote(
        keyword: str, count: int = 1, use_local: bool = True
) -> Union[Quote, None, List[Quote]]:
    """
    根据关键词搜索以获取证券信息

    Parameters
    ----------
    keyword : str
        搜索词(股票代码、债券代码甚至证券名称都可以)
    count : int, optional
        最多搜索结果数, 默认为 `1`
    use_local : bool, optional
        是否使用本地缓存

    Returns
    -------
    Union[Quote, None, List[Quote]]

    """
    # NOTE 本地仅存储第一个搜索结果
    if use_local and count == 1:
        quote = search_quote_locally(keyword)
        if quote:
            return quote
    url = 'https://searchapi.eastmoney.com/api/suggest/get'
    params = (
        ('input', f'{keyword}'),
        ('type', '14'),
        ('token', 'D43BF722C8E33BDC906FB84D85E326E8'),
        ('count', f'{count}'),
    )
    json_response = requests_obj.get(url, params).json()
    items = json_response['QuotationCodeTable']['Data']
    if items is not None:
        quotes = [Quote(*item.values()) for item in items]
        # NOTE 暂时仅存储第一个搜索结果
        save_search_result(keyword, quotes[:1])
        if count == 1:
            return quotes[0]
        return quotes
    return None


def save_search_result(keyword: str, quotes: List[Quote]):
    """
    存储搜索结果到文件中

    Parameters
    ----------
    keyword : str
        搜索词
    quotes : List[Quote]
        搜索结果
    """
    with open(SEARCH_RESULT_CACHE_PATH, 'w', encoding='utf-8') as f:
        # TODO考虑如何存储多个搜索结果
        for quote in quotes:
            now = time.time()
            d = dict(quote._asdict())
            d['last_time'] = now
            SEARCH_RESULT_DICT[keyword] = d
            break
        json.dump(SEARCH_RESULT_DICT.copy(), f)


@retry(tries=3, delay=1)
def get_quote_id(stock_code: str) -> str:
    """
    生成东方财富股票专用的行情ID

    Parameters
    ----------
    stock_code : str
        证券代码或者证券名称

    Returns
    -------
    str
        东方财富股票专用的 secid
    """
    if len(str(stock_code).strip()) == 0:
        raise Exception('证券代码应为长度不应为 0')
    quote = search_quote(stock_code)
    if isinstance(quote, Quote):
        return quote.quote_id
    if quote is None:
        rich.print(f'证券代码 "{stock_code}" 可能有误')
        return stock_code


def process_dataframe_and_series(
    function_fields: Dict[str, Callable] = dict(),
    remove_columns_and_indexes: List[str] = list(),
):
    """
    对 DataFrame 和 Series 进一步操作

    Parameters
    ----------
    function_fields : Dict[str, Callable], optional
        函数字典
    remove_columns_and_indexes : List[str], optional
        需要删除的行或者列, by default list()
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            values = func(*args, **kwargs)
            if isinstance(values, pd.DataFrame):
                for column, function_name in function_fields.items():
                    if column not in values.columns:
                        continue
                    values[column] = values[column].apply(function_name)
                for column in remove_columns_and_indexes:
                    if column in values.columns:
                        del values[column]
            elif isinstance(values, pd.Series):
                for index in remove_columns_and_indexes:
                    values = values.drop(index)
            return values

        return wrapper

    return decorator


