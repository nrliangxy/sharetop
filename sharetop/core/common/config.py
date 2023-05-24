from pathlib import Path
from typing import Dict

import pandas as pd

HERE = Path(__file__).parent


class MagicConfig:
    EXTRA_FIELDS = 'extra_fields'
    QUOTE_ID_MODE = 'quote_id_mode'
    RETURN_DF = 'return_df'


EASTMONEY_BASE_INFO_FIELDS = {
    'f57': '代码',
    'f58': '名称',
    'f162': '市盈率(动)',
    'f167': '市净率',
    'f127': '所处行业',
    'f116': '总市值',
    'f117': '流通市值',
    'f198': '板块编号',
    'f173': 'ROE',
    'f187': '净利率',
    'f105': '净利润',
    'f186': '毛利率',
}


# 行情ID搜索缓存
BASE_INFO_CACHE: Dict[str, pd.Series] = dict()

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
    "f58": "股票名称",
    "f57": "股票代码",
    "f43": "最新价",
    "f44": "最高价",
    "f45": "最低价",
    "f46": "开盘价",
    "f47": "成交量(手)",
    "f48": "成交额(元)",
    "f49": "外盘(手)",
    "f60": "昨收",
    "f71": "均价",
    "f84": "总股本",
    "f85": "流通股本",
    "f92": "每股净资产",
    "f108": "每股收益",
    "f116": "总市值",
    "f117": "流通市值",
    "f161": "内盘(手)",
    "f164": "市盈率(TTM)",
    "f167": "市净率",
    "f169": "涨跌值",
    "f170": "涨跌幅(%)",
    "f171": "振幅(%)"
}

# 股票、债券榜单表头
EASTMONEY_QUOTE_FIELDS = {
    'f12': '代码',
    'f14': '名称',
    'f3': '涨跌幅',
    'f2': '最新价',
    'f15': '最高',
    'f16': '最低',
    'f17': '今开',
    'f4': '涨跌额',
    'f8': '换手率',
    'f10': '量比',
    'f9': '动态市盈率',
    'f5': '成交量',
    'f6': '成交额',
    'f18': '昨日收盘',
    'f20': '总市值',
    'f21': '流通市值',
    'f13': '市场编号',
    'f124': '更新时间戳',
    'f297': '最新交易日',
}

# 各个市场编号
MARKET_NUMBER_DICT = {
    '0': '深A',
    '1': '沪A',
    '105': '美股',
    '106': '美股',
    '107': '美股',
    '116': '港股',
    '128': '港股',
    '113': '上期所',
    '114': '大商所',
    '115': '郑商所',
    '8': '中金所',
    '142': '上海能源期货交易所',
    '155': '英股',
    '90': '板块',
    '225': '广期所',
}

FS_DICT = {
    # 可转债
    'bond': 'b:MK0354',
    '可转债': 'b:MK0354',
    'stock': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
    # 沪深A股
    # 'stock': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23',
    '沪深A股': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23',
    '沪深京A股': 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048',
    '北证A股': 'm:0 t:81 s:2048',
    '北A': 'm:0 t:81 s:2048',
    # 期货
    'futures': 'm:113,m:114,m:115,m:8,m:142,m:225',
    '期货': 'm:113,m:114,m:115,m:8,m:142,m:225',
    '上证A股': 'm:1 t:2,m:1 t:23',
    '沪A': 'm:1 t:2,m:1 t:23',
    '深证A股': 'm:0 t:6,m:0 t:80',
    '深A': 'm:0 t:6,m:0 t:80',
    # 沪深新股
    '新股': 'm:0 f:8,m:1 f:8',
    '创业板': 'm:0 t:80',
    '科创板': 'm:1 t:23',
    '沪股通': 'b:BK0707',
    '深股通': 'b:BK0804',
    '风险警示板': 'm:0 f:4,m:1 f:4',
    '两网及退市': 'm:0 s:3',
    # 板块
    '地域板块': 'm:90 t:1 f:!50',
    '行业板块': 'm:90 t:2 f:!50',
    '概念板块': 'm:90 t:3 f:!50',
    # 指数
    '上证系列指数': 'm:1 s:2',
    '深证系列指数': 'm:0 t:5',
    '沪深系列指数': 'm:1 s:2,m:0 t:5',
    # ETF 基金
    'ETF': 'b:MK0021,b:MK0022,b:MK0023,b:MK0024',
    # LOF 基金
    'LOF': 'b:MK0404,b:MK0405,b:MK0406,b:MK0407',
    '美股': 'm:105,m:106,m:107',
    '港股': 'm:128 t:3,m:128 t:4,m:128 t:1,m:128 t:2',
    '英股': 'm:155 t:1,m:155 t:2,m:155 t:3,m:156 t:1,m:156 t:2,m:156 t:5,m:156 t:6,m:156 t:7,m:156 t:8',
    '中概股': 'b:MK0201',
    '中国概念股': 'b:MK0201',
}

