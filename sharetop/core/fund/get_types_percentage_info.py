from retry import retry
from ..utils import to_numeric, requests_obj
from .config import EastmoneyFundHeaders
from typing import List, Union
from ...crawl.settings import *
import pandas as pd


@retry(tries=3)
@to_numeric
def get_types_percentage(
    fund_code: str, dates: Union[List[str], str, None] = None
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
    >>> import efinance as ef
    >>> # 获取持仓公开日期
    >>> public_dates = ef.fund.get_public_dates('005827')
    >>> # 取前两个公开持仓日期
    >>> dates = public_dates[:2]
    >>> ef.fund.get_types_percentage('005827',dates)
        基金代码   股票比重 债券比重  现金比重         总规模(亿元) 其他比重
    0  005827   94.4   --  6.06  880.1570625231    0
    0  005827  94.09   --  7.63   677.007455712    0
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
    return df
