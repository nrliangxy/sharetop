import re
import pandas as pd
from retry import retry
from ..utils import requests_obj, validate_request, to_numeric
from ..common.getter import BaseApplication
from ..common.explain_change import exchange_explain


@validate_request
@to_numeric
@retry(tries=3)
def get_fund_codes(token: str, ft: str = None, is_explain: bool = False) -> pd.DataFrame:
    """
    获取天天基金网公开的全部公墓基金名单
    Parameters
    ----------
    ft : str, optional
        基金类型可选示例如下
        - ``'zq'``  : 债券类型基金
        - ``'gp'``  : 股票类型基金
        - ``'etf'`` : ETF 基金
        - ``'hh'``  : 混合型基金
        - ``'zs'``  : 指数型基金
        - ``'fof'`` : FOF 基金
        - ``'qdii'``: QDII 型基金
        - ``None``  : 全部
    Returns
    -------
    DataFrame
        天天基金网基金名单数据
    Examples
    --------
        基金代码                  基金简称
    0     003834              华夏能源革新股票
    1     005669            前海开源公用事业股票
    2     004040             金鹰医疗健康产业A
    3     517793                 1.20%
    4     004041             金鹰医疗健康产业C
    ...      ...                   ...
    1981  012503      国泰中证环保产业50ETF联接A
    1982  012517  国泰中证细分机械设备产业主题ETF联接C
    1983  012600             中银内核驱动股票C
    1984  011043             国泰价值先锋股票C
    1985  012516  国泰中证细分机械设备产业主题ETF联接A
    :param is_explain:
    :param ft:
    :param token:
    """
    params = [
        ('op', 'dy'),
        ('dt', 'kf'),
        ('rs', ''),
        ('gs', '0'),
        ('sc', 'qjzf'),
        ('st', 'desc'),
        ('es', '0'),
        ('qdii', ''),
        ('pi', '1'),
        ('pn', '50000'),
        ('dx', '0'),
    ]
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Accept': '*/*',
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    if ft is not None:
        params.append(('ft', ft))
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx'
    response = requests_obj.get(url, params, headers=headers)
    results = re.findall('\[.*\]', response.text)
    new_results = eval(results[0])
    application_obj = BaseApplication(new_results)
    return exchange_explain(application_obj.deal_fund_list(), is_explain)