QUARTERLY_DICT = {
    "SECURITY_CODE": "股票代码",
    "SECURITY_NAME_ABBR": "股票名称",
    "TRADE_MARKET": "板块",
    "SECURITY_TYPE": "股票类型",
    "UPDATE_DATE": "最新公告日期",
    "REPORTDATE": "报告期",
    "BASIC_EPS": "每股收益(元)",
    "DEDUCT_BASIC_EPS": "每股收益(扣除)(元)",
    "TOTAL_OPERATE_INCOME": "营业总收入(元)",
    "PARENT_NETPROFIT": "净利润(元)",
    "WEIGHTAVG_ROE": "净资产收益率(%)",
    "YSTZ": "营业总收入同比增长(%)",
    "SJLTZ": "净利润同比增长(%)",
    "BPS": "每股净资产(元)",
    "MGJYXJJE": "每股经营现金流量(元)",
    "XSMLL": "销售毛利率(%)",
    "YSHZ": "营业总收入季度环比增长(%)",
    "SJLHZ": "净利润季度环比增长",
    "ASSIGNDSCRPT": "利润分配",
    "ZXGXL": "股息率(%)",
    "NOTICE_DATE": "首次公告日期",
    "DATATYPE": "年报类型"
}

# 股票、债券历史大单数据表头
EASTMONEY_HISTORY_BILL_FIELDS = {
    'f51': '日期',
    'f52': '主力净流入',
    'f53': '小单净流入',
    'f54': '中单净流入',
    'f55': '大单净流入',
    'f56': '超大单净流入',
    'f57': '主力净流入占比',
    'f58': '小单流入净占比',
    'f59': '中单流入净占比',
    'f60': '大单流入净占比',
    'f61': '超大单流入净占比',
    'f62': '收盘价',
    'f63': '涨跌幅',
}

today = {
    "fid": "f62",
    "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
    "fields_map": {"f3": "今日涨跌幅", "f14": "行业", "f62": "今日主力净流入额", "f184": "今日主力流入净占比", "f66": "今日超大单净流入额",
                   "f69": "今日超大单流入净占比", "f72": "今日大单净流入额", "f75": "今日大单流入净占比", "f78": "今日中单净流入额",
                   "f81": "今日中单流入净占比", "f84": "今日小单净流入额", "f87": "今日小单流入净占比", "f204": "股票名称", "f205": "股票代码"}
}

five_day = {
    "fid": "f164",
    "fields": "f14,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258",
    "fields_map": {"f109": "5日涨跌幅", "f14": "行业", "f164": "5日主力净流入额", "f165": "5日主力流入净占比",
                   "f166": "5日超大单净流入额", "f167": "5日超大单流入净占比", "f168": "5日大单净流入额",
                   "f169": "5日大单净流入净占比", "f170": "5日中单净流入额", "f171": "5日中单流入净占比", "f172": "5日小单净流入额",
                   "f173": "5日小单净流入净占比", "f257": "股票名称", "f258": "股票代码"}
}

ten_day = {
    "fid": "f174",
    "fields": "f12,f14,f2,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261,f124,f1,f13"
}


sector_dict = {
    '1': today,
    '5': five_day,
    '10': ten_day
}


industry = {
    "fs": "m:90+t:2"
}

concept = {
    "fs": "m:90+t:3"
}

area = {
    "fs": "m:90+t:1"
}

sector_dict2 = {
    "industry": industry,
    "concept": concept,
    "area": area
}
