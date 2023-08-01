import pandas as pd
from typing import List
from ..common.config import EASTMONEY_REQUEST_HEADERS, FS_DICT
from .config import EASTMONEY_BOND_BASE_INFO_FIELDS
from ..utils import requests_obj
from ...crawl.settings import *
from ..utils import to_numeric, process_dataframe_and_series, validate_request
from ..common import get_market_realtime_by_fs
from ..common.explain_change import exchange_explain


@validate_request
def get_bond_base_info_list(token: str, is_explain: bool = False) -> pd.DataFrame:
    """
    获取全部债券基本信息列表
    Returns
    -------
    DataFrame
        债券一些基本信息
    Examples
    --------
        债券代码   债券名称    正股代码  正股名称 债券评级                 申购日期    发行规模(亿)  网上发行中签率(%)                 上市日期                 到期日期   期限(年)                                               利率说明
    0   123120   隆华转债  300263  隆华科技  AA-  2021-07-30 00:00:00   7.989283         NaN                 None  2027-07-30 00:00:00       6  第一年为0.40%、第二年为0.70%、第三年为1.00%、第四年为1.60%、第五年为2....
    1   110081   闻泰转债  600745  闻泰科技  AA+  2021-07-28 00:00:00  86.000000    0.044030                 None  2027-07-28 00:00:00       6  第一年0.10%、第二年0.20%、第三年0.30%、第四年1.50%、第五年1.80%、第...
    2   118001   金博转债  688598  金博股份   A+  2021-07-23 00:00:00   5.999010    0.001771                 None  2027-07-23 00:00:00       6  第一年0.50%、第二年0.70%、第三年1.20%、第四年1.80%、第五年2.40%、第...
    3   123119   康泰转2  300601  康泰生物   AA  2021-07-15 00:00:00  20.000000    0.014182                 None  2027-07-15 00:00:00       6  第一年为0.30%、第二年为0.50%、第三年为1.00%、第 四年为1.50%、第五年为1....
    4   113627   太平转债  603877   太平鸟   AA  2021-07-15 00:00:00   8.000000    0.000542                 None  2027-07-15 00:00:00       6  第一年0.30%、第二年0.50%、第三年1.00%、第四年1.50%、第五年1.80%、第...
    ..     ...    ...     ...   ...  ...                  ...        ...         ...                  ...                  ...     ...                                                ...
    80  110227   赤化转债  600227   圣济堂  AAA  2007-10-10 00:00:00   4.500000    0.158854  2007-10-23 00:00:00  2009-05-25 00:00:00  1.6192  票面利率和付息日期:本次发行的债券票面利率第一 年为1.5%、第二年为1.8%、第三年为2....
    81  126006  07深高债  600548   深高速  AAA  2007-10-09 00:00:00  15.000000    0.290304  2007-10-30 00:00:00  2013-10-09 00:00:00       6                                               None
    82  110971   恒源转债  600971  恒源煤电  AAA  2007-09-24 00:00:00   4.000000    5.311774  2007-10-12 00:00:00  2009-12-21 00:00:00  2.2484  票面利率为:第一年年利率1.5%,第二年年利率1.8%,第三年年利率2.1%,第四年年利率2...
    83  110567   山鹰转债  600567  山鹰国际   AA  2007-09-05 00:00:00   4.700000    0.496391  2007-09-17 00:00:00  2010-02-01 00:00:00  2.4055  票面利率和付息日期:本次发行的债券票面利率第一年为1.4%,第二年为1.7%,第三年为2....
    84  110026   中海转债  600026  中远海能  AAA  2007-07-02 00:00:00  20.000000    1.333453  2007-07-12 00:00:00  2008-03-27 00:00:00   0.737  票面利率:第一年为1.84%,第二年为2.05%,第三年为2.26%,第四年为2.47%,第...
    """

    page = 1
    dfs: List[pd.DataFrame] = []
    columns = EASTMONEY_BOND_BASE_INFO_FIELDS
    while 1:
        params = (
            ('sortColumns', 'PUBLIC_START_DATE'),
            ('sortTypes', '-1'),
            ('pageSize', '500'),
            ('pageNumber', f'{page}'),
            ('reportName', 'RPT_BOND_CB_LIST'),
            ('columns', 'ALL'),
            ('source', 'WEB'),
            ('client', 'WEB'),
        )
        json_response = requests_obj.get(''.join(bond_base_list_url), params, headers=EASTMONEY_REQUEST_HEADERS).json()
        if json_response['result'] is None:
            break
        data = json_response['result']['data']
        df = pd.DataFrame(data).rename(columns=columns)[columns.values()]
        dfs.append(df)
        page += 1
    df = pd.concat(dfs, ignore_index=True)
    return exchange_explain(df, is_explain)


