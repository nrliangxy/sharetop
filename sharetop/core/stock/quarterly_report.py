import rich
import pandas as pd
from ..utils import to_numeric, requests_obj, validate_request
from typing import List, Union
from jsonpath import jsonpath
from ...crawl.settings import *
from ..common.getter import get_company_report
from ..common.explain_change import exchange_explain


@validate_request
def get_stock_all_report_dates(token: str, is_explain: bool = False) -> pd.DataFrame:
    """
    获取沪深市场的全部股票报告期信息

    Returns
    -------
    DataFrame
        沪深市场的全部股票报告期信息

    Examples
    --------
            报告日期       季报名称
    0   2021-06-30  2021年 半年报
    1   2021-03-31  2021年 一季报
    2   2020-12-31   2020年 年报
    3   2020-09-30  2020年 三季报
    4   2020-06-30  2020年 半年报
    5   2020-03-31  2020年 一季报
    6   2019-12-31   2019年 年报
    7   2019-09-30  2019年 三季报
    8   2019-06-30  2019年 半年报
    9   2019-03-31  2019年 一季报
    10  2018-12-31   2018年 年报
    11  2018-09-30  2018年 三季报
    12  2018-06-30  2018年 半年报
    13  2018-03-31  2018年 一季报
    14  2017-12-31   2017年 年报
    15  2017-09-30  2017年 三季报
    16  2017-06-30  2017年 半年报
    17  2017-03-31  2017年 一季报
    18  2016-12-31   2016年 年报
    19  2016-09-30  2016年 三季报
    20  2016-06-30  2016年 半年报
    21  2016-03-31  2016年 一季报
    22  2015-12-31   2015年 年报
    24  2015-06-30  2015年 半年报
    25  2015-03-31  2015年 一季报
    26  2014-12-31   2014年 年报
    27  2014-09-30  2014年 三季报
    28  2014-06-30  2014年 半年报
    29  2014-03-31  2014年 一季报
    30  2013-12-31   2013年 年报
    31  2013-09-30  2013年 三季报
    32  2013-06-30  2013年 半年报
    33  2013-03-31  2013年 一季报
    34  2012-12-31   2012年 年报
    35  2012-09-30  2012年 三季报
    36  2012-06-30  2012年 半年报
    37  2012-03-31  2012年 一季报
    38  2011-12-31   2011年 年报
    39  2011-09-30  2011年 三季报

    """
    fields = {'REPORT_DATE': '报告日期', 'DATATYPE': '季报名称'}
    params = (
        ('type', 'RPT_LICO_FN_CPD_BBBQ'),
        ('sty', ','.join(fields.keys())),
        ('p', '1'),
        ('ps', '2000'),
    )
    url = 'https://datacenter.eastmoney.com/securities/api/data/get'
    response = requests_obj.get(url, params, user_agent=True)
    items = jsonpath(response.json(), '$..data[:]')
    if not items:
        pd.DataFrame(columns=fields.values())
    df = pd.DataFrame(items)
    df = df.rename(columns=fields)
    df['报告日期'] = df['报告日期'].apply(lambda x: x.split()[0])
    return exchange_explain(df, is_explain)


@validate_request
@to_numeric
def get_stock_company_report_data(token: str, stock_codes: Union[str, List[str]], report_class: str = None,
                                  is_explain: bool = False) -> pd.DataFrame:
    """
    获取单个或者多个上市公司历史年报
    :param is_explain: 是否需要翻译
    :param token:
    :param stock_codes: 指定的单个公司或者多个公司
    :param report_class: 默认为空是全部，剩余参数可以为：“一季报”，“半年报”，“三季报”，“年报”
    :return:
    """
    return exchange_explain(get_company_report(stock_codes, report_class), is_explain)



