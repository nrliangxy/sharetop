## Introduction

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat)](https://pypi.python.org/pypi/efinance)
[![Pypi Package](https://img.shields.io/pypi/v/sharetop.svg?maxAge=60)](https://pypi.python.org/pypi/efinance)
[![Pypi-Install](https://img.shields.io/pypi/dm/sharetop.svg?maxAge=2592000&label=installs&color=%2327B1FF)](https://pypi.python.org/pypi/sharetop)
[![Docs](https://readthedocs.org/projects/sharetop/badge/?version=latest)](https://efinance.readthedocs.io)
[![CodeFactor](https://www.codefactor.io/repository/github/micro-sheep/efinance/badge)](https://www.codefactor.io/repository/github/micro-sheep/efinance/overview/main)
[![Github Stars](https://img.shields.io/github/stars/sharetop/sharetop.svg?style=social&label=Star&maxAge=60)](https://github.com/nrliangxy/sharetop)

[`efinance`](https://github.com/nrliangxy/sharetop) 是由个人打造的用于获取股票、基金、期货数据的免费开源 Python 库，你可以使用它很方便地获取数据以便更好地服务于个人的交易系统需求。

- [`Source Code`](https://github.com/nrliangxy/sharetop)

---

## Installation

- 通过 `pip` 安装

```bash
pip install sharetop
```

- 通过 `pip` 更新

```bash
pip install sharetop --upgrade
```


- 源码安装（用于开发）

```bash
git clone https://github.com/Micro-sheep/efinance
cd efinance
pip install -e .
```

---

## Examples

### Stock

- 获取股票历史日 K 线数据

```python
>>> import sharetop as sp
>>> # 股票代码
>>> stock_code = '600519'
>>> sp.stock.get_history_data(stock_code)
      股票名称    股票代码          日期       开盘       收盘       最高       最低       成交量           成交额    振幅   涨跌幅    涨跌额    换手率
0     贵州茅台  600519  2001-08-27   -89.74   -89.53   -89.08   -90.07  406318.0  1.410347e+09 -1.10  0.92   0.83  56.83
1     贵州茅台  600519  2001-08-28   -89.64   -89.27   -89.24   -89.72  129647.0  4.634630e+08 -0.54  0.29   0.26  18.13
2     贵州茅台  600519  2001-08-29   -89.24   -89.36   -89.24   -89.42   53252.0  1.946890e+08 -0.20 -0.10  -0.09   7.45
3     贵州茅台  600519  2001-08-30   -89.38   -89.22   -89.14   -89.44   48013.0  1.775580e+08 -0.34  0.16   0.14   6.72
4     贵州茅台  600519  2001-08-31   -89.21   -89.24   -89.12   -89.28   23231.0  8.623100e+07 -0.18 -0.02  -0.02   3.25
...    ...     ...         ...      ...      ...      ...      ...       ...           ...   ...   ...    ...    ...
4756  贵州茅台  600519  2021-07-23  1937.82  1900.00  1937.82  1895.09   47585.0  9.057762e+09  2.20 -2.06 -40.01   0.38
4757  贵州茅台  600519  2021-07-26  1879.00  1804.11  1879.00  1780.00   98619.0  1.789436e+10  5.21 -5.05 -95.89   0.79
4758  贵州茅台  600519  2021-07-27  1803.00  1712.89  1810.00  1703.00   86577.0  1.523081e+10  5.93 -5.06 -91.22   0.69
4759  贵州茅台  600519  2021-07-28  1703.00  1768.90  1788.20  1682.12   85369.0  1.479247e+10  6.19  3.27  56.01   0.68
4760  贵州茅台  600519  2021-07-29  1810.01  1740.00  1823.00  1734.34   51035.0  9.067345e+09  5.01 -1.63 -28.90   0.41

[4761 rows x 13 columns]
```

- 获取非 A 股的股票 K 线数据（支持输入股票名称以及代码）

```python
>>> import sharetop as sp
>>> # 股票代码
>>> stock_code = 'AAPL'
>>> sp.stock.get_history_data(stock_code)
     股票名称  股票代码          日期      开盘      收盘      最高      最低          成交量           成交额    振幅   涨跌幅   涨跌额   换手率
0      苹果  AAPL  1984-09-07   -5.37   -5.37   -5.36   -5.37    2981600.0  0.000000e+00  0.00  0.00  0.00  0.02
1      苹果  AAPL  1984-09-10   -5.37   -5.37   -5.36   -5.37    2346400.0  0.000000e+00 -0.19  0.00  0.00  0.01
2      苹果  AAPL  1984-09-11   -5.36   -5.36   -5.36   -5.36    5444000.0  0.000000e+00  0.00  0.19  0.01  0.03
3      苹果  AAPL  1984-09-12   -5.36   -5.37   -5.36   -5.37    4773600.0  0.000000e+00 -0.19 -0.19 -0.01  0.03
4      苹果  AAPL  1984-09-13   -5.36   -5.36   -5.36   -5.36    7429600.0  0.000000e+00  0.00  0.19  0.01  0.04
...   ...   ...         ...     ...     ...     ...     ...          ...           ...   ...   ...   ...   ...
8739   苹果  AAPL  2021-07-22  145.94  146.80  148.19  145.81   77338156.0  1.137623e+10  1.64  0.96  1.40  0.47
8740   苹果  AAPL  2021-07-23  147.55  148.56  148.72  146.92   71447416.0  1.058233e+10  1.23  1.20  1.76  0.43
8741   苹果  AAPL  2021-07-26  148.27  148.99  149.83  147.70   72434089.0  1.080774e+10  1.43  0.29  0.43  0.44
8742   苹果  AAPL  2021-07-27  149.12  146.77  149.21  145.55  104818578.0  1.540140e+10  2.46 -1.49 -2.22  0.63
8743   苹果  AAPL  2021-07-28  144.81  144.98  146.97  142.54  118931191.0  1.723188e+10  3.02 -1.22 -1.79  0.72

[8744 rows x 13 columns]

>>> # 股票名称
>>> stock_name = '微软'
>>> sp.stock.get_history_data(stock_name)
       股票名称  股票代码          日期      开盘      收盘      最高      最低           成交量           成交额    振幅   涨跌幅   涨跌额    换手率
0      微软  MSFT  1986-03-13  -20.74  -20.73  -20.73  -20.74  1.031789e+09  0.000000e+00  0.00  0.00  0.00  13.72
1      微软  MSFT  1986-03-14  -20.73  -20.73  -20.73  -20.73  3.081600e+08  0.000000e+00  0.00  0.00  0.00   4.10
2      微软  MSFT  1986-03-17  -20.73  -20.73  -20.73  -20.73  1.331712e+08  0.000000e+00  0.00  0.00  0.00   1.77
3      微软  MSFT  1986-03-18  -20.73  -20.73  -20.73  -20.73  6.776640e+07  0.000000e+00  0.00  0.00  0.00   0.90
4      微软  MSFT  1986-03-19  -20.73  -20.73  -20.73  -20.73  4.789440e+07  0.000000e+00  0.00  0.00  0.00   0.64
...   ...   ...         ...     ...     ...     ...     ...           ...           ...   ...   ...   ...    ...
8357   微软  MSFT  2021-07-22  283.84  286.14  286.42  283.42  2.338406e+07  6.677062e+09  1.07  1.68  4.74   0.31
8358   微软  MSFT  2021-07-23  287.37  289.67  289.99  286.50  2.276807e+07  6.578686e+09  1.22  1.23  3.53   0.30
8359   微软  MSFT  2021-07-26  289.00  289.05  289.69  286.64  2.317607e+07  6.685868e+09  1.05 -0.21 -0.62   0.31
8360   微软  MSFT  2021-07-27  289.43  286.54  289.58  282.95  3.360407e+07  9.599993e+09  2.29 -0.87 -2.51   0.45
8361   微软  MSFT  2021-07-28  288.99  286.22  290.15  283.83  3.356685e+07  9.638499e+09  2.21 -0.11 -0.32   0.45

[8362 rows x 13 columns]
```

- 获取 ETF K 线数据

```python
>>> import sharetop as sp
>>> # ETF 代码（以中概互联网 ETF 为例）
>>> etf_code = '513050'
>>> sp.stock.get_history_data(etf_code)
      股票名称    股票代码          日期     开盘     收盘     最高     最低         成交量           成交额    振幅   涨跌幅    涨跌额    换手率
0     中概互联网ETF  513050  2017-01-18  0.989  0.977  0.989  0.969    345605.0  3.381795e+07  0.00  0.00  0.000   0.26
1     中概互联网ETF  513050  2017-01-19  0.978  0.989  0.990  0.978    257716.0  2.542553e+07  1.23  1.23  0.012   0.19
2     中概互联网ETF  513050  2017-01-20  0.989  0.988  0.990  0.986     50980.0  5.043289e+06  0.40 -0.10 -0.001   0.04
3     中概互联网ETF  513050  2017-01-23  0.988  0.988  0.989  0.986     13739.0  1.356129e+06  0.30  0.00  0.000   0.01
4     中概互联网ETF  513050  2017-01-24  0.989  0.989  0.992  0.987     17937.0  1.774398e+06  0.51  0.10  0.001   0.01
...        ...     ...         ...    ...    ...    ...    ...         ...           ...   ...   ...    ...    ...
1097  中概互联网ETF  513050  2021-07-23  1.789  1.760  1.789  1.758   4427623.0  7.836530e+08  1.73 -1.51 -0.027   3.32
1098  中概互联网ETF  513050  2021-07-26  1.679  1.645  1.698  1.642  13035366.0  2.182816e+09  3.18 -6.53 -0.115   9.78
1099  中概互联网ETF  513050  2021-07-27  1.600  1.547  1.620  1.546  14269546.0  2.257610e+09  4.50 -5.96 -0.098  10.70
1100  中概互联网ETF  513050  2021-07-28  1.545  1.552  1.578  1.506  13141023.0  2.024106e+09  4.65  0.32  0.005   9.85
1101  中概互联网ETF  513050  2021-07-29  1.615  1.641  1.651  1.606  10658041.0  1.734404e+09  2.90  5.73  0.089   7.99

[1102 rows x 13 columns]
```

- 获取单只股票 5 分钟 K 线数据

```python
>>> import sharetop as sp
>>> # 股票代码
>>> stock_code = '600519'
>>> # 5 分钟
>>> frequency = 5
>>> sp.stock.get_history_data(stock_code, klt=frequency)
      股票名称    股票代码                日期       开盘       收盘       最高       最低     成交量          成交额    振幅   涨跌幅    涨跌额   换手率
0     贵州茅台  600519  2021-06-16 09:35  2172.71  2159.71  2175.71  2150.74  1885.0  411159309.0  1.15 -0.64 -14.00  0.02
1     贵州茅台  600519  2021-06-16 09:40  2156.69  2148.71  2160.48  2143.37  1238.0  268790684.0  0.79 -0.51 -11.00  0.01
2     贵州茅台  600519  2021-06-16 09:45  2149.79  2159.71  2160.69  2149.79   706.0  153631002.0  0.51  0.51  11.00  0.01
3     贵州茅台  600519  2021-06-16 09:50  2159.61  2148.87  2159.71  2148.87   586.0  127346502.0  0.50 -0.50 -10.84  0.00
4     贵州茅台  600519  2021-06-16 09:55  2148.87  2161.04  2163.71  2148.72   788.0  171491075.0  0.70  0.57  12.17  0.01
...    ...     ...               ...      ...      ...      ...      ...     ...          ...   ...   ...    ...   ...
1521  贵州茅台  600519  2021-07-29 13:50  1746.51  1746.09  1748.95  1746.01   738.0  128889575.0  0.17 -0.09  -1.49  0.01
1522  贵州茅台  600519  2021-07-29 13:55  1746.08  1742.01  1746.09  1741.96   831.0  144968679.0  0.24 -0.23  -4.08  0.01
1523  贵州茅台  600519  2021-07-29 14:00  1742.00  1739.58  1742.00  1739.58   864.0  150446840.0  0.14 -0.14  -2.43  0.01
1524  贵州茅台  600519  2021-07-29 14:05  1741.87  1740.00  1745.00  1738.88  1083.0  188427970.0  0.35  0.02   0.42  0.01
1525  贵州茅台  600519  2021-07-29 14:10  1740.00  1740.02  1740.10  1740.00    59.0   10315488.0  0.01  0.00   0.02  0.00

[1526 rows x 13 columns]
```

- 沪深市场 A 股最新状况

```python
>>> import sharetop as sp
>>> sp.stock.get_market_real_time()
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

[4603 rows x 18 columns]
```

- 获取单只股或者多只最新状况

```python
>>> import sharetop as sp
>>> stock_code = '30033'
>>> sp.stock.get_real_time_data(stock_code)
        股票名称    股票代码     最新价    最高价    最低价  ...  市盈率(TTM)    市净率     涨跌值  涨跌幅(%)  振幅(%)
0  同花顺  300033  174.92  198.0  172.3  ...     55.27  15.63 -0.2009   -10.3  13.18
>>> stock_code = ['300033', '516110']
>>> sp.stock.get_real_time_data(stock_code)
{'300033':   股票名称    股票代码     最新价    最高价    最低价  ...  市盈率(TTM)    市净率     涨跌值  涨跌幅(%)  振幅(%)
0  同花顺  300033  174.92  198.0  172.3  ...     55.27  15.63 -0.2009   -10.3  13.18

[1 rows x 23 columns], '516110':     股票名称    股票代码    最新价    最高价  ...   内盘(手)       涨跌值  涨跌幅(%)  振幅(%)
0  汽车ETF  516110  0.945  0.953  ...  466383  0.000023   0.249  0.358

[1 rows x 19 columns]}
```

- 股票龙虎榜

```python
>>> import sharetop as sp
>>> # 获取最新一个公开的龙虎榜数据(后面还有获取指定日期区间的示例代码)
>>> sp.stock.get_daily_billboard()
    股票代码   股票名称        上榜日期                解读  ...   净买额占总成交比    成交额占总成交比          流通市值
                上榜原因
0    000021    深科技  2023-04-26  4家机构卖出，成功率60.41%  ...   2.373821   31.288324  2.661389e+10                          日跌幅偏离值达到7%的前5只证券
1    000150  *ST宜康  2023-04-26    主力做T，成功率29.56%  ... -21.126097   78.093035  4.352347e+08  连续三个交易日内，跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券
2    000606  *ST顺利  2023-04-26  北京资金卖出，成功率42.63%  ... -44.344337  138.384208  7.811153e+08  连续三个交易日内，跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券
3    000620    新华联  2023-04-26  1家机构卖出，成功率35.81%  ... -24.580743   42.757218  2.863903e+09                  连续三个交易日内，跌幅偏离值累计达到20%的证券
4    000719   中原传媒  2023-04-26  2家机构买入，成功率45.96%  ...   5.265043   29.831509  9.119907e+09                           日振幅值达到15% 的前5只证券
..      ...    ...         ...               ...  ...        ...         ...           ...                                       ...
106  688580   伟思医疗  2023-04-26  1家机构买入，成功率46.20%  ...   0.680386   45.458772  1.916985e+09               有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券
107  832662   方盛股份  2023-04-26  普通席位买入，成功率33.33%  ...   7.829732   39.737402  1.787436e+08                          当日换手率达到20%的前5只股票
108  833394    民士达  2023-04-26  1家机构买入，成功率35.62%  ...  -0.423705   28.803391  4.664451e+08                          当日换手率达到20% 的前5只股票
109  872808   曙光数创  2023-04-26  1家机构买入，成功率28.49%  ... -10.998660   32.268764  3.259663e+09                        当日收盘价涨幅达到20%的前5只股票
110  900915   中路B股  2023-04-26  普通席位买入，成功率47.33%  ...  -4.542227   51.427620  5.588460e+09             有价格涨跌幅限制的日收盘价格涨幅偏离值达到7%的前五只证券

[111 rows x 16 columns]

>>> # 获取指定日期区间的龙虎榜数据
>>> start_date = '2023-04-07' # 开始日期
>>> end_date = '2023-04-25' # 结束日期
>>> sp.stock.get_daily_billboard(start_date = start_date,end_date = end_date)
           股票代码  股票名称        上榜日期                   解读    收盘价  ...        市场总成交额   净买额占总成交比   成交额占总成交比
 流通市值                         上榜原因
0    000521  长虹美菱  2023-04-25     3家机构买入，成功率36.54%   7.79  ...  7.065423e+08   2.079029  29.969549  7.207487e+09             日涨幅偏离值达到7%的前5只证券
1    000950  重药控股  2023-04-25     2家机构买入，成功率44.64%   7.03  ...  1.158314e+09   5.843986  29.801649  1.214914e+10             日涨幅偏离值达到7%的前5只证券
2    000950  重药控股  2023-04-25     2家机构买入，成功率43.67%   7.03  ...  1.737031e+09   3.719371  29.171036  1.214914e+10     连续三个交易日内，涨幅偏离值累计达到20%的证券
3    001269  欧晶科技  2023-04-25     4家机构卖出，成功率47.21%  95.46  ...  6.431845e+08 -11.481581  33.037047  3.279663e+09             日跌幅偏离值达到7%的前5只证券
4    001337  四川黄金  2023-04-25  西藏自治区资金买入，成功率37.01%  41.25  ...  9.748661e+08   1.426310  15.850799  2.475000e+09              日 换手率达到20%的前5只证券
..      ...   ...         ...                  ...    ...  ...           ...        ...        ...           ...                          ...
820  688112  鼎阳科技  2023-04-07     2家机构买入，成功率44.20%  89.56  ...  2.652485e+08 -13.693809  85.027009  2.650262e+09  有价格涨跌幅限制的 日收盘价格涨幅达到15%的前五只证券
821  688197  首药控股  2023-04-07     1家机构买入，成功率42.56%  52.10  ...  7.752080e+07   2.625985  37.326871  2.663924e+09  有价格涨跌幅限制的 日收盘价格涨幅达到15%的前五只证券
822  688292  浩瀚深度  2023-04-07     2家机构买入，成功率42.51%  38.77  ...  2.725678e+08   7.600839  34.555959  1.400885e+09  有价格涨跌幅限制的 日收盘价格涨幅达到15%的前五只证券
823  688525  佰维存储  2023-04-07       买一主买，成功率45.68%  75.30  ...  1.224959e+09   7.171807  23.722308  2.619422e+09  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券
824  688525  佰维存储  2023-04-07       买一主买，成功率45.68%  75.30  ...  1.224959e+09   7.171807  23.722308  2.619422e+09     有价格涨跌幅限制 的日换手率达到30%的前五只证券

[825 rows x 16 columns]
```

- 沪深 A 股股票季度表现

```python
>>> import sharetop as sp
>>> sp.stock.get_all_company_quarterly_report() # 默认为最新季度，亦可指定季度
        股票代码  股票简称                 公告日期          营业收入    营业收入同比增长  营业收入季度环比  ...   净利润季度环比    每股收益      每股净资产  净资产收益率      销售毛利率  每股经营现金流量
0     689009  九号公司  2023-04-27 00:00:00  1.661971e+09  -13.318009  -33.3121  ...  -69.2641  0.2400   6.989759    0.35  28.217862 -0.027784
1     688777  中控技术  2023-04-27 00:00:00  1.445708e+09   47.297685  -39.6880  ...  -71.4405  0.1800  10.750850    1.74  33.329184 -1.447543
2     688619   罗普特  2023-04-27 00:00:00  2.426531e+07  122.454886  -62.9774  ...   89.4008 -0.0900   6.769040   -1.34  29.015660 -0.328464
3     688618  三旺通信  2023-04-27 00:00:00  7.170795e+07   31.499767  -38.2247  ...  -66.1811  0.2300  15.892091    1.45  58.706983 -0.094093
4     688616  西力科技  2023-04-27 00:00:00  5.352820e+07  -23.243255  -65.1878  ...  -85.2866  0.0200   5.085878    0.36  25.904601  0.188316
...      ...   ...                  ...           ...         ...       ...  ...       ...     ...        ...     ...        ...       ...
2486  002772  众兴菌业  2023-04-11 00:00:00  6.229097e+08   27.595337   18.5618  ...  395.5582  0.5042   8.573732    5.69  43.228766  0.642276
2487  688700  东威科技  2023-04-08 00:00:00  2.343187e+08   20.234687  -28.8650  ...  -24.9129  0.3400   6.715296    5.25  45.157212  0.183051
2488  600557  康缘药业  2023-04-08 00:00:00  1.352494e+09   25.390576   10.3734  ...   -7.6349  0.2500   8.374359    2.93  75.100289 -0.103785
2489  600313  农发种业  2023-04-08 00:00:00  1.216816e+09   25.531891  -15.8044  ...  -75.2715  0.0361   1.641364    2.23  10.883559  0.109289
2490  603102  百合股份  2023-04-07 00:00:00  2.319653e+08   58.729728   12.5487  ...   43.5618  0.7000  22.919256    3.10  39.261229  0.160328

[2491 rows x 14 columns]

```

- 股票历史单子流入数据(日级)

```python
>>> import sharetop as sp
>>> sp.stock.get_history_bill('300033')
     [11]:
    股票名称    股票代码          日期        主力净流入        小单净流入        中单净流入        大单净流入  ...  主力净流入占比  小单流入净占 比  中单流入净占比  大单流入净占比  超大单流入净占比     收盘价    涨跌幅
0    同花顺  300033  2022-11-25     882089.0     224019.0   -1106108.0   -5475560.0  ...     0.23     0.06    -0.29    -1.42      1.65   91.70  -0.17
1    同花顺  300033  2022-11-28  -26657991.0   -1271355.0   27929346.0    7247576.0  ...    -7.12    -0.34     7.46     1.94     -9.06   89.77  -2.10
2    同花顺  300033  2022-11-29  -28424729.0   -7268909.0   35693632.0   -5113388.0  ...    -3.41    -0.87     4.28    -0.61     -2.79   95.87   6.80
3    同花顺  300033  2022-11-30   79732027.0  -38462589.0  -41269424.0  -15238245.0  ...     8.88    -4.28    -4.59    -1.70     10.57   98.06   2.28
4    同花顺  300033  2022-12-01  -78911985.0    2884073.0   76027920.0  -66718656.0  ...    -6.96     0.25     6.71    -5.88     -1.08  103.92   5.98
..   ...     ...         ...          ...          ...          ...          ...  ...      ...      ...      ...      ...       ...     ...    ...
97   同花顺  300033  2023-04-20 -111105712.0  -53784144.0  164889856.0  -79994960.0  ...    -3.30    -1.60     4.90    -2.38     -0.93  210.00   6.25
98   同花顺  300033  2023-04-21 -221531232.0  130341040.0   91190176.0  -66933888.0  ...    -8.75     5.15     3.60    -2.64     -6.11  196.20  -6.57
99   同花顺  300033  2023-04-24 -340801376.0  353636016.0  -12834656.0 -180464832.0  ...   -10.56    10.96    -0.40    -5.59     -4.97  185.00  -5.71
100  同花顺  300033  2023-04-25   64723600.0   43360432.0 -108084016.0  -18683920.0  ...     2.03     1.36    -3.40    -0.59      2.62  195.01   5.41
101  同花顺  300033  2023-04-26 -284631712.0  127536400.0  157095328.0   78138048.0  ...    -8.47     3.80     4.68     2.33    -10.80  174.92 -10.30

[102 rows x 15 columns]
```

- 股票最新一个交易日单子流入数据(分钟级)

```python
>>> import sharetop as sp
>>> sp.stock.get_real_time_bill('300033')
      股票名称    股票代码                时间        主力净流入        小单净流入        中单净流入       大单净流入       超大单净流入
0    同花顺  300033  2023-04-26 09:31   -3217110.0     282877.0    2934232.0  -2000281.0   -1216829.0
1    同花顺  300033  2023-04-26 09:32   -2170472.0    1124259.0    1046212.0    155117.0   -2325589.0
2    同花顺  300033  2023-04-26 09:33   -9655528.0    6350780.0    3304748.0  -1823981.0   -7831547.0
3    同花顺  300033  2023-04-26 09:34  -16808716.0    9597965.0    7210752.0  -5368535.0  -11440181.0
4    同花顺  300033  2023-04-26 09:35  -20358486.0   12331063.0    8027424.0  -5877906.0  -14480580.0
..   ...     ...               ...          ...          ...          ...         ...          ...
235  同花顺  300033  2023-04-26 14:56 -282170831.0  124642581.0  157528257.0  77398429.0 -359569260.0
236  同花顺  300033  2023-04-26 14:57 -284631720.0  127536411.0  157095316.0  78138042.0 -362769762.0
237  同花顺  300033  2023-04-26 14:58 -284631720.0  127536411.0  157095316.0  78138042.0 -362769762.0
238  同花顺  300033  2023-04-26 14:59 -284631720.0  127536411.0  157095316.0  78138042.0 -362769762.0
239  同花顺  300033  2023-04-26 15:00 -284631720.0  127536411.0  157095316.0  78138042.0 -362769762.0

[240 rows x 8 columns]
```

### Fund

- 获取基金历史净值信息

```python
>>> import sharetop as sp
>>> sp.fund.get_fund_history('010434')
     日期    单位净值    累计净值   涨跌幅
0    2023-04-26  1.2760  1.2760 -1.15
1    2023-04-25  1.2909  1.2909  -1.5
2    2023-04-24  1.3105  1.3105  0.75
3    2023-04-21  1.3007  1.3007  0.26
4    2023-04-20  1.2973  1.2973  0.02
..          ...     ...     ...   ...
608  2020-10-28  0.9987  0.9987 -0.02
609  2020-10-27  0.9989  0.9989 -0.01
610  2020-10-26  0.9990  0.9990 -0.05
611  2020-10-23  0.9995  0.9995    --
612  2020-10-20  1.0000  1.0000    --

[613 rows x 4 columns]
```

- 获取基金公开持仓信息

```python
>>> import sharetop as sp
>>> # 获取最新公开的持仓数据
>>> sp.fund.get_invest_position('010434')
    基金代码    股票代码  股票简称  持仓占比  较上期变化        公开日期
0  010434  600329   达仁堂  9.52   0.90  2023-03-31
1  010434  600557  康缘药业  9.34  -0.54  2023-03-31
2  010434  600572   康恩贝  6.22  -0.42  2023-03-31
3  010434  300181  佐力药业  5.25  -1.10  2023-03-31
4  010434  600129  太极集团  5.19   0.39  2023-03-31
5  010434  603998  方盛制药  5.09   5.09  2023-03-31
6  010434  002603  以岭药业  5.04   5.04  2023-03-31
7  010434  600535   天士力  4.82   4.82  2023-03-31
8  010434  000989   九芝堂  4.53   4.53  2023-03-31
9  010434  300396  迪瑞医疗  4.42   4.42  2023-03-31
```

- 获取单只基金实时净值估算

```python
>>> import sharetop as sp
>>> sp.fund.get_fund_real_time_god('010434')
基金名称    基金代码    净值估算     涨跌值  估算涨幅              估值时间
0  红土创新医疗保健股票  010434  1.2959  0.0199  1.56  2023-04-27 10:12
```

- 获取单多支基金实时净值估算

```python
>>> import sharetop as sp
>>> sp.fund.get_fund_real_time_god(['010434', '004997'])
基金名称    基金代码    净值估算      涨跌值   估算涨幅              估值时间
0   广发高端制造股票A  004997  2.2639  -0.0126  -0.55  2023-04-27 10:31
1  红土创新医疗保健股票  010434  1.3059   0.0299   2.34  2023-04-27 10:31
```

### Bond

- 可转债整体行情

```python
>>> import sharetop as sp
>>> sp.bond.get_bond_realtime_quotes()
债券代码  债券名称    涨跌幅      最新价       最高       最低       今开  ...     昨日收盘         总市值        流通市值      行情ID 市场类型                 更新时间       最新交易日
0    127082  亚科转债   20.0    120.0    120.0  116.992    118.0  ...  100.000  1390800000  1390800000  0.127082   深A  2023-04-27 10:39:36  2023-04-27
1    113668  N鹿山转  16.51  116.511    118.0  115.485    116.9  ...  100.000           -   610517640  1.113668   沪A  2023-04-27 10:39:42  2023-04-27
2    128100  搜特转债   9.44    69.55   71.257    59.32   62.825  ...   63.550   555023119   555037029  0.128100   深A  2023-04-27 10:39:45  2023-04-27
3    123118  惠城转债   7.48  224.839  234.107    209.5    212.0  ...  209.200   444834968   445107023  0.123118   深A  2023-04-27 10:39:45  2023-04-27
4    123181  亚康转债   5.79  158.067   163.28    155.0    155.0  ...  149.420   412554870   412554870  0.123181   深A  2023-04-27 10:39:45  2023-04-27
..      ...   ...    ...      ...      ...      ...      ...  ...      ...         ...         ...       ...  ...                  ...         ...
501  123185  能辉转债  -2.84  117.753    121.5  116.965    119.9  ...  121.199   409670930   409670930  0.123185   深A  2023-04-27 10:39:45  2023-04-27
502  123116  万兴转债  -4.14   250.08    257.0  245.256    256.0  ...  260.888   511184277   511211785  0.123116   深A  2023-04-27 10:39:45  2023-04-27
503  123152  润禾转债  -4.83  130.057    134.9  129.111    134.7  ...  136.657   380107580   380107580  0.123152   深A  2023-04-27 10:39:45  2023-04-27
504  110058  永鼎转债  -7.04  155.155  164.999  154.181    162.0  ...  166.914           -   404116092  1.110058   沪A  2023-04-27 10:39:44  2023-04-27
505  123046  天铁转债 -16.72  389.318  481.525    387.0  471.441  ...  467.500   227693022   227693022  0.123046   深A  2023-04-27 10:39:45  2023-04-27

[506 rows x 20 columns]
```

- 全部可转债信息

```python
>>> import sharetop as sp
>>> sp.bond.get_bond_base_info_list()
      债券代码   债券名称    正股代码  正股名称  ...                 上市日期                 到期日期   期限(年)
               利率说明
0    118034   晶能转债  688223  晶科能源  ...                 None  2029-04-20 00:00:00       6  本次发行的可转债票面利率为第一年0.20%、第二年0.40%、第三年0.60%、第四年1.5...
1    123196  正元转02  300645  正元智慧  ...                 None  2029-04-18 00:00:00       6  第一年0.20%、第二年0.40%、第三年0.60%、第四年1.50%、第五年1.80%、第...
2    113670  金23转债  603180  金牌厨柜  ...                 None  2029-04-17 00:00:00       6  本次发行的可转债票面利率设定为:第一年0.30%、第二年0.50%、第三年1.00%、第四年...
3    123195  蓝晓转02  300487  蓝晓科技  ...                 None  2029-04-17 00:00:00       6   第一年0.4%,第二年0.6%,第三年1.1%,第四年1.8%,第五 年2.5%,第六年3.0%。
4    123194   百洋转债  301015  百洋医药  ...                 None  2029-04-14 00:00:00       6  第一年0.30%、第二年0.50%、第三年1.00%、第四年1.50%、第五年2.00%、第...
..      ...    ...     ...   ...  ...                  ...                  ...     ...                                                ...
815  110227   赤化转债  600227   圣济堂  ...  2007-10-23 00:00:00  2009-05-25 00:00:00  1.6192  票面利率和付息日期:本次发行的可转债票面利率第一年 为1.5%、第二年为1.8%、第三年为2....
816  126006  07深高债  600548   深高速  ...  2007-10-30 00:00:00  2013-10-09 00:00:00       6                                               None
817  110971   恒源转债  600971  恒源煤电  ...  2007-10-12 00:00:00  2009-12-21 00:00:00  2.2484  票面利率为:第一年年利率1.5%,第二年年利率1.8%,第三年年利率2.1%,第四年年利率2...
818  110567   山鹰转债  600567  山鹰国际  ...  2007-09-17 00:00:00  2010-02-01 00:00:00  2.4055  票面利率和付息日期:本次发行的可转债票面利率第一年为1.4%,第二年为1.7%,第三年为2....
819  110026   中海转债  600026  中远海能  ...  2007-07-12 00:00:00  2008-03-27 00:00:00   0.737  票面利率:第一年为1.84%,第二年为2.05%,第三年为2.26%,第四年为2.47%,第...

[820 rows x 12 columns]
```

- 指定可转债 K 线数据

```python
>>> import sharetop as sp
>>> # 可转债代码（以 东财转3 为例）
>>> bond_code = '123111'
>>> sp.stock.get_history_data(bond_code)
    债券名称    债券代码          日期       开盘       收盘       最高       最低      成交量           成交额    振幅    涨跌幅     涨跌额    换手率
0   东财转3  123111  2021-04-23  130.000  130.000  130.000  130.000  1836427  2.387355e+09  0.00  30.00  30.000  11.62
1   东财转3  123111  2021-04-26  130.353  130.010  133.880  125.110  8610944  1.126033e+10  6.75   0.01   0.010  54.50
2   东财转3  123111  2021-04-27  129.000  129.600  130.846  128.400  1820766  2.357472e+09  1.88  -0.32  -0.410  11.52
3   东财转3  123111  2021-04-28  129.100  130.770  131.663  128.903  1467727  1.921641e+09  2.13   0.90   1.170   9.29
4   东财转3  123111  2021-04-29  130.690  131.208  133.150  130.560  1156934  1.525974e+09  1.98   0.33   0.438   7.32
..   ...     ...         ...      ...      ...      ...      ...      ...           ...   ...    ...     ...    ...
72  东财转3  123111  2021-08-09  159.600  159.300  162.990  158.690   596124  9.585751e+08  2.69  -0.34  -0.550   3.77
73  东财转3  123111  2021-08-10  159.190  160.950  161.450  157.000   517237  8.234596e+08  2.79   1.04   1.650   3.27
74  东财转3  123111  2021-08-11  161.110  159.850  162.300  159.400   298906  4.800711e+08  1.80  -0.68  -1.100   1.89
75  东财转3  123111  2021-08-12  159.110  158.290  160.368  158.010   270641  4.298100e+08  1.48  -0.98  -1.560   1.71
76  东财转3  123111  2021-08-13  158.000  158.358  160.290  157.850   250059  3.975513e+08  1.54   0.04   0.068   1.58

[77 rows x 13 columns]
```

- 国债发行

```python
>>> import sharetop as sp
>>> start_date = '20230407' # 开始日期
>>> end_date = '20230425' # 结束日期
>>> sp.bond.bond_treasure_issue_cninfo(start_date, end_date)
    债券代码      债券简称  ...        公告日期                债券名称
0   019697    23国债04  ...  2023-04-26    2023年记账式附息(四期)国债
1   102232    国债2304  ...  2023-04-26    2023年记账式附息(四期)国债
2   230004  23附息国债04  ...  2023-04-26    2023年记账式附息(四期)国债
3   019703    23国债10  ...  2023-04-17    2023年记账式附息(十期)国债
4   102238    国债2310  ...  2023-04-17    2023年记账式附息(十期)国债
5   230010  23附息国债10  ...  2023-04-17    2023年记账式附息(十期)国债
6   020561    23贴债23  ...  2023-04-14  2023年记账式贴现(二十三期)国债
7   108561    贴债2323  ...  2023-04-14  2023年记账式贴现(二十三期)国债
8   239923  23贴现国债23  ...  2023-04-14  2023年记账式贴现(二十三期)国债
9   020562    23贴债24  ...  2023-04-20  2023年记账式贴现(二十四期)国债
10  108562    贴债2324  ...  2023-04-20  2023年记账式贴现(二十四期)国债
11  239924  23贴现国债24  ...  2023-04-20  2023年记账式贴现(二十四期)国债
12  019696    23国债03  ...  2023-04-24    2023年记账式附息(三期)国债
13  102231    国债2303  ...  2023-04-24    2023年记账式附息(三期)国债
14  230003  23附息国债03  ...  2023-04-24    2023年记账式附息(三期)国债
15  019699    23国债06  ...  2023-04-24    2023年记账式附息(六期)国债
16  102234    国债2306  ...  2023-04-24    2023年记账式附息(六期)国债
17  230006  23附息国债06  ...  2023-04-24    2023年记账式附息(六期)国债

[18 rows x 15 columns]

```


### Futures

- 获取交易所期货基本信息

```python
>>> import sharetop as sp
>>> sp.futures.get_futures_base_info()
       期货代码     期货名称        行情ID 市场类型
0    wr2310   线材2310  113.wr2310  上期所
1     SM307    锰硅307   115.SM307  郑商所
2    fb2307  纤维板2307  114.fb2307  大商所
3       SMM     锰硅主力     115.SMM  郑商所
4     SM306    锰硅306   115.SM306  郑商所
..      ...      ...         ...  ...
881  jm2310   焦煤2310  114.jm2310  大商所
882  jm2308   焦煤2308  114.jm2308  大商所
883  jm2307   焦煤2307  114.jm2307  大商所
884     jms    焦煤次主力     114.jms  大商所
885  jm2305   焦煤2305  114.jm2305  大商所

[886 rows x 4 columns]
```

- 获取期货历史行情

```python
>>> import sharetop as sp
>>> # 获取全部期货行情ID列表
>>> quote_ids = sp.futures.get_realtime_quotes()['行情ID']
>>> # 指定单个期货的行情ID(以上面获得到的行情ID列表为例)
>>> quote_id = quote_ids[0]
>>> # 查看第一个行情ID
>>> quote_ids[0]
'113.wr2310'
>>> # 获取第行情ID为第一个的期货日 K 线数据
>>> sp.futures.get_history_data(quote_id)
       期货名称    期货代码          日期    开盘    收盘    最高    最低  成交量     成交额    振幅   涨跌幅    涨跌额  换手率
0  线材2310  wr2310  2022-11-14  4065  4350  4350  4065    4  168300  0.00  0.00    0.0  0.0
1  线材2310  wr2310  2022-11-28  4401  4151  4401  4151    2   85520  5.94 -1.33  -56.0  0.0
2  线材2310  wr2310  2023-04-07  4582  4582  4582  4582    5  229100  0.00  7.16  306.0  0.0
3  线材2310  wr2310  2023-04-13  4582  4582  4582  4582    1   45820  0.00  0.00    0.0  0.0
4  线材2310  wr2310  2023-04-24  4445  4260  4445  4260    2   87050  4.04 -7.03 -322.0  0.0
5  线材2310  wr2310  2023-04-25  4468  4390  4468  4213   10  434890  5.86  0.87   38.0  0.0
6  线材2310  wr2310  2023-04-26  4253  4253  4253  4253    1   42530  0.00 -2.18  -95.0  0.0
7  线材2310  wr2310  2023-04-27  4587  4587  4587  4587    1   45870  0.00  7.85  334.0  0.0

>>> # 指定多个期货的 行情ID
>>> quote_ids = ['115.ZCM','115.ZC109']
>>> futures_df = sp.futures.get_history_data(quote_ids)
>>> type(futures_df)
<class 'dict'>
>>> futures_df['115.ZCM']
       期货名称 期货代码          日期     开盘     收盘     最高     最低    成交量           成交额    振幅   涨跌幅   涨跌额  换手率
0     动力煤主力  ZCM  2015-05-18  440.0  437.6  440.2  437.6     64  2.806300e+06  0.00  0.00   0.0  0.0
1     动力煤主力  ZCM  2015-05-19  436.0  437.0  437.6  436.0      6  2.621000e+05  0.36 -0.32  -1.4  0.0
2     动力煤主力  ZCM  2015-05-20  436.8  435.8  437.0  434.8      8  3.487500e+05  0.50 -0.23  -1.0  0.0
3     动力煤主力  ZCM  2015-05-21  438.0  443.2  446.8  437.8     37  1.631850e+06  2.06  1.65   7.2  0.0
4     动力煤主力  ZCM  2015-05-22  439.2  441.4  443.8  439.2     34  1.502500e+06  1.04  0.09   0.4  0.0
...     ...  ...         ...    ...    ...    ...    ...    ...           ...   ...   ...   ...  ...
1524  动力煤主力  ZCM  2021-08-17  755.0  770.8  776.0  750.6  82373  6.288355e+09  3.25 -1.26  -9.8  0.0
1525  动力煤主力  ZCM  2021-08-18  770.8  776.8  785.8  766.0  77392  6.016454e+09  2.59  1.76  13.4  0.0
1526  动力煤主力  ZCM  2021-08-19  776.8  777.6  798.0  764.6  97229  7.597474e+09  4.30  0.03   0.2  0.0
1527  动力煤主力  ZCM  2021-08-20  778.0  793.0  795.0  775.2  70549  5.553617e+09  2.53  1.48  11.6  0.0
1528  动力煤主力  ZCM  2021-08-23  796.8  836.6  843.8  796.8  82954  6.850341e+09  5.97  6.28  49.4  0.0

[1529 rows x 13 columns]
```


## Contact

[![Github](https://img.shields.io/badge/Github-blue?style=social&logo=github)](https://github.com/nrliangxy)
[![Email](https://img.shields.io/badge/Email-blue)](mailto:nrliangxy@foxmail.com)
