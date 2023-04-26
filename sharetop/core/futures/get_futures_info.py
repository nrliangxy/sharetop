import pandas as pd
from ..common.config import FS_DICT
from ..common.getter import get_market_realtime_by_fs, get_deal_detail
from ..utils import process_dataframe_and_series


def get_futures_base_info() -> pd.DataFrame:
    """
    获取四个交易所全部期货基本信息
    Returns
    -------
    DataFrame
        四个交易所全部期货一些基本信息
    Examples
    --------
        期货代码      期货名称        行情ID       市场类型
    0       ZCM     动力煤主力     115.ZCM        郑商所
    1     ZC201    动力煤201   115.ZC201        郑商所
    2        jm      焦炭主力      114.jm        大商所
    3     j2201    焦炭2201   114.j2201        大商所
    4       jmm      焦煤主力     114.jmm        大商所
    ..      ...       ...         ...        ...
    846  jm2109    焦煤2109  114.jm2109        大商所
    847  071108    IH2108    8.071108        中金所
    848  070131   IH次主力合约    8.070131        中金所
    849  070120    IH当月连续     8.07012        中金所
    850  lu2109  低硫燃油2109  142.lu2109  上海能源期货交易所
    Notes
    -----
    这里的 行情ID 主要作用是为使用函数 ``efinance.futures.get_quote_history``
    获取期货行情信息提供参数
    """
    columns = ['期货代码', '期货名称', '行情ID', '市场类型']
    df = get_realtime_quotes()
    df = df[columns]
    return df


@process_dataframe_and_series(remove_columns_and_indexes=['市场编号'])
def get_realtime_quotes() -> pd.DataFrame:
    """
    获取期货最新行情总体情况

    Returns
    -------
    DataFrame
        期货市场的最新行情信息（涨跌幅、换手率等信息）

    Examples
    --------
        期货代码      期货名称   涨跌幅     最新价      最高      最低      今开    涨跌额 换手率    量比 动态市盈率     成交量            成交额    昨日收盘     总市值 流通市值        行情ID       市场类型
    0       ZCM     动力煤主力  6.28   836.6   843.8   796.8   796.8   49.4   -  2.82     -   82954   6850341376.0   793.0       -    -     115.ZCM        郑商所
    1     ZC201    动力煤201  6.28   836.6   843.8   796.8   796.8   49.4   -  2.82     -   82954   6850341376.0   793.0       -    -   115.ZC201        郑商所
    2        jm      焦炭主力  5.39  2980.0  2982.0  2833.0  2834.0  152.5   -   1.4     -  166433  48567923456.0  2830.5       -    -      114.jm        大商所
    3     j2201    焦炭2201  5.39  2980.0  2982.0  2833.0  2834.0  152.5   -   1.4     -  166433  48567923456.0  2830.5       -    -   114.j2201        大商所
    4       jmm      焦煤主力   5.0  2354.0  2360.0  2221.0  2221.0  112.0   -  1.42     -  238671  32924591872.0  2238.0       -    -     114.jmm        大商所
    ..      ...       ...   ...     ...     ...     ...     ...    ...  ..   ...   ...     ...            ...     ...     ...  ...         ...        ...
    846  jm2109    焦煤2109 -2.28  2748.0  2882.5  2688.0  2845.0  -64.0   -  1.85     -   34029   5656982528.0  2866.0       -    -  114.jm2109        大商所
    847  071108    IH2108 -2.52  3060.0  3130.0  3043.0  3111.2  -79.0   -  0.39     -   14384  13315567616.0  3139.2  918000    -    8.071108        中金所
    848  070131   IH次主力合约 -2.52  3060.0  3130.0  3043.0  3111.2  -79.0   -  0.57     -   14384  13315567616.0  3139.2  918000    -    8.070131        中金所
    849  070120    IH当月连续 -2.52  3060.0  3130.0  3043.0  3111.2  -79.0   -  0.39     -   14384  13315567616.0  3139.2  918000    -    8.070120        中金所
    850  lu2109  低硫燃油2109 -3.79  3123.0  3127.0  3121.0  3121.0 -123.0   -     -     -      22       687420.0  3143.0       -    -  142.lu2109  上海能源期货交易所

    Notes
    -----
    如果不记得行情ID,则可以调用函数 ``efinance.futures.get_realtime_quotes`` 获取
    接着便可以使用函数 ``efinance.futures.get_quote_history``
    来获取期货 K 线数据
    """
    fs = FS_DICT['futures']
    df = get_market_realtime_by_fs(fs)
    df = df.rename(columns={'代码': '期货代码', '名称': '期货名称'})
    return df


def get_future_deal_detail(quote_id: str, max_count: int = 1000000) -> pd.DataFrame:
    """
    获取期货最新交易日成交明细

    Parameters
    ----------
    quote_id : str
        期货行情ID
    max_count : int, optional
        最大返回条数,  默认为 ``1000000``

    Returns
    -------
    DataFrame
        期货最新交易日成交明细

    Notes
    -----
    行情ID 格式参考 ``efinance.futures.get_futures_base_info`` 中得到的数据

    Examples
    --------
        期货名称 期货代码        时间   昨收    成交价  成交量     单数
    0  动力煤主力  ZCM  21:00:00  0.0  879.0   23    0.0
    1  动力煤主力  ZCM  21:00:00  0.0  879.0    0 -373.0
    2  动力煤主力  ZCM  21:00:00  0.0  879.0    0    0.0

    """
    df = get_deal_detail(quote_id, max_count=max_count)
    df.rename(columns={'代码': '期货代码', '名称': '期货名称'}, inplace=True)
    return df
