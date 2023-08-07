import uuid
import pandas as pd
from typing import List, Union, Dict, Any
from retry import retry
from ..utils import to_numeric, requests_obj, validate_request
from jsonpath import jsonpath
from .config import EastmoneyFundHeaders
from ..common.explain_change import exchange_explain


@validate_request
@retry(tries=3)
@to_numeric
def get_fund_invest_position(token: str,
                             fund_code: str, dates: Union[str, List[str]] = None, is_explain: bool = False
                             ) -> pd.DataFrame:
    """
    获取基金持仓占比数据
    Parameters
    ----------
    fund_code : str
        基金代码
    dates : Union[str, List[str]], optional
        日期或者日期构成的列表
        可选示例如下

        - ``None`` : 最新公开日期
        - ``'2020-01-01'`` : 一个公开持仓日期
        - ``['2020-12-31' ,'2019-12-31']`` : 多个公开持仓日期
    Returns
    -------
    DataFrame
        基金持仓占比数据
    Examples
    --------
        基金代码    股票代码  股票简称   持仓占比  较上期变化        公开日期
    0  161725  600519  贵州茅台  16.78   1.36  2022-03-31
    1  161725  600809  山西汾酒  15.20   0.52  2022-03-31
    2  161725  000568  泸州老窖  14.57  -0.89  2022-03-31
    3  161725  000858   五粮液  12.83  -1.26  2022-03-31
    4  161725  002304  洋河股份  11.58   0.91  2022-03-31
    5  161725  603369   今世缘   3.75  -0.04  2022-03-31
    6  161725  000799   酒鬼酒   3.40  -0.91  2022-03-31
    7  161725  000596  古井贡酒   3.27  -0.24  2022-03-31
    8  161725  600779   水井坊   2.59  -0.26  2022-03-31
    9  161725  603589   口子窖   2.30  -0.38  2022-03-31

        基金代码    股票代码  股票简称   持仓占比  较上期变化        公开日期
    0   161725  600519  贵州茅台  16.78   1.36  2022-03-31
    1   161725  600809  山西汾酒  15.20   0.52  2022-03-31
    2   161725  000568  泸州老窖  14.57  -0.89  2022-03-31
    3   161725  000858   五粮液  12.83  -1.26  2022-03-31
    4   161725  002304  洋河股份  11.58   0.91  2022-03-31
    5   161725  603369   今世缘   3.75  -0.04  2022-03-31
    6   161725  000799   酒鬼酒   3.40  -0.91  2022-03-31
    7   161725  000596  古井贡酒   3.27  -0.24  2022-03-31
    8   161725  600779   水井坊   2.59  -0.26  2022-03-31
    9   161725  603589   口子窖   2.30  -0.38  2022-03-31
    10  161725  000568  泸州老窖  15.46   0.57  2021-12-31
    11  161725  600519  贵州茅台  15.42   0.63  2021-12-31
    12  161725  600809  山西汾酒  14.68  -1.72  2021-12-31
    13  161725  000858   五粮液  14.09   0.87  2021-12-31
    14  161725  002304  洋河股份  10.67  -1.34  2021-12-31
    15  161725  000799   酒鬼酒   4.31   0.09  2021-12-31
    16  161725  603369   今世缘   3.79   0.81  2021-12-31
    17  161725  000596  古井贡酒   3.51  -0.69  2021-12-31
    18  161725  600779   水井坊   2.85  -0.41  2021-12-31
    19  161725  603589   口子窖   2.68   2.68  2021-12-31
    :param token:
    :param fund_code:
    :param dates:
    :param is_explain:

    """
    columns = {
        'GPDM': '股票代码',
        'GPJC': '股票简称',
        'JZBL': '持仓占比',
        'PCTNVCHG': '较上期变化',
    }
    str_uuid = str(uuid.uuid4()).upper()
    df = pd.DataFrame(columns=columns.values())
    if not isinstance(dates, List):
        dates = [dates]
    if dates is None:
        dates = [None]
    dfs: List[pd.DataFrame] = []
    for date in dates:
        params = [
            ('FCODE', fund_code),
            ('appType', 'ttjj'),
            ('deviceid', str_uuid),
            ('plat', 'Iphone'),
            ('product', 'EFund'),
            ('serverVersion', '6.2.8'),
            ('version', '6.2.8'),
        ]
        if date is not None:
            params.append(('DATE', date))
        url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition'
        json_response = requests_obj.get(url, params, headers=EastmoneyFundHeaders).json()
        stocks = jsonpath(json_response, '$..fundStocks[:]')
        if not stocks:
            continue
        date = json_response['Expansion']
        _df = pd.DataFrame(stocks)
        _df['公开日期'] = date
        _df.insert(0, '基金代码', fund_code)
        dfs.append(_df)
    fields = ['基金代码'] + list(columns.values()) + ['公开日期']
    if not dfs:
        return pd.DataFrame(columns=fields)
    df = pd.concat(dfs, axis=0, ignore_index=True).rename(columns=columns)[fields]
    return exchange_explain(df, is_explain)


@validate_request
def get_fund_public_dates(token: str, fund_code: str) -> Dict[str, Any]:
    """
    获取历史上更新持仓情况的日期列表
    Parameters
    ----------
    fund_code : str
        6 位基金代码
    Returns
    -------
    List[str]
        指定基金公开持仓的日期列表
    Examples
    --------
    ['2021-03-31', '2021-01-08', '2020-12-31', '2020-09-30', '2020-06-30']
    """
    params = (
        ('FCODE', fund_code),
        ('appVersion', '6.3.8'),
        ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
        ('plat', 'Iphone'),
        ('product', 'EFund'),
        ('serverVersion', '6.3.6'),
        ('version', '6.3.8'),
    )
    url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNIVInfoMultiple'
    json_response = requests_obj.get(url, params, headers=EastmoneyFundHeaders).json()
    if json_response['Datas'] is None:
        return {"date_list": []}
    return {"date_list": json_response['Datas']}
