from ..utils import to_numeric, validate_request
from ..common.getter import get_history_bill as get_history_bill_for_stock
from ..common.getter import get_real_time_bill_data_one
from ..common.common_base import CommonFunc
from ..common.explain_change import exchange_explain
from typing import Dict, List, Union
import pandas as pd

common_func_obj = CommonFunc()


@validate_request
@to_numeric
def get_stock_history_capital(token: str, stock_code: str, is_explain: bool = False) -> pd.DataFrame:
    """
    获取单只股票历史单子流入流出数据
    Parameters
    ----------
    stock_code : str
        股票代码
    Returns
    -------
    DataFrame
        沪深市场单只股票历史单子流入流出数据
    Examples
    --------
        股票名称    股票代码          日期         主力净流入       小单净流入         中单净流入         大单净流入        超大单净流入  主力净流入占比  小单流入净占比  中单流入净占比  大单流入净占比  超大单流入净占比      收盘价   涨跌幅
    0    贵州茅台  600519  2021-03-04 -3.670272e+06  -2282056.0  5.952143e+06  1.461528e+09 -1.465199e+09    -0.03    -0.02     0.04    10.99    -11.02  2013.71 -5.05
    1    贵州茅台  600519  2021-03-05 -1.514880e+07  -1319066.0  1.646793e+07 -2.528896e+07  1.014016e+07    -0.12    -0.01     0.13    -0.19      0.08  2040.82  1.35
    2    贵州茅台  600519  2021-03-08 -8.001702e+08   -877074.0  8.010473e+08  5.670671e+08 -1.367237e+09    -6.29    -0.01     6.30     4.46    -10.75  1940.71 -4.91
    3    贵州茅台  600519  2021-03-09 -2.237770e+08  -6391767.0  2.301686e+08 -1.795013e+08 -4.427571e+07    -1.39    -0.04     1.43    -1.11     -0.27  1917.70 -1.19
    4    贵州茅台  600519  2021-03-10 -2.044173e+08  -1551798.0  2.059690e+08 -2.378506e+08  3.343331e+07    -2.02    -0.02     2.03    -2.35      0.33  1950.72  1.72
    ..    ...     ...         ...           ...         ...           ...           ...           ...      ...      ...      ...      ...       ...      ...   ...
    97   贵州茅台  600519  2021-07-26 -1.564233e+09  13142211.0  1.551091e+09 -1.270400e+08 -1.437193e+09    -8.74     0.07     8.67    -0.71     -8.03  1804.11 -5.05
    98   贵州茅台  600519  2021-07-27 -7.803296e+08 -10424715.0  7.907544e+08  6.725104e+07 -8.475807e+08    -5.12    -0.07     5.19     0.44     -5.56  1712.89 -5.06
    99   贵州茅台  600519  2021-07-28  3.997645e+08   2603511.0 -4.023677e+08  2.315648e+08  1.681997e+08     2.70     0.02    -2.72     1.57      1.14  1768.90  3.27
    100  贵州茅台  600519  2021-07-29 -9.209842e+08  -2312235.0  9.232964e+08 -3.959741e+08 -5.250101e+08    -8.15    -0.02     8.17    -3.50     -4.65  1749.79 -1.08
    101  贵州茅台  600519  2021-07-30 -1.524740e+09  -6020099.0  1.530761e+09  1.147248e+08 -1.639465e+09   -11.63    -0.05    11.68     0.88    -12.51  1678.99 -4.05
    :param is_explain:
    :param stock_code:
    :param token:

    """
    df = get_history_bill_for_stock(stock_code)
    df.rename(columns={'代码': '股票代码', '名称': '股票名称'}, inplace=True)
    return exchange_explain(df, is_explain)


@to_numeric
def get_stock_real_time_daily_capital(stock_code: str, is_explain: bool = False) -> pd.DataFrame:
    """
    获取单只股票最新交易日的日内分钟级单子流入流出数据
    Parameters
    ----------
    stock_code : str
        股票代码
    Returns
    -------
    DataFrame
        单只股票最新交易日的日内分钟级单子流入流出数据

    Examples
    --------
        股票代码                时间        主力净流入      小单净流入        中单净流入        大单净流入       超大单净流入
    0    600519  2021-07-29 09:31   -3261705.0  -389320.0    3651025.0  -12529658.0    9267953.0
    1    600519  2021-07-29 09:32    6437999.0  -606994.0   -5831006.0  -42615994.0   49053993.0
    2    600519  2021-07-29 09:33   13179707.0  -606994.0  -12572715.0  -85059118.0   98238825.0
    3    600519  2021-07-29 09:34   15385244.0  -970615.0  -14414632.0  -86865209.0  102250453.0
    4    600519  2021-07-29 09:35    7853716.0  -970615.0   -6883104.0  -75692436.0   83546152.0
    ..      ...               ...          ...        ...          ...          ...          ...
    235  600519  2021-07-29 14:56 -918956019.0 -1299630.0  920255661.0 -397127393.0 -521828626.0
    236  600519  2021-07-29 14:57 -920977761.0 -2319213.0  923296987.0 -397014702.0 -523963059.0
    237  600519  2021-07-29 14:58 -920984196.0 -2312233.0  923296442.0 -395974137.0 -525010059.0
    238  600519  2021-07-29 14:59 -920984196.0 -2312233.0  923296442.0 -395974137.0 -525010059.0
    239  600519  2021-07-29 15:00 -920984196.0 -2312233.0  923296442.0 -395974137.0 -525010059.0
    :param stock_code:
    :param is_explain:
    """
    df = get_real_time_bill_data_one(stock_code)
    return exchange_explain(df, is_explain)


def get_stock_real_time_sum_capital(stock_codes: Union[str, List[str]], is_explain: bool = False
                                    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    获取单只股票最新交易日的日内最新单子流入流出数据
    Parameters
    ----------
    stock_codes : 股票、债券代码 str 或者是 list
    如果是 str，为单支股票，如果为list，为多支股票
    Returns
    -------
    DataFrame
        单支或者多支股票、债券最新交易日的日内实时子流入流出数据
        :param stock_codes:
        :param is_explain:
    """
    base_func_name = get_stock_real_time_sum_capital.__name__
    return exchange_explain(common_func_obj.get_common_func(stock_codes, base_func_name), is_explain)


def get_stock_real_time_sector_capital(sector: str, monitor_time: str, is_explain: bool = False):
    """
    :param is_explain:
    :param sector: industry: 行业, concept: 概念, area: 地域
    :param monitor_time: 1: 当天, 5: 5日,  10: 10日
    :return:
    """
    allowed_values = ['industry', 'concept', 'area']
    if sector not in allowed_values:
        raise ValueError(f"Invalid input: {sector}. Allowed values are {allowed_values}")
    monitor_time_allowed_values = ['1', '5', '10']
    if monitor_time not in monitor_time_allowed_values:
        raise ValueError(f"Invalid input: {monitor_time}. Allowed values are {monitor_time_allowed_values}")
    kwargs = {"monitor_time": monitor_time}
    base_func_name = get_stock_real_time_sector_capital.__name__
    return exchange_explain(common_func_obj.get_common_func(sector, base_func_name, **kwargs), is_explain)
