import pandas as pd
from ..utils import to_numeric, requests_obj, validate_request
from retry import retry
from .config import EastmoneyFundHeaders
from ...crawl.settings import *
from ..common.explain_change import exchange_explain


@validate_request
@retry(tries=3)
@to_numeric
def get_fund_history_price(token: str, fund_code: str, pz: int = 40000, is_explain: bool = False) -> pd.DataFrame:
    """
    根据基金代码和要获取的页码抓取基金净值信息

    Parameters
    ----------
    fund_code : str
        6 位基金代码
    pz : int, optional
        页码, 默认为 40000 以获取全部历史数据

    Returns
    -------
    DataFrame
        包含基金历史净值等数据

    Examples
    --------
        日期    单位净值    累计净值     涨跌幅
    0    2021-06-11  1.5188  3.1499   -3.09
    1    2021-06-10  1.5673  3.1984    1.69
    2    2021-06-09  1.5412  3.1723    0.11
    3    2021-06-08  1.5395  3.1706    -6.5
    4    2021-06-07  1.6466  3.2777    1.61
    ...         ...     ...     ...     ...
    1469 2015-06-08  1.0380  1.0380  2.5692
    1470 2015-06-05  1.0120  1.0120  1.5045
    1471 2015-06-04  0.9970  0.9970      --
    1472 2015-05-29  0.9950  0.9950      --
    1473 2015-05-27  1.0000  1.0000      --
    :param is_explain:
    :param pz:
    :param fund_code:
    :param token:

    """
    data = {
        'FCODE': f'{fund_code}',
        'IsShareNet': 'true',
        'MobileKey': '1',
        'appType': 'ttjj',
        'appVersion': '6.2.8',
        'cToken': '1',
        'deviceid': '1',
        'pageIndex': '1',
        'pageSize': f'{pz}',
        'plat': 'Iphone',
        'product': 'EFund',
        'serverVersion': '6.2.8',
        'uToken': '1',
        'userId': '1',
        'version': '6.2.8',
    }
    json_response = requests_obj.get(''.join(fund_history_url), data, headers=EastmoneyFundHeaders).json()
    rows = []
    columns = ['日期', '单位净值', '累计净值', '涨跌幅']
    if json_response is None:
        return pd.DataFrame(rows, columns=columns)
    datas = json_response['Datas']
    if len(datas) == 0:
        return pd.DataFrame(rows, columns=columns)
    for stock in datas:
        date = stock['FSRQ']
        rows.append(
            {
                '日期': date,
                '单位净值': stock['DWJZ'],
                '累计净值': stock['LJJZ'],
                '涨跌幅': stock['JZZZL'],
            }
        )
    df = pd.DataFrame(rows)
    return exchange_explain(df, is_explain)
