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
def get_fund_period_change(token: str, fund_code: str, is_explain: bool = False) -> pd.DataFrame:
    """
    获取基金阶段涨跌幅度
    Parameters
    ----------
    fund_code : str
        6 位基金代码
    Returns
    -------
    DataFrame
        指定基金的阶段涨跌数据
    Examples
    --------
        基金代码     收益率   同类平均  同类排行  同类总数   时间段
    0  161725   -6.28   0.07  1408  1409   近一周
    1  161725   10.85   5.82   178  1382   近一月
    2  161725   25.32   7.10    20  1332   近三月
    3  161725   22.93  10.39    79  1223   近六月
    4  161725  103.76  33.58     7  1118   近一年
    5  161725  166.59  55.42     9   796   近两年
    6  161725  187.50  48.17     2   611   近三年
    7  161725  519.44  61.62     1   389   近五年
    8  161725    6.46   5.03   423  1243  今年以来
    9  161725  477.00                     成立以来
    :param is_explain:
    :param fund_code:
    :param token:
    """
    str_uuid = str(uuid.uuid4()).upper()
    params = (
        ('AppVersion', '6.3.8'),
        ('FCODE', fund_code),
        ('MobileKey', str_uuid),
        ('OSVersion', '14.3'),
        ('deviceid', str_uuid),
        ('passportid', '3061335960830820'),
        ('plat', 'Iphone'),
        ('product', 'EFund'),
        ('version', '6.3.6'),
    )
    json_response = requests_obj.get(''.join(fund_period_change_url), params, headers=EastmoneyFundHeaders).json()
    columns = {
        'syl': '收益率',
        'avg': '同类平均',
        'rank': '同类排行',
        'sc': '同类总数',
        'title': '时间段',
    }
    titles = {
        'Z': '近一周',
        'Y': '近一月',
        '3Y': '近三月',
        '6Y': '近六月',
        '1N': '近一年',
        '2Y': '近两年',
        '3N': '近三年',
        '5N': '近五年',
        'JN': '今年以来',
        'LN': '成立以来',
    }
    # 发行时间
    ESTABDATE = json_response['Expansion']['ESTABDATE']
    df = pd.DataFrame(json_response['Datas'])
    df = df[list(columns.keys())].rename(columns=columns)
    df['时间段'] = titles.values()
    df.insert(0, '基金代码', fund_code)
    return exchange_explain(df, is_explain)
