import uuid
import pandas as pd
from typing import List, Union
from ..utils import to_numeric, requests_obj, validate_request
from ...crawl.settings import *
from .config import EastmoneyFundHeaders
from ..common.explain_change import exchange_explain


@validate_request
@to_numeric
def get_fund_industry_distribution(
    token: str, fund_code: str, dates: Union[str, List[str]] = None, is_explain: bool = False
) -> pd.DataFrame:
    """
    获取指定基金行业分布信息
    Parameters
    ----------
    fund_code : str
        6 位基金代码
    dates : Union[str, List[str]], optional
        日期
        可选示例如下
        - ``None`` : 最新公开日期
        - ``'2020-01-01'`` : 一个公开持仓日期
        - ``['2020-12-31' ,'2019-12-31']`` : 多个公开持仓日期
    Returns
    -------
    DataFrame
        指定基金行业持仓信息
    Examples
    --------
    0   161725               制造业  93.07  2021-06-30  6492580.019556
    1   161725               金融业   0.01  2021-06-30      485.060688
    2   161725          农、林、牧、渔业      0  2021-06-30        0.585078
    3   161725  电力、热力、燃气及水生产和供应业      0  2021-06-30        1.302039
    4   161725               建筑业      0  2021-06-30        2.537137
    5   161725            批发和零售业      0  2021-06-30        5.888394
    6   161725   信息传输、软件和信息技术服务业      0  2021-06-30      157.037536
    7   161725     水利、环境和公共设施管理业      0  2021-06-30        4.443833
    8   161725                教育      0  2021-06-30        1.626203
    9   161725        科学研究和技术服务业      0  2021-06-30        48.30805
    10  161725               采矿业     --  2021-06-30              --
    11  161725       交通运输、仓储和邮政业     --  2021-06-30              --
    12  161725          租赁和商务服务业     --  2021-06-30              --
    13  161725            住宿和餐饮业     --  2021-06-30              --
    14  161725              房地产业     --  2021-06-30              --
    15  161725     居民服务、修理和其他服务业     --  2021-06-30              --
    16  161725           卫生和社会工作     --  2021-06-30              --
    17  161725         文化、体育和娱乐业     --  2021-06-30              --
    18  161725                综合     --  2021-06-30              --
    19  161725                合计  93.08  2021-06-30  6493286.808514
    :param is_explain:
    :param dates:
    :param fund_code:
    :param token:
    """
    columns = {'HYMC': '行业名称', 'ZJZBL': '持仓比例', 'FSRQ': '公布日期', 'SZ': '市值'}
    str_uuid = str(uuid.uuid4()).upper()
    df = pd.DataFrame(columns=columns.values())
    if isinstance(dates, str):
        dates = [dates]
    elif dates is None:
        dates = [None]
    for date in dates:
        params = [
            ('FCODE', fund_code),
            ('OSVersion', '14.4'),
            ('appVersion', '6.3.8'),
            ('deviceid', str_uuid),
            ('plat', 'Iphone'),
            ('product', 'EFund'),
            ('serverVersion', '6.3.6'),
            ('version', '6.3.8'),
        ]
        if date is not None:
            params.append(('DATE', date))
        url = "".join(fund_industry_url)
        response = requests_obj.get(url, params, headers=EastmoneyFundHeaders)
        datas = response.json()['Datas']
        _df = pd.DataFrame(datas)
        _df = _df.rename(columns=columns)
        df = pd.concat([df, _df], axis=0, ignore_index=True)
    df.insert(0, '基金代码', fund_code)
    df = df.drop_duplicates()
    return exchange_explain(df, is_explain)
