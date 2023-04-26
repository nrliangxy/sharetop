import rich
import uuid
import pandas as pd
from retry import retry
from ..utils import to_numeric, requests_obj
from .config import EastmoneyFundHeaders
from ...crawl.settings import *


@retry(tries=3)
@to_numeric
def get_base_info(fund_code: str) -> pd.Series:
    """
    获取基金的一些基本信息
    Parameters
    ----------
    fund_code : str
        6 位基金代码
    Returns
    -------
    Series
        基金的一些基本信息
    """
    str_uuid = str(uuid.uuid4()).upper()
    params = (
        ('FCODE', fund_code),
        ('deviceid', str_uuid),
        ('plat', 'Iphone'),
        ('product', 'EFund'),
        ('version', '6.3.8'),
    )
    json_response = requests_obj.get(''.join(fund_basic_url), params, headers=EastmoneyFundHeaders).json()
    columns = {
        'FCODE': '基金代码',
        'SHORTNAME': '基金简称',
        'ESTABDATE': '成立日期',
        'RZDF': '涨跌幅',
        'DWJZ': '最新净值',
        'JJGS': '基金公司',
        'FSRQ': '净值更新日期',
        'COMMENTS': '简介',
    }
    items = json_response['Datas']
    if not items:
        rich.print('基金代码', fund_code, '可能有误')
        return pd.Series(index=columns.values())

    s = pd.Series(json_response['Datas']).rename(index=columns)[columns.values()]

    s = s.apply(lambda x: x.replace('\n', ' ').strip() if isinstance(x, str) else x)
    return s
