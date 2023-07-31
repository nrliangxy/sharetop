import inspect

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
        "成交额": "volume",
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
        "股票简称": "stock_name",
        "公告日期": "public_date",
        "营业收入": "operating_revenue",
        "营业收入同比增长": "yoy_growth_operating_revenue",
        "营业收入季度环比": "qoq_growth_operating_revenue",
        "净利润": "net_profit",
        "净利润同比增长": "yoy_growth_net_profit",
        "净利润季度环比": "qoq_growth_net_profit",
        "每股收益": "eps",
        "每股净资产": "navps",
        "净资产收益率": "roe",
        "销售毛利率": "gross_profit_margin",
        "每股经营现金流量": "eps_operating_cash_flow"
    }

    get_stock_company_report_data_fields = {
        "股票代码": "stock_code",
        "股票名称": "stock_name",
        "板块": "sector",
        "股票类型": "stock_type",
        "最新公告日期": "latest_announcement_date",
        "报告期": "reporting_period",
        "每股收益(元)": "eps",
        "每股收益(扣除)(元)": "eps_diluted",
        "营业总收入(元)": "total_operating_revenue",
        "净利润(元)": "net_profit",
        "净资产收益率(%)": "roe",
        "营业总收入同比增长(%)": "yoy_growth_operating_revenue",
        "净利润同比增长(%)": "yoy_growth_net_profit",
        "每股净资产(元)": "navps",
        "每股经营现金流量(元)": "eps_operating_cash_flow",
        "销售毛利率(%)": "gross_profit_margin",
        "营业总收入季度环比增长(%)": "qoq_growth_operating_revenue",
        "净利润季度环比增长": "qoq_growth_net_profit",
        "利润分配": "profit_distribution",
        "股息率(%)": "dividend_yield",
        "首次公告日期": "initial_announcement_date",
        "年报类型": "annual_report_type"
    }

    get_stock_base_info_fields = {
        "唯一代码": "unique_id",
        "股票代码": "stock_code",
        "市场代码": "market_code",
        "股票名称": "stock_name",
        "公司名称": "org_name",
        "公司英文名称": "org_name_en",
        "统一社会信用代码": "uscc",
        "证券类别": "security_type",
        "上市交易所": "stock_exchange",
        "东财行业": "east_money_industry",
        "证监会行业": "csrc_industry",
        "董事长": "chairman",
        "法人代表": "legal_representative",
        "总经理": "manager",
        "董秘": "board_secretary",
        "证券事务代表": "securities_representative",
        "注册资本(万)": "reg_capital",
        "公司成立日期": "found_date",
        "公司上市日期": "ipo_date",
        "所在省份": "province",
        "所在城市": "city",
        "公司简介": "introduction",
        "经营范围": "business_scope",
        "公司主页": "website",
        "联系电话": "org_tel",
        "联系传真": "org_fax",
        "电子邮件": "email",
        "注册地址": "reg_address",
        "办公地址": "office_address",
        "员工人数": "emp_num",
        "管理人员人数": "manager_num",
        "律师事务所": "law_office",
        "会计师事务所": "accounting_firm",
        "交易所代码": "exchange_code"
    }

    get_stock_real_time_data_fields = {
        "股票名称": "stock_name",
        "股票代码": "stock_code",
        "最新价": "latest_price",
        "最高价": "highest_price",
        "最低价": "lowest_price",
        "开盘价": "open_price",
        "成交量(手)": "trading_volume",
        "成交额(元)": "volume",
        "外盘(手)": "foreign_volume(lots)",
        "昨收": "previous_close",
        "均价": "average_price",
        "总股本": "total_share_capital",
        "流通股本": "floating_shares",
        "每股净资产": "navps",
        "每股收益": "eps",
        "总市值": "market_cap",
        "流通市值": "free_float_market_cap",
        "内盘(手)": "domestic_volume(lots)",
        "市盈率(TTM)": "ttm",
        "市净率": "pb_ratio",
        "涨跌值": "price_change",
        "涨跌幅(%)": "percentage_change",
        "振幅(%)": "amplitude"
    }

    get_stock_kline_data_fields = {
        "股票名称": "stock_name",
        "股票代码": "stock_code",
        "日期": "date",
        "开盘": "opening_price",
        "收盘": "closing_price",
        "最高": "highest_price",
        "最低": "lowest_price",
        "成交量": "trading_volume",
        "成交额": "volume",
        "振幅": "amplitude",
        "涨跌幅": "percentage_change",
        "涨跌额": "price_change",
        "换手率": "turnover_rate",
        "盘后量": "after_hours_volume",
        "盘后额": "after_hours_value"
    }

    get_stock_history_capital_fields = {
        "股票名称": "stock_name",
        "股票代码": "stock_code",
        "日期": "date",
        "主力净流入": "net_main_inflow",
        "小单净流入": "small_order_net_inflow",
        "中单净流入": "medium_order_net_inflow",
        "大单净流入": "large_order_net_inflow",
        "超大单净流入": "super_large_order_net_inflow",
        "主力净流入占比": "main_net_inflow_ratio",
        "小单流入净占比": "smail_order_net_inflow_ratio",
        "中单流入净占比": "medium_order_net_inflow_ratio",
        "大单流入净占比": "large_order_net_inflow_ratio",
        "超大单流入净占比": "super_large_order_net_inflow_ratio",
        "收盘价": "closing_price",
        "涨跌幅": "percentage_change"
    }

    get_stock_real_time_daily_capital_fields = {
        "股票名称": "stock_name",
        "股票代码": "stock_code",
        "时间": "time",
        "主力净流入": "net_main_inflow",
        "小单净流入": "small_order_net_inflow",
        "中单净流入": "medium_order_net_inflow",
        "大单净流入": "large_order_net_inflow",
        "超大单净流入": "super_large_order_net_inflow"
    }

    get_stock_real_time_sum_capital_fields = {
        "今日主力净流入": "net_main_inflow_today",
        "超大单流入": "super_large_inflow",
        "超大单流出": "super_large_outflow",
        "今日超大单净流入": "net_super_large_inflow_today",
        "超大单净比": "net_super_large_ratio",
        "大单流入": "large_inflow",
        "大单流出": "large_outflow",
        "今日大单净流入": "net_large_inflow_today",
        "大单净比": "net_large_ratio",
        "中单流入": "medium_inflow",
        "中单流出": "medium_outflow",
        "今日中单净流入": "net_medium_inflow_today",
        "中单净比": "net_medium_ratio",
        "小单流入": "small_inflow",
        "小单流出": "small_outflow",
        "今日小单净流入": "net_small_inflow_today",
        "小单净比": "net_small_ratio",
        "主力净比": "net_main_ratio",
        "20日主力净流入": "net_main_inflow_20_days",
        "20日超大单净流入": "net_super_large_inflow_20_days",
        "20日大单净流入": "net_large_inflow_20_days",
        "20日中单净流入": "net_medium_inflow_20_days",
        "20日小单净流入": "net_small_inflow_20_days",
        "5日主力净流入": "net_main_inflow_5_days",
        "5日超大单净流入": "net_super_large_inflow_5_days",
        "5日大单净流入": "net_large_inflow_5_days",
        "5日中单净流入": "net_medium_inflow_5_days",
        "5日小单净流入": "net_small_inflow_5_days"
    }

    get_stock_real_time_sector_capital_fields = {
        "今日涨跌幅(%)": "percentage_change_today",
        "行业": "industry",
        "今日主力净流入额": "net_main_inflow_amount_today",
        "今日超大单净流入额": "net_super_large_inflow_amount_today",
        "今日超大单流入净占比(%)": "net_super_large_inflow_ratio_today",
        "今日大单净流入额": "net_large_inflow_amount_today",
        "今日大单流入净占比(%)": "net_large_inflow_ratio_today",
        "今日中单净流入额": "net_medium_inflow_amount_today",
        "今日中单流入净占比(%)": "net_medium_inflow_ratio_today",
        "今日小单净流入额": "net_small_inflow_ratio_today",
        "今日小单流入净占比(%)": "net_small_inflow_ratio_today",
        "今日主力流入净占比(%)": "net_main_inflow_ratio_today",
        "股票名称": "stock_name",
        "股票代码": "stock_code"
    }

    get_stock_dragon_tiger_list_fields = {
        "股票名称": "stock_name",
        "股票代码": "stock_code",
        "上榜日期": "listing_date",
        "解读": "interpretation",
        "收盘价": "closing_price",
        "涨跌幅": "percentage_change",
        "换手率": "turnover_rate",
        "龙虎榜净买额": "net_buying_amount_on_dtl",
        "龙虎榜买入额": "buying_amount_on_dtl",
        "龙虎榜卖出额": "selling_amount_on_dtl",
        "龙虎榜成交额": "transaction_amount_on_dtl",
        "市场总成交额": "total_market_turnover",
        "净买额占总成交比": "net_buy_ratio",
        "成交额占总成交比": "turnover_ratio",
        "流通市值": "free_float_market_cap",
        "上榜原因": "reason_listing"
    }

    get_fund_codes_fields = {
        "基金代码": "fund_code",
        "基金名称": "fund_name",
        "自成立以来收益(%)": "cumulative_return_since_inception",
        "成立时间": "inception_date",
        "净值时间": "nav_date",
        "单位净值": "nav_per_unit",
        "累计净值": "cumulative_net_asset_value"
    }

    get_fund_open_rank_fields = {
        "序号": "number",
        "基金代码": "fund_code",
        "基金简称": "fund_name",
        "日期": "date",
        "单位净值": "nav_per_unit",
        "累计净值": "cumulative_net_asset_value",
        "日增长率": "daily_growth_rate",
        "近1周": "last_one_week",
        "近1月": "last_one_month",
        "近3月": "last_three_month",
        "近6月": "last_six_month",
        "近1年": "last_one_year",
        "近2年": "last_two_year",
        "近3年": "last_three_year",
        "今年来": "year_to_day",
        "成立来": "since_inception",
        "手续费": "handling_fee"
    }

    get_fund_exchange_rank_fields = {
        '序号': 'number',
        "基金代码": "fund_code",
        "基金简称": "fund_name",
        "类型": "fund_type",
        "日期": "date",
        "单位净值": "nav_per_unit",
        "累计净值": "cumulative_net_asset_value",
        "近1周": "last_one_week",
        "近1月": "last_one_month",
        "近3月": "last_three_month",
        "近6月": "last_six_month",
        "近1年": "last_one_year",
        "近2年": "last_two_year",
        "近3年": "last_three_year",
        "今年来": "year_to_day",
        "成立来": "since_inception",
        "成立日期": "inception_date"
    }

    get_fund_money_rank_fields = {
        "序号": "number",
        "近1月": "last_one_month",
        "近3月": "last_three_month",
        "近6月": "last_six_month",
        "近1年": "last_one_year",
        "近2年": "last_two_year",
        "近3年": "last_three_year",
        "近5年": "last_five_year",
        "基金代码": "fund_code",
        "基金简称": "fund_name",
        "日期": "date",
        "万份收益": "income_yield",
        "年化收益率7日": "7_day_annualized_yield",
        "年化收益率14日": "14_day_annualized_yield",
        "年化收益率28日": "28_day_annualized_yield",
        "今年来": "year_to_day",
        "成立来": "since_inception"
    }

    get_fund_hk_rank_fields = {
        "序号": "number",
        "基金代码": "fund_code",
        "基金简称": "fund_name",
        "币种": "currency",
        "日期": "date",
        "单位净值": "nav_per_unit",
        "日增长率": "daily_growth_rate",
        "近1周": "last_one_week",
        "近1月": "last_one_month",
        "近3月": "last_three_month",
        "近6月": "last_six_month",
        "近1年": "last_one_year",
        "近2年": "last_two_year",
        "近3年": "last_three_year",
        "今年来": "year_to_day",
        "成立来": "since_inception",
        "可购买": "available_purchase",
        "香港基金代码": "hong_kong_fund_code"
    }

    get_fund_base_info_fields = {
        "基金代码": "fund_code",
        "基金简称": "fund_name",
        "涨跌幅": "percentage_change",
        "最新净值": "latest_nav",
        "成立日期": "inception_date",
        "最新评级": "latest_rating",
        "基金公司": "fund_company",
        "净值更新日期": "nav_update_date",
        "基金规模": "fund_size",
        "基金规模更新时间": "fund_size_update_date",
        "简介": "introduction"
    }

    get_fund_history_price_fields = {
        "日期": "date",
        "单位净值": "nav_per_unit",
        "累计净值": "cumulative_net_asset_value",
        "涨跌幅": "percentage_change"
    }


def exchange_explain_one(df, exchange_fields, is_explain):
    if not is_explain:
        df.rename(columns=exchange_fields, inplace=True)
    return df


def exchange_explain(df, is_explain):
    frame = inspect.currentframe().f_back
    func_name_fields = frame.f_code.co_name
    exchange_fields = getattr(Explain, f"{func_name_fields}_fields")
    if not is_explain:
        if isinstance(df, dict):
            return {k: exchange_explain_one(v, exchange_fields, is_explain) for k, v in df.items()}
        df.rename(columns=exchange_fields, inplace=True)
    return df