@process_dataframe_and_series(remove_columns_and_indexes=['市场编号'])
@to_numeric
def get_bond_realtime_quotes(is_explain: bool = False, **kwargs) -> pd.DataFrame:
    """
    获取沪深市场全部债券实时行情信息
    Returns
    -------
    DataFrame
        沪深市场全部债券实时行情信息
    Examples
    --------
        债券代码  债券名称    涨跌幅      最新价       最高       最低      今开     涨跌额      换手率     量比 动态市盈率      成交量           成交额    昨日收盘         总市值        流通市值      行情ID 市场类型
    0    123051  今天转债  24.03   158.66    165.0    134.0   134.0   30.74   496.74  67.16     -  1388341  2185911136.0  127.92   443443594   443443594  0.123051   深A
    1    123042  银河转债  16.04  219.309    224.0   193.11   194.5  30.309  1833.99   1.34     -  3042265  6402014720.0   189.0   363794813   363794813  0.123042   深A
    2    113034  滨化转债  13.49   247.71   255.62    214.5   214.5   29.45   334.56   2.96     -  1585993  3798255024.0  218.26  1174284861  1174284861  1.113034   沪A
    3    128064  司尔转债  11.29   148.01   150.34  133.007  133.73   15.01   277.06   7.04     -   887301  1305800336.0   133.0   474009426   474009426  0.128064   深A
    4    113027  华钰转债   8.38   129.86    130.2    122.3   123.0   10.04    83.84   4.15     -   272641   346817120.0  119.82   422273164   422273164  1.113027   沪A
    ..      ...   ...    ...      ...      ...      ...     ...     ...      ...    ...   ...      ...           ...     ...         ...         ...       ...  ...
    390  113621  彤程转债  -4.45   188.57   198.22    188.0  196.01   -8.79    29.91   0.47     -   168709   326018848.0  197.36  1063693010  1063693010  1.113621   沪A
    391  128017  金禾转债  -4.86  182.676  204.989   182.61  195.16  -9.324    35.58    2.0     -   196375   375750768.0   192.0  1008366222  1008366222  0.128017   深A
    392  113548  石英转债  -5.16   250.22   267.57   246.56   262.3  -13.61   143.32   0.72     -   175893   452796304.0  263.83   307086749   307086749  1.113548   沪A
    393  128093  百川转债  -5.71  429.042   449.97  426.078   443.1 -25.958   426.86   0.36     -   693261  3032643232.0   455.0   696810974   696810974  0.128093   深A
    394  123066  赛意转债   -6.0   193.08  203.999   193.08   203.0  -12.32   323.13   0.22     -   133317   261546032.0   205.4    79660753    79660753  0.123066   深A
    """
    df = get_market_realtime_by_fs(FS_DICT['bond'], **kwargs)
    df.rename(columns={'代码': '债券代码', '名称': '债券名称'}, inplace=True)
    return exchange_explain(df, is_explain)


@validate_request
@to_numeric
def get_bond_base_info(token: str, bond_code: str, is_explain: bool = False) -> pd.Series:
    """
    获取单只债券基本信息
    Parameters
    ----------
    bond_code : str
        债券代码
    Returns
    -------
    Series
        债券的一些基本信息
        :param is_explain:
        :param bond_code:
        :param token:
    """
    columns = EASTMONEY_BOND_BASE_INFO_FIELDS
    params = (
        ('reportName', 'RPT_BOND_CB_LIST'),
        ('columns', 'ALL'),
        ('source', 'WEB'),
        ('client', 'WEB'),
        ('filter', f'(SECURITY_CODE="{bond_code}")'),
    )
    url = ''.join(bond_base_info_url)
    json_response = requests_obj.get(url, params, headers=EASTMONEY_REQUEST_HEADERS).json()
    if json_response['result'] is None:
        return pd.Series(index=columns.values(), dtype='object')
    items = json_response['result']['data']
    s = pd.DataFrame(items).rename(columns=columns)
    s = s[columns.values()]
    return exchange_explain(s, is_explain)


@validate_request
def get_bond_public(token: str) -> pd.DataFrame:
    """
    中国-债券信息披露-债券发行
    http://www.chinamoney.com.cn/chinese/xzjfx/
    :return: 债券发行
    :rtype: pandas.DataFrame
    """
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-an/bnBondEmit"
    params = {
        "enty": "",
        "bondType": "",
        "bondNameCode": "",
        "leadUnderwriter": "",
        "pageNo": "1",
        "pageSize": "1000",
        "limit": "1",
    }
    import requests
    json_response = requests.post(url, data=params)
    temp_df = pd.DataFrame(json_response["records"])
    temp_df.columns = [
        "债券全称",
        "债券类型",
        "-",
        "发行日期",
        "-",
        "计息方式",
        "-",
        "债券期限",
        "-",
        "债券评级",
        "-",
        "价格",
        "计划发行量",
    ]
    temp_df = temp_df[
        [
            "债券全称",
            "债券类型",
            "发行日期",
            "计息方式",
            "价格",
            "债券期限",
            "计划发行量",
            "债券评级",
        ]
    ]
    temp_df["价格"] = pd.to_numeric(temp_df["价格"], errors="coerce")
    temp_df["计划发行量"] = pd.to_numeric(temp_df["计划发行量"], errors="coerce")
    return temp_df
