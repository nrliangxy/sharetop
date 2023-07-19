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
        "股票简称": "stock_name",
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
