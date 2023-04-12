from pathlib import Path

HERE = Path(__file__).parent


class MagicConfig:
    EXTRA_FIELDS = 'extra_fields'
    QUOTE_ID_MODE = 'quote_id_mode'
    RETURN_DF = 'return_df'


# 请求头
EASTMONEY_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
}

# 股票、ETF、债券 K 线表头
EM_KLINE_FIELDS = {
    'f51': '日期',
    'f52': '开盘',
    'f53': '收盘',
    'f54': '最高',
    'f55': '最低',
    'f56': '成交量',
    'f57': '成交额',
    'f58': '振幅',
    'f59': '涨跌幅',
    'f60': '涨跌额',
    'f61': '换手率',
    'f62': '盘后量',
    'f63': '盘后额',
}

# 获取实时股票数据 请求参数
EM_REAL_TIME_FIELDS_PARAMS = "f58,f107,f57,f43,f59,f169,f170,f152,f46,f60,f44,f45,f47,f48,f19,f532,f39,f161,f49,f171," \
                      "f50,f86,f600,f601,f154,f84,f85,f168,f108,f116,f167,f164,f92,f71,f117"

EM_REAL_TIME_FIELDS = {
    "f43": "最新价",
    "f44": "最高价",
    "f45": "最低价",
    "f46": "开盘价",
    "f47": "成交量(手)",
    "f48": "成交额(元)",
    "f49": "外盘",
    "f57": "股票代码",
    "f58": "股票名称",
    "f60": "昨收",
    "f71": "均价",
    "f84": "总股本",
    "f85": "流通股本",
    "f92": "每股净资产",
    "f108": "每股收益",
    "f116": "总市值",
    "f117": "流通市值",
    "f161": "内盘",
    "f164": "市盈率(TTM)",
    "f167": "市净率",
    "f169": "涨跌值",
    "f170": "涨跌幅",
    "f171": "振幅"
}