@validate_request
@to_numeric
def get_stock_all_company_quarterly_report(token: str, date: str = None, is_explain: bool = False) -> pd.DataFrame:
    """
    获取沪深市场股票某一季度的表现情况
    Parameters
    ----------
    date : str, optional
        报告发布日期 部分可选示例如下(默认为 ``None``)

        - ``None`` : 最新季报
        - ``'2021-06-30'`` : 2021 年 Q2 季度报
        - ``'2021-03-31'`` : 2021 年 Q1 季度报

    Returns
    -------
    DataFrame
        获取沪深市场股票某一季度的表现情况

    Examples
    ---------
            股票代码  股票简称                 公告日期          营业收入   营业收入同比增长  营业收入季度环比           净利润     净利润同比增长   净利润季度环比    每股收益      每股净资产  净资产收益率      销售毛利率  每股经营现金流量
    0     688981  中芯国际  2021-08-28 00:00:00  1.609039e+10  22.253453   20.6593  5.241321e+09  278.100000  307.8042  0.6600  11.949525    5.20  26.665642  1.182556
    1     688819  天能股份  2021-08-28 00:00:00  1.625468e+10   9.343279   23.9092  6.719446e+08  -14.890000  -36.8779  0.7100  11.902912    6.15  17.323263 -1.562187
    2     688789  宏华数科  2021-08-28 00:00:00  4.555604e+08  56.418441    6.5505  1.076986e+08   49.360000   -7.3013  1.8900  14.926761   13.51  43.011243  1.421272
    3     688681  科汇股份  2021-08-28 00:00:00  1.503343e+08  17.706987  121.9407  1.664509e+07  -13.100000  383.3331  0.2100   5.232517    4.84  47.455511 -0.232395
    4     688670   金迪克  2021-08-28 00:00:00  3.209423e+07 -63.282413  -93.1788 -2.330505e+07 -242.275001 -240.1554 -0.3500   3.332254  -10.10  85.308531  1.050348
    ...      ...   ...                  ...           ...        ...       ...           ...         ...       ...     ...        ...     ...        ...       ...
    3720  600131  国网信通  2021-07-16 00:00:00  2.880378e+09   6.787087   69.5794  2.171389e+08   29.570000  296.2051  0.1800   4.063260    4.57  19.137437 -0.798689
    3721  600644  乐山电力  2021-07-15 00:00:00  1.257030e+09  18.079648    5.7300  8.379727e+07  -14.300000   25.0007  0.1556   3.112413    5.13  23.645137  0.200906
    3722  002261  拓维信息  2021-07-15 00:00:00  8.901777e+08  47.505282   24.0732  6.071063e+07   68.320000   30.0596  0.0550   2.351598    2.37  37.047968 -0.131873
    3723  601952  苏垦农发  2021-07-13 00:00:00  4.544138e+09  11.754570   47.8758  3.288132e+08    1.460000   83.1486  0.2400   3.888046    6.05  15.491684 -0.173772
    3724  601568  北元集团  2021-07-09 00:00:00  6.031506e+09  32.543303   30.6352  1.167989e+09   61.050000   40.8165  0.3200   3.541533    9.01  27.879243  0.389860


            股票代码  股票简称                 公告日期          营业收入  营业收入同比增长  营业收入季度环比           净利润     净利润同比增长  净利润季度环比    每股收益      每股净资产  净资产收益率      销售毛利率  每股经营现金流量
    0     605033  美邦股份  2021-08-25 00:00:00  2.178208e+08       NaN       NaN  4.319814e+07         NaN      NaN  0.4300        NaN     NaN  37.250416       NaN
    1     301048  金鹰重工  2021-07-30 00:00:00  9.165528e+07       NaN       NaN -2.189989e+07         NaN      NaN     NaN        NaN   -1.91  20.227118       NaN
    2     001213  中铁特货  2021-07-29 00:00:00  1.343454e+09       NaN       NaN -3.753634e+07         NaN      NaN -0.0100        NaN     NaN  -1.400708       NaN
    3     605588  冠石科技  2021-07-28 00:00:00  1.960175e+08       NaN       NaN  1.906751e+07         NaN      NaN  0.3500        NaN     NaN  16.324650       NaN
    4     688798  艾为电子  2021-07-27 00:00:00  2.469943e+08       NaN       NaN  2.707568e+07         NaN      NaN  0.3300        NaN    8.16  33.641934       NaN
    ...      ...   ...                  ...           ...       ...       ...           ...         ...      ...     ...        ...     ...        ...       ...
    4440  603186  华正新材  2020-04-09 00:00:00  4.117502e+08 -6.844813  -23.2633  1.763252e+07   18.870055 -26.3345  0.1400   5.878423    2.35  18.861255  0.094249
    4441  002838  道恩股份  2020-04-09 00:00:00  6.191659e+08 -8.019810  -16.5445  6.939886e+07   91.601624  76.7419  0.1700   2.840665    6.20  22.575224  0.186421
    4442  600396  金山股份  2020-04-08 00:00:00  2.023133e+09  0.518504   -3.0629  1.878432e+08  114.304022  61.2733  0.1275   1.511012    8.81  21.422393  0.085698
    4443  002913   奥士康  2020-04-08 00:00:00  4.898977e+08 -3.883035  -23.2268  2.524717e+07  -47.239162 -58.8136  0.1700  16.666749    1.03  22.470020  0.552624
    4444  002007  华兰生物  2020-04-08 00:00:00  6.775414e+08 -2.622289  -36.1714  2.472864e+08   -4.708821 -22.6345  0.1354   4.842456    3.71  61.408522  0.068341

    Notes
    -----
    :param is_explain:
    :param date:
    :param token:

    """
    # TODO 加速
    fields = {
        'SECURITY_CODE': '股票代码',
        'SECURITY_NAME_ABBR': '股票简称',
        'NOTICE_DATE': '公告日期',
        'TOTAL_OPERATE_INCOME': '营业收入',
        'YSTZ': '营业收入同比增长',
        'YSHZ': '营业收入季度环比',
        'PARENT_NETPROFIT': '净利润',
        'SJLTZ': '净利润同比增长',
        'SJLHZ': '净利润季度环比',
        'BASIC_EPS': '每股收益',
        'BPS': '每股净资产',
        'WEIGHTAVG_ROE': '净资产收益率',
        'XSMLL': '销售毛利率',
        'MGJYXJJE': '每股经营现金流量'
        # 'ISNEW':'是否最新'
    }

    dates = get_stock_all_report_dates(token)['report_date'].to_list()
    if date is None:
        date = dates[0]
    if date not in dates:
        rich.print('日期输入有误，可选日期如下:')
        rich.print(dates)
        return pd.DataFrame(columns=fields.values())

    date = f"(REPORTDATE=\'{date}\')"
    page = 1
    dfs: List[pd.DataFrame] = []
    while 1:
        params = (
            ('st', 'NOTICE_DATE,SECURITY_CODE'),
            ('sr', '-1,-1'),
            ('ps', '500'),
            ('p', f'{page}'),
            ('type', 'RPT_LICO_FN_CPD'),
            ('sty', 'ALL'),
            ('token', '894050c76af8597a853f5b408b759f5d'),
            # ! 只选沪深A股
            ('filter', f'(SECURITY_TYPE_CODE in ("058001001","058001008")){date}'),
        )
        url = "".join(quarterly_report_url_list)
        response = requests_obj.get(url, params, user_agent=True)
        items = jsonpath(response.json(), '$..data[:]')
        if not items:
            break
        df = pd.DataFrame(items)
        dfs.append(df)
        page += 1
    if len(dfs) == 0:
        df = pd.DataFrame(columns=fields.values())
        return df
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df = df.rename(columns=fields)[fields.values()]
    return exchange_explain(df, is_explain)
