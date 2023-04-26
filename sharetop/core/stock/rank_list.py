import pandas as pd
from datetime import datetime, timedelta
from retry import retry
from tqdm import tqdm
from ..utils import to_numeric, requests_obj
from typing import Dict, List, Union
from jsonpath import jsonpath
from .config import (
    EASTMONEY_STOCK_BASE_INFO_FIELDS,
    EASTMONEY_STOCK_DAILY_BILL_BOARD_FIELDS,
)
from ...crawl.settings import *


@to_numeric
@retry(tries=3)
def get_daily_billboard(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    获取指定日期区间的龙虎榜详情数据

    Parameters
    ----------
    start_date : str, optional
        开始日期
        部分可选示例如下

        - ``None`` 最新一个榜单公开日(默认值)
        - ``"2021-08-27"`` 2021年8月27日

    end_date : str, optional
        结束日期
        部分可选示例如下

        - ``None`` 最新一个榜单公开日(默认值)
        - ``"2021-08-31"`` 2021年8月31日

    Returns
    -------
    DataFrame
        龙虎榜详情数据

    Examples
    --------
        股票代码  股票名称        上榜日期                解读     收盘价      涨跌幅      换手率        龙虎榜净买额        龙虎榜买入额        龙虎榜卖出额        龙虎榜成交额      市场总成交额  净买额占总成交比   成交额占总成交比          流通市值                                  上榜原因
    0   000608  阳光股份  2021-08-27    卖一主卖，成功率48.36%    3.73  -9.9034   3.8430 -8.709942e+06  1.422786e+07  2.293780e+07  3.716565e+07   110838793 -7.858208  33.531268  2.796761e+09                      日跌幅偏离值达到7%的前5只证券
    1   000751  锌业股份  2021-08-27    主力做T，成功率18.84%    5.32  -2.9197  19.6505 -1.079219e+08  5.638899e+07  1.643109e+08  2.206999e+08  1462953973 -7.376984  15.085906  7.500502e+09                       日振幅值达到15%的前5只证券
    2   000762  西藏矿业  2021-08-27  北京资金买入，成功率39.42%   63.99   1.0741  15.6463  2.938758e+07  4.675541e+08  4.381665e+08  9.057206e+08  4959962598  0.592496  18.260633  3.332571e+10                       日振幅值达到15%的前5只证券
    3   000833  粤桂股份  2021-08-27  实力游资买入，成功率44.55%    8.87  10.0496   8.8263  4.993555e+07  1.292967e+08  7.936120e+07  2.086580e+08   895910429  5.573721  23.290046  3.353614e+09              连续三个交易日内，涨幅偏离值累计达到20%的证券
    4   001208  华菱线缆  2021-08-27  1家机构买入，成功率40.43%   19.72   4.3386  46.1985  4.055258e+07  1.537821e+08  1.132295e+08  2.670117e+08  1203913048  3.368398  22.178651  2.634710e+09                       日换手率达到20%的前5只证券
    ..     ...   ...         ...               ...     ...      ...      ...           ...           ...           ...           ...         ...       ...        ...           ...                                   ...
    70  688558  国盛智科  2021-08-27    买一主买，成功率38.71%   60.72   1.6064  34.0104  1.835494e+07  1.057779e+08  8.742293e+07  1.932008e+08   802569300  2.287023  24.072789  2.321743e+09              有价格涨跌幅限制的日换手率达到30%的前五只证券
    71  688596  正帆科技  2021-08-27  1家机构买入，成功率57.67%   26.72   3.1660   3.9065 -1.371039e+07  8.409046e+07  9.780085e+07  1.818913e+08   745137400 -1.839982  24.410438  4.630550e+09  有价格涨跌幅限制的连续3个交易日内收盘价格涨幅偏离值累计达到30%的证券
    72  688663   新风光  2021-08-27    卖一主卖，成功率37.18%   28.17 -17.6316  32.2409  1.036460e+07  5.416901e+07  4.380440e+07  9.797341e+07   274732700  3.772613  35.661358  8.492507e+08           有价格涨跌幅限制的日收盘价格跌幅达到15%的前五只证券
    73  688663   新风光  2021-08-27    卖一主卖，成功率37.18%   28.17 -17.6316  32.2409  1.036460e+07  5.416901e+07  4.380440e+07  9.797341e+07   274732700  3.772613  35.661358  8.492507e+08              有价格涨跌幅限制的日换手率达到30%的前五只证券
    74  688667  菱电电控  2021-08-27  1家机构卖出，成功率49.69%  123.37 -18.8996  17.7701 -2.079877e+06  4.611216e+07  4.819204e+07  9.430420e+07   268503400 -0.774618  35.122163  1.461225e+09           有价格涨跌幅限制的日收盘价格跌幅达到15%的前五只证券

        股票代码  股票名称        上榜日期                解读     收盘价      涨跌幅      换手率        龙虎榜净买额        龙虎榜买入额        龙虎榜卖出额        龙虎榜成交额      市场总成交额   净买额占总成交比    成交额占总成交比          流通市值                           上榜原因
    0    000608  阳光股份  2021-08-27    卖一主卖，成功率48.36%    3.73  -9.9034   3.8430 -8.709942e+06  1.422786e+07  2.293780e+07  3.716565e+07   110838793  -7.858208   33.531268  2.796761e+09               日跌幅偏离值达到7%的前5只证券
    1    000751  锌业股份  2021-08-27    主力做T，成功率18.84%    5.32  -2.9197  19.6505 -1.079219e+08  5.638899e+07  1.643109e+08  2.206999e+08  1462953973  -7.376984   15.085906  7.500502e+09                日振幅值达到15%的前5只证券
    2    000762  西藏矿业  2021-08-27  北京资金买入，成功率39.42%   63.99   1.0741  15.6463  2.938758e+07  4.675541e+08  4.381665e+08  9.057206e+08  4959962598   0.592496   18.260633  3.332571e+10                日振幅值达到15%的前5只证券
    3    000833  粤桂股份  2021-08-27  实力游资买入，成功率44.55%    8.87  10.0496   8.8263  4.993555e+07  1.292967e+08  7.936120e+07  2.086580e+08   895910429   5.573721   23.290046  3.353614e+09       连续三个交易日内，涨幅偏离值累计达到20%的证券
    4    001208  华菱线缆  2021-08-27  1家机构买入，成功率40.43%   19.72   4.3386  46.1985  4.055258e+07  1.537821e+08  1.132295e+08  2.670117e+08  1203913048   3.368398   22.178651  2.634710e+09                日换手率达到20%的前5只证券
    ..      ...   ...         ...               ...     ...      ...      ...           ...           ...           ...           ...         ...        ...         ...           ...                            ...
    414  605580  恒盛能源  2021-08-20    买一主买，成功率33.33%   13.28  10.0249   0.4086  2.413149e+06  2.713051e+06  2.999022e+05  3.012953e+06     2713051  88.945937  111.054054  6.640000e+08  有价格涨跌幅限制的日收盘价格涨幅偏离值达到7%的前三只证券
    415  688029  南微医学  2021-08-20  4家机构卖出，成功率55.82%  204.61 -18.5340   8.1809 -1.412053e+08  1.883342e+08  3.295394e+08  5.178736e+08   762045800 -18.529760   67.958326  9.001510e+09    有价格涨跌幅限制的日收盘价格跌幅达到15%的前五只证券
    416  688408   中信博  2021-08-20  4家机构卖出，成功率47.86%  179.98  -0.0666  15.3723 -4.336304e+07  3.750919e+08  4.184550e+08  7.935469e+08   846547400  -5.122340   93.739221  5.695886e+09      有价格涨跌幅限制的日价格振幅达到30%的前五只证券
    417  688556  高测股份  2021-08-20  上海资金买入，成功率60.21%   51.97  17.0495  10.6452 -3.940045e+07  1.642095e+08  2.036099e+08  3.678194e+08   575411600  -6.847351   63.922831  5.739089e+09    有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券
    418  688636   智明达  2021-08-20  2家机构买入，成功率47.37%  161.90  15.8332  11.9578  2.922406e+07  6.598126e+07  3.675721e+07  1.027385e+08   188330100  15.517464   54.552336  1.647410e+09    有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券
    """
    today = datetime.today().date()
    mode = 'auto'
    if start_date is None:
        start_date = today

    if end_date is None:
        end_date = today

    if isinstance(start_date, str):
        mode = 'user'
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        mode = 'user'
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    fields = EASTMONEY_STOCK_DAILY_BILL_BOARD_FIELDS
    bar: tqdm = None

    while 1:

        dfs: List[pd.DataFrame] = []
        page = 1
        while 1:
            params = (
                ('sortColumns', 'TRADE_DATE,SECURITY_CODE'),
                ('sortTypes', '-1,1'),
                ('pageSize', '500'),
                ('pageNumber', page),
                ('reportName', 'RPT_DAILYBILLBOARD_DETAILS'),
                ('columns', 'ALL'),
                ('source', 'WEB'),
                ('client', 'WEB'),
                ('filter', f"(TRADE_DATE<='{end_date}')(TRADE_DATE>='{start_date}')"),
            )

            url = ''.join(rank_list_list)
            response = requests_obj.get(
                url, params, user_agent=False
            )
            if bar is None:
                pages = jsonpath(response.json(), '$..pages')
                print("pages:", pages)
                if pages and pages[0] != 1:
                    total = pages[0]
                    bar = tqdm(total=int(total))
            if bar is not None:
                bar.update()

            items = jsonpath(response.json(), '$..data[:]')
            if not items:
                break
            page += 1
            df = pd.DataFrame(items).rename(columns=fields)[fields.values()]
            dfs.append(df)
        if mode == 'user':
            break
        if len(dfs) == 0:
            start_date = start_date - timedelta(1)
            end_date = end_date - timedelta(1)

        if len(dfs) > 0:
            break
    if len(dfs) == 0:
        df = pd.DataFrame(columns=fields.values())
        return df

    df = pd.concat(dfs, ignore_index=True)
    df['上榜日期'] = df['上榜日期'].astype('str').apply(lambda x: x.split(' ')[0])
    return df
