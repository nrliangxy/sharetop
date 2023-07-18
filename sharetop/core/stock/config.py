import inspect
from pathlib import Path

HERE = Path(__file__).parent

# 股票基本信息表头
EASTMONEY_STOCK_BASE_INFO_FIELDS = {
    'f57': '股票代码',
    'f58': '股票名称',
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

EASTMONEY_STOCK_DAILY_BILL_BOARD_FIELDS = {
    'SECURITY_CODE': '股票代码',
    'SECURITY_NAME_ABBR': '股票名称',
    'TRADE_DATE': '上榜日期',
    'EXPLAIN': '解读',
    'CLOSE_PRICE': '收盘价',
    'CHANGE_RATE': '涨跌幅',
    'TURNOVERRATE': '换手率',
    'BILLBOARD_NET_AMT': '龙虎榜净买额',
    'BILLBOARD_BUY_AMT': '龙虎榜买入额',
    'BILLBOARD_SELL_AMT': '龙虎榜卖出额',
    'BILLBOARD_DEAL_AMT': '龙虎榜成交额',
    'ACCUM_AMOUNT': '市场总成交额',
    'DEAL_NET_RATIO': '净买额占总成交比',
    'DEAL_AMOUNT_RATIO': '成交额占总成交比',
    'FREE_MARKET_CAP': '流通市值',
    'EXPLANATION': '上榜原因',
}


class Explain:
    get_stock_all_report_dates_fields = {
        "报告日期": "report_date",
        "季报名称": "quarterly_report_title"
    }

    get_stock_market_real_time_data_fields = {
        "股票代码": "stock_code",
        "股票名称": "stock_name",
        "涨跌幅": "percentage_change",
        "最新价": "last_price",
        "最高": "high_price",
        "最低": "low_price",
        "今开": "open_price",
        "涨跌额": "price_change",
        "换手率": "turnover_rate",
        "量比": "volume_ratio",
        "动态市盈率": "price_to_earnings_ratio",
        "成交量": "trading_volume",
        "成交额": "trading_volume",
        "昨日收盘": "previous_close",
        "总市值": "market_cap",
        "流通市值": "free_float_market_cap",
        "行情ID": "item_id",
        "市场类型": "market_type",
        "更新时间": "update_time",
        "最新交易日": "latest_trading_day"
    }

    get_stock_all_company_quarterly_report_fields = {
        "股票代码": "stock_code",
        "股票简称": "short_name",
        "公告日期": "public_date",
        "营业收入": "operating_revenue",
        "营业收入同比增长": "yoy_growth_operating_revenue",
        "营业收入季度环比": "qoq_growth_operating_revenue",
        "净利润": "net_profit",
        "净利润同比增长": "yoy_growth_net_profit",
        "净利润季度环比": "qoq_growth_net_profit",
        "每股收益": "earnings_per_share",
        "每股净资产": "navps",
        "净资产收益率": "roe",
        "销售毛利率": "gross_profit_margin",
        "每股经营现金流量": "eps_operating_cash_flow"
    }


def exchange_explain(df, is_explain):
    frame = inspect.currentframe().f_back
    func_name_fields = frame.f_code.co_name
    exchange_fields = getattr(Explain, f"{func_name_fields}_fields")
    if not is_explain:
        df.rename(columns=exchange_fields, inplace=True)
    return df
