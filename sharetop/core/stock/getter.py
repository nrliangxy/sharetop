from typing import Dict, List, Union
import pandas as pd
from ..common import get_history as get_history_data_for_stock
from ..common import get_real_time
from ..common.config import FS_DICT
from ..common import get_market_realtime_by_fs
from ..utils import to_numeric, process_dataframe_and_series, validate_request


@validate_request
def get_stock_kline_data(
        token: str,
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


def get_stock_real_time_data(
        stock_codes: Union[str, List[str]],
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    获取单个或者多个股票的实时股价
    :param stock_codes: 单个或者多个股票代码
    也可以是1.000001 0为深证，1为上证， 116为港股
    :return: 获取单个或者多个股票的实时股价和相关信息
    """
    df = get_real_time(stock_codes)
    return df


@process_dataframe_and_series(remove_columns_and_indexes=['市场编号'])
@to_numeric
def get_stock_market_real_time_data(fs: Union[str, List[str]] = None, **kwargs) -> pd.DataFrame:
    """
        获取单个或者多个市场行情的最新状况

        Parameters
        ----------
        fs : Union[str, List[str]], optional
            行情名称或者多个行情名列表 可选值及示例如下

            - ``None``  沪深京A股市场行情
            - ``'沪深A股'`` 沪深A股市场行情
            - ``'沪A'`` 沪市A股市场行情
            - ``'深A'`` 深市A股市场行情
            - ``北A``   北证A股市场行情
            - ``'可转债'``  沪深可转债市场行情
            - ``'期货'``    期货市场行情
            - ``'创业板'``  创业板市场行情
            - ``'美股'``    美股市场行情
            - ``'港股'``    港股市场行情
            - ``'中概股'``  中国概念股市场行情
            - ``'新股'``    沪深新股市场行情
            - ``'科创板'``  科创板市场行情
            - ``'沪股通'``  沪股通市场行情
            - ``'深股通'``  深股通市场行情
            - ``'行业板块'``    行业板块市场行情
            - ``'概念板块'``    概念板块市场行情
            - ``'沪深系列指数'``    沪深系列指数市场行情
            - ``'上证系列指数'``    上证系列指数市场行情
            - ``'深证系列指数'``    深证系列指数市场行情
            - ``'ETF'`` ETF 基金市场行情
            - ``'LOF'`` LOF 基金市场行情


        Returns
        -------
        DataFrame
            单个或者多个市场行情的最新状况

        Raises
        ------
        KeyError
            当参数 ``fs`` 中含有不正确的行情类型时引发错误

        Examples
        --------
                股票代码   股票名称     涨跌幅     最新价      最高      最低      今开     涨跌额    换手率    量比    动态市盈率     成交量           成交额   昨日收盘           总市值         流通市值      行情ID 市场类型
        0     688787    N海天  277.59  139.48  172.39  139.25  171.66  102.54  85.62     -    78.93   74519  1110318832.0  36.94    5969744000   1213908667  1.688787   沪A
        1     301045    N天禄  149.34   39.42   48.95    39.2   48.95   23.61  66.66     -    37.81  163061   683878656.0  15.81    4066344240    964237089  0.301045   深A
        2     300532   今天国际   20.04   12.16   12.16   10.69   10.69    2.03   8.85  3.02   -22.72  144795   171535181.0  10.13    3322510580   1989333440  0.300532   深A
        3     300600   国瑞科技   20.02   13.19   13.19   11.11   11.41     2.2  18.61  2.82   218.75  423779   541164432.0  10.99    3915421427   3003665117  0.300600   深A
        4     300985   致远新能   20.01   47.08   47.08    36.8    39.4    7.85  66.65  2.17    58.37  210697   897370992.0  39.23    6277336472   1488300116  0.300985   深A
        ...      ...    ...     ...     ...     ...     ...     ...     ...    ...   ...      ...     ...           ...    ...           ...          ...       ...  ...
        4598  603186   华正新材   -10.0   43.27   44.09   43.27   43.99   -4.81   1.98  0.48    25.24   27697   120486294.0  48.08    6146300650   6063519472  1.603186   沪A
        4599  688185  康希诺-U  -10.11   476.4  534.94  460.13   530.0   -53.6   6.02  2.74 -2088.07   40239  1960540832.0  530.0  117885131884  31831479215  1.688185   沪A
        4600  688148   芳源股份  -10.57    31.3   34.39    31.3    33.9    -3.7  26.07  0.56   220.01  188415   620632512.0   35.0   15923562000   2261706043  1.688148   沪A
        4601  300034   钢研高纳  -10.96   43.12   46.81   42.88    46.5   -5.31   7.45  1.77    59.49  323226  1441101824.0  48.43   20959281094  18706911861  0.300034   深A
        4602  300712   永福股份  -13.71    96.9  110.94    95.4   109.0   -15.4   6.96  1.26   511.21  126705  1265152928.0  112.3   17645877600  17645877600  0.300712   深A

            股票代码    股票名称    涨跌幅    最新价     最高     最低     今开    涨跌额   换手率     量比   动态市盈率       成交量         成交额   昨日收盘         总市值        流通市值       行情ID  市场类型
        0     00859  中昌国际控股  49.02   0.38   0.38   0.26   0.26  0.125  0.08  86.85   -2.83    938000    262860.0  0.255   427510287   427510287  128.00859  None
        1     01058    粤海制革  41.05   1.34   1.51    0.9   0.93   0.39  8.34   1.61  249.89  44878000  57662440.0   0.95   720945460   720945460  128.01058  None
        2     00713  世界(集团)  27.94   0.87    0.9   0.68   0.68   0.19  1.22  33.28    3.64   9372000   7585400.0   0.68   670785156   670785156  128.00713  None
        3     08668    瀛海集团  24.65  0.177  0.179  0.145  0.145  0.035   0.0   10.0   -9.78     20000      3240.0  0.142   212400000   212400000  128.08668  None
        4     08413    亚洲杂货  24.44   0.28   0.28   0.25   0.25  0.055  0.01   3.48  -20.76    160000     41300.0  0.225   325360000   325360000  128.08413  None
        ...     ...     ...    ...    ...    ...    ...    ...    ...   ...    ...     ...       ...         ...    ...         ...         ...        ...   ...
        5632  08429    冰雪集团 -16.75  0.174    0.2  0.166    0.2 -0.035  2.48   3.52  -21.58  11895000   2074645.0  0.209    83520000    83520000  128.08429  None
        5633  00524    长城天下 -17.56  0.108  0.118  0.103  0.118 -0.023  0.45  15.43   -6.55   5961200    649171.0  0.131   141787800   141787800  128.00524  None
        5634  08377    申酉控股 -17.71  0.395   0.46   0.39   0.46 -0.085  0.07   8.06   -5.07    290000    123200.0   0.48   161611035   161611035  128.08377  None
        5635  00108    国锐地产 -19.01   1.15   1.42   1.15   1.42  -0.27  0.07   0.78   23.94   2376000   3012080.0   1.42  3679280084  3679280084  128.00108  None
        5636  08237    华星控股  -25.0  0.024  0.031  0.023  0.031 -0.008  0.43   8.74   -2.01  15008000    364188.0  0.032    83760000    83760000  128.08237  None

            股票代码         股票名称   涨跌幅    最新价     最高     最低     今开    涨跌额    换手率    量比 动态市盈率       成交量           成交额   昨日收盘          总市值         流通市值      行情ID 市场类型
        0    513050     中概互联网ETF  4.49  1.444  1.455  1.433  1.452  0.062   6.71  0.92     -  12961671  1870845984.0  1.382  27895816917  27895816917  1.513050   沪A
        1    513360        教育ETF  4.38    0.5  0.502  0.486  0.487  0.021  16.89   1.7     -   1104254    54634387.0  0.479    326856952    326856952  1.513360   沪A
        2    159766        旅游ETF  3.84  0.974  0.988   0.95   0.95  0.036  14.46  1.97     -    463730    45254947.0  0.938    312304295    312304295  0.159766   深A
        3    159865        养殖ETF   3.8  0.819  0.828  0.785  0.791   0.03  12.13  0.89     -   1405871   114254714.0  0.789    949594189    949594189  0.159865   深A
        4    516670      畜牧养殖ETF  3.76  0.856  0.864  0.825  0.835  0.031  24.08  0.98     -    292027    24924513.0  0.825    103803953    103803953  1.516670   沪A
        ..      ...          ...   ...    ...    ...    ...    ...    ...    ...   ...   ...       ...           ...    ...          ...          ...       ...  ...
        549  513060      恒生医疗ETF -4.12  0.861  0.905   0.86  0.902 -0.037  47.96  1.57     -   1620502   141454355.0  0.898    290926128    290926128  1.513060   沪A
        550  515220        煤炭ETF -4.46  2.226  2.394  2.194  2.378 -0.104  14.39  0.98     -   2178176   487720560.0  2.330   3369247992   3369247992  1.515220   沪A
        551  513000  日经225ETF易方达 -4.49  1.212  1.269   1.21  1.269 -0.057   5.02  2.49     -     25819     3152848.0  1.269     62310617     62310617  1.513000   沪A
        552  513880     日经225ETF -4.59  1.163  1.224  1.162  1.217 -0.056  16.93  0.94     -     71058     8336846.0  1.219     48811110     48811110  1.513880   沪A
        553  513520        日经ETF -4.76    1.2  1.217  1.196  1.217  -0.06   27.7  1.79     -    146520    17645828.0  1.260     63464640     63464640  1.513520   沪A

        Notes
        -----
        无论股票、可转债、期货还是基金。第一列表头始终叫 ``股票代码``
        """
    fs_list: List[str] = []
    if fs is None:
        fs_list.append(FS_DICT['stock'])

    if isinstance(fs, str):
        fs = [fs]

    if isinstance(fs, list):

        for f in fs:
            if not FS_DICT.get(f):
                raise KeyError(f'指定的行情参数 `{fs}` 不正确')
            fs_list.append(FS_DICT[f])
        # 给空列表时 试用沪深A股行情
        if not fs_list:
            fs_list.append(FS_DICT['stock'])
    fs_str = ','.join(fs_list)
    df = get_market_realtime_by_fs(fs_str, **kwargs)
    df.rename(columns={'代码': '股票代码', '名称': '股票名称'}, inplace=True)

    return df
