from typing import Dict, List, Union
import pandas as pd
from ..common import get_history as get_history_data_for_stock
from ..common import get_real_time

def get_history_data(
        stock_codes: Union[str, List[str]],
        beg: str = '19000101',
        end: str = '20500101',
        klt: int = 101,
        fqt: int = 1,
        **kwargs,
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    获取股票的 K 线数据

    Parameters
    ----------
    stock_codes : Union[str,List[str]]
        股票代码、名称 或者 股票代码、名称构成的列表
    beg : str, optional
        开始日期，默认为 ``'19000101'`` ，表示 1900年1月1日
    end : str, optional
        结束日期，默认为 ``'20500101'`` ，表示 2050年1月1日
    klt : int, optional
        行情之间的时间间隔，默认为 ``101`` ，可选示例如下

        - ``1`` : 分钟
        - ``5`` : 5 分钟
        - ``15`` : 15 分钟
        - ``30`` : 30 分钟
        - ``60`` : 60 分钟
        - ``101`` : 日
        - ``102`` : 周
        - ``103`` : 月

    fqt : int, optional
        复权方式，默认为 ``1`` ，可选示例如下

        - ``0`` : 不复权
        - ``1`` : 前复权
        - ``2`` : 后复权

    Returns
    -------
    Union[DataFrame, Dict[str, DataFrame]]
        股票的 K 线数据

        - ``DataFrame`` : 当 ``stock_codes`` 是 ``str`` 时
        - ``Dict[str, DataFrame]`` : 当 ``stock_codes`` 是 ``List[str]`` 时

    Examples
    --------
    >>> import sharetop as ef
    >>> # 获取单只股票日 K 行情数据
    >>> ef.core.stock.get_history_data('600519')
        股票名称    股票代码          日期      开盘      收盘  ...    涨跌幅   涨跌额    换手率  盘后量  盘后额
            0     比亚迪  002594  2011-06-30   20.75   24.20  ...  44.48  7.45  87.96    0    0
            1     比亚迪  002594  2011-07-01   24.52   26.75  ...  10.54  2.55  52.44    0    0
            2     比亚迪  002594  2011-07-04   27.63   29.55  ...  10.47  2.80  34.32    0    0
            3     比亚迪  002594  2011-07-05   31.53   31.80  ...   7.61  2.25  59.54    0    0
            4     比亚迪  002594  2011-07-06   31.55   32.15  ...   1.10  0.35  48.90    0    0
            ...   ...     ...         ...     ...     ...  ...    ...   ...    ...  ...  ...
            2846  比亚迪  002594  2023-04-03  256.00  255.92  ...  -0.04 -0.10   1.15    0    0
            2847  比亚迪  002594  2023-04-04  255.81  250.92  ...  -1.95 -5.00   1.18    0    0
            2848  比亚迪  002594  2023-04-06  248.00  250.00  ...  -0.37 -0.92   0.70    0    0
            2849  比亚迪  002594  2023-04-07  250.05  249.28  ...  -0.29 -0.72   0.59    0    0
            2850  比亚迪  002594  2023-04-10  249.28  251.00  ...   0.69  1.72   0.84    0    0

    >>> # 获取多只股票历史行情
    >>> stock_df = ef.core.stock.get_history_data(['600519','300750'])
    >>> type(stock_df)
    <class 'dict'>
    >>> stock_df.keys()
    dict_keys(['300750', '600519'])
    >>> stock_df['002594']
             股票名称    股票代码          日期      开盘      收盘  ...    涨跌幅   涨跌额    换手率  盘后量  盘后额
            0     比亚迪  002594  2011-06-30   20.75   24.20  ...  44.48  7.45  87.96    0    0
            1     比亚迪  002594  2011-07-01   24.52   26.75  ...  10.54  2.55  52.44    0    0
            2     比亚迪  002594  2011-07-04   27.63   29.55  ...  10.47  2.80  34.32    0    0
            3     比亚迪  002594  2011-07-05   31.53   31.80  ...   7.61  2.25  59.54    0    0
            4     比亚迪  002594  2011-07-06   31.55   32.15  ...   1.10  0.35  48.90    0    0
            ...   ...     ...         ...     ...     ...  ...    ...   ...    ...  ...  ...
            2846  比亚迪  002594  2023-04-03  256.00  255.92  ...  -0.04 -0.10   1.15    0    0
            2847  比亚迪  002594  2023-04-04  255.81  250.92  ...  -1.95 -5.00   1.18    0    0
            2848  比亚迪  002594  2023-04-06  248.00  250.00  ...  -0.37 -0.92   0.70    0    0
            2849  比亚迪  002594  2023-04-07  250.05  249.28  ...  -0.29 -0.72   0.59    0    0
            2850  比亚迪  002594  2023-04-10  249.28  251.00  ...   0.69  1.72   0.84    0    0
    """
    df = get_history_data_for_stock(
        stock_codes, beg=beg, end=end, klt=klt, fqt=fqt, **kwargs
    )
    if isinstance(df, pd.DataFrame):
        df.rename(columns={'代码': '股票代码', '名称': '股票名称'}, inplace=True)
    elif isinstance(df, dict):
        for stock_code in df.keys():
            df[stock_code].rename(columns={'代码': '股票代码', '名称': '股票名称'}, inplace=True)
    return df


def get_real_time_data(
        stock_codes: Union[str, List[str]],
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    df = get_real_time(stock_codes)
    print(df)
