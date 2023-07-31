import rich
import uuid
import pandas as pd
from retry import retry
from ..utils import to_numeric, requests_obj, validate_request
from .config import EastmoneyFundHeaders
from ...crawl.settings import *
from ..common.explain_change import exchange_explain


@validate_request
@retry(tries=3)
@to_numeric
def get_fund_base_info(token: str, fund_code: str, is_explain: bool = False) -> pd.Series:
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
        :param is_explain:
        :param fund_code:
        :param token:
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
        'ENDNAV': '基金规模',
        'FEGMRQ': '基金规模更新时间',
        'RLEVEL_SZ': '最新评级'
    }
    items = json_response['Datas']
    items = {columns.get(k): v for k, v in items.items() if columns.get(k)}
    if not items:
        rich.print('基金代码', fund_code, '可能有误')
        return pd.Series(index=columns.values())

    s = pd.DataFrame([items])
    df = s.apply(lambda x: x.replace('\n', ' ').strip() if isinstance(x, str) else x)
    return exchange_explain(df, is_explain)
