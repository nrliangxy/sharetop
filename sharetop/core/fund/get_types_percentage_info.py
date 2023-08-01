from retry import retry
from ..utils import to_numeric, requests_obj, validate_request
from .config import EastmoneyFundHeaders
from typing import List, Union
from ...crawl.settings import *
import pandas as pd
from ..common.explain_change import exchange_explain


@validate_request
@retry(tries=3)
@to_numeric
def get_fund_types_percentage(
    token: str, fund_code: str, dates: Union[List[str], str, None] = None, is_explain: bool = False
) -> pd.DataFrame:
    """
    获取指定基金不同类型占比信息
    Parameters
    ----------
    fund_code : str
        6 位基金代码
    dates : Union[List[str], str, None]
        可选值类型示例如下(后面有获取 dates 的例子)

        - ``None`` : 最新公开日期
        - ``'2020-01-01'`` : 一个公开持仓日期
        - ``['2020-12-31' ,'2019-12-31']`` : 多个公开持仓日期
    Returns
    -------
    DataFrame
        指定基金的在不同日期的不同类型持仓占比信息
    Examples
    --------
        基金代码   股票比重 债券比重  现金比重         总规模(亿元) 其他比重
    0  005827   94.4   --  6.06  880.1570625231    0
    0  005827  94.09   --  7.63   677.007455712    0
    :param dates:
    :param fund_code:
    :param token:
    """
    columns = {'GP': '股票比重', 'ZQ': '债券比重', 'HB': '现金比重', 'JZC': '总规模(亿元)', 'QT': '其他比重'}
    df = pd.DataFrame(columns=columns.values())
    if not isinstance(dates, List):
        dates = [dates]
    elif dates is None:
        dates = [None]
    for date in dates:
        params = [
            ('FCODE', fund_code),
            ('OSVersion', '14.3'),
            ('appVersion', '6.3.8'),
            ('deviceid', '3EA024C2-7F21-408B-95E4-383D38160FB3'),
            ('plat', 'Iphone'),
            ('product', 'EFund'),
            ('serverVersion', '6.3.6'),
            ('version', '6.3.8'),
        ]
        if date is not None:
            params.append(('DATE', date))
        params = tuple(params)
        url = ''.join(fun_types_percentage_url)
        json_response = requests_obj.get(url, params, headers=EastmoneyFundHeaders).json()
        if len(json_response['Datas']) == 0:
            continue
        _df = pd.DataFrame(json_response['Datas'])[columns.keys()]
        _df = _df.rename(columns=columns)
        df = pd.concat([df, _df], axis=0, ignore_index=True)
    df.insert(0, '基金代码', fund_code)
    return exchange_explain(df, is_explain)
