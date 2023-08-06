import requests
import datetime
import re
import pandas as pd
from ..utils import requests_obj, parse_obj, validate_request, to_numeric
from .config import fund_money_cloumns
from ..common.explain_change import exchange_explain


def fund_export_df(text_data):
    json_data = parse_obj.parse_fund_json(text_data)
    temp_df = pd.DataFrame(json_data)
    temp_df = temp_df.iloc[:, 0].str.split(",", expand=True)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    return temp_df


@to_numeric
@validate_request
def get_fund_open_rank(token: str, symbol: str = "全部", is_explain: bool = False) -> pd.DataFrame:
    """
    东方财富网-数据中心-开放基金排行
    https://fund.eastmoney.com/data/fundranking.html
    :param token:
    :param is_explain:
    :param symbol: choice of {"全部", "股票型", "混合型", "债券型", "指数型", "QDII", "LOF", "FOF"}
    :type symbol: str
    :return: 开放基金排行
    :rtype: pandas.DataFrame
    """
    current_date = datetime.datetime.now().date().isoformat()
    last_date = str(int(current_date[:4]) - 1) + current_date[4:]
    url = "http://fund.eastmoney.com/data/rankhandler.aspx"
    type_map = {
        "全部": ["all", "zzf"],
        "股票型": ["gp", "6yzf"],
        "混合型": ["hh", "6yzf"],
        "债券型": ["zq", "6yzf"],
        "指数型": ["zs", "6yzf"],
        "QDII": ["qdii", "6yzf"],
        "LOF": ["lof", "6yzf"],
        "FOF": ["fof", "6yzf"],
    }
    params = {
        "op": "ph",
        "dt": "kf",
        "ft": type_map[symbol][0],
        "rs": "",
        "gs": "0",
        "sc": type_map[symbol][1],
        "st": "desc",
        "sd": last_date,
        "ed": current_date,
        "qdii": "",
        "tabSubtype": ",,,,,",
        "pi": "1",
        "pn": "20000",
        "dx": "1",
        "v": "0.1591891419018292",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    r = requests_obj.get(url, params, headers=headers)
    text_data = r.text
    temp_df = fund_export_df(text_data)
    temp_df.columns = [
        "序号",
        "基金代码",
        "基金简称",
        "_",
        "日期",
        "单位净值",
        "累计净值",
        "日增长率",
        "近1周",
        "近1月",
        "近3月",
        "近6月",
        "近1年",
        "近2年",
        "近3年",
        "今年来",
        "成立来",
        "_",
        "_",
        "自定义",
        "_",
        "手续费",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "日期",
            "单位净值",
            "累计净值",
            "日增长率",
            "近1周",
            "近1月",
            "近3月",
            "近6月",
            "近1年",
            "近2年",
            "近3年",
            "今年来",
            "成立来",
            "手续费",
        ]
    ]
    return exchange_explain(temp_df, is_explain)


@to_numeric
@validate_request
def get_fund_exchange_rank(token: str, is_explain: bool = False) -> pd.DataFrame:
    """
    东方财富网-数据中心-场内交易基金排行
    https://fund.eastmoney.com/data/fbsfundranking.html
    :return: 场内交易基金数据
    :rtype: pandas.DataFrame
    """
    url = "http://fund.eastmoney.com/data/rankhandler.aspx"
    params = {
        "op": "ph",
        "dt": "fb",
        "ft": "ct",
        "rs": "",
        "gs": "0",
        "sc": "1nzf",
        "st": "desc",
        "pi": "1",
        "pn": "10000",
        "v": "0.1591891419018292",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    r = requests_obj.get(url, params, headers=headers)
    text_data = r.text
    temp_df = fund_export_df(text_data)
    temp_df.columns = [
        "序号",
        "基金代码",
        "基金简称",
        "_",
        "日期",
        "单位净值",
        "累计净值",
        "近1周",
        "近1月",
        "近3月",
        "近6月",
        "近1年",
        "近2年",
        "近3年",
        "今年来",
        "成立来",
        "成立日期",
        "_",
        "_",
        "_",
        "_",
        "_",
        "类型",
        "_",
    ]
    temp_df = temp_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "类型",
            "日期",
            "单位净值",
            "累计净值",
            "近1周",
            "近1月",
            "近3月",
            "近6月",
            "近1年",
            "近2年",
            "近3年",
            "今年来",
            "成立来",
            "成立日期",
        ]
    ]
    # temp_df['日期'] = pd.to_datetime(temp_df['日期']).dt.date
    # temp_df['成立日期'] = pd.to_datetime(temp_df['成立日期']).dt.date
    # temp_df['单位净值'] = pd.to_numeric(temp_df['单位净值'], errors="coerce")
    # temp_df['累计净值'] = pd.to_numeric(temp_df['累计净值'], errors="coerce")
    # temp_df['近1周'] = pd.to_numeric(temp_df['近1周'], errors="coerce")
    # temp_df['近1月'] = pd.to_numeric(temp_df['近1月'], errors="coerce")
    # temp_df['近3月'] = pd.to_numeric(temp_df['近3月'], errors="coerce")
    # temp_df['近6月'] = pd.to_numeric(temp_df['近6月'], errors="coerce")
    # temp_df['近1年'] = pd.to_numeric(temp_df['近1年'], errors="coerce")
    # temp_df['近2年'] = pd.to_numeric(temp_df['近2年'], errors="coerce")
    # temp_df['近3年'] = pd.to_numeric(temp_df['近3年'], errors="coerce")
    # temp_df['今年来'] = pd.to_numeric(temp_df['今年来'], errors="coerce")
    # temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    return exchange_explain(temp_df, is_explain)


@to_numeric
@validate_request
def get_fund_money_rank(token: str, is_explain: bool = False) -> pd.DataFrame:
    """
    东方财富网-数据中心-货币型基金排行
    https://fund.eastmoney.com/data/hbxfundranking.html
    :return: 货币型基金排行
    :rtype: pandas.DataFrame
    """
    url = "http://api.fund.eastmoney.com/FundRank/GetHbRankList"
    params = {
        "intCompany": "0",
        "MinsgType": "",
        "IsSale": "1",
        "strSortCol": "SYL_1N",
        "orderType": "desc",
        "pageIndex": "1",
        "pageSize": "10000",
        "_": "1603867224251",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    r = requests_obj.get(url, params, headers=headers)
    json_data = r.json()
    temp_data_json = []
    for _ in json_data["Data"]:
        temp_dict = {}
        for k, v in _.items():
            if k in fund_money_cloumns:
                temp_dict[k] = v
        temp_data_json.append(temp_dict)
    temp_df = pd.DataFrame(temp_data_json)
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    temp_df.rename(columns=fund_money_cloumns, inplace=True)
    # temp_df['日期'] = pd.to_datetime(temp_df['日期']).dt.date
    # temp_df['万份收益'] = pd.to_numeric(temp_df['万份收益'], errors="coerce")
    # temp_df['年化收益率7日'] = pd.to_numeric(temp_df['年化收益率7日'], errors="coerce")
    # temp_df['年化收益率14日'] = pd.to_numeric(temp_df['年化收益率14日'], errors="coerce")
    # temp_df['年化收益率28日'] = pd.to_numeric(temp_df['年化收益率28日'], errors="coerce")
    # temp_df['近1月'] = pd.to_numeric(temp_df['近1月'], errors="coerce")
    # temp_df['近3月'] = pd.to_numeric(temp_df['近3月'], errors="coerce")
    # temp_df['近6月'] = pd.to_numeric(temp_df['近6月'], errors="coerce")
    # temp_df['近1年'] = pd.to_numeric(temp_df['近1年'], errors="coerce")
    # temp_df['近2年'] = pd.to_numeric(temp_df['近2年'], errors="coerce")
    # temp_df['近3年'] = pd.to_numeric(temp_df['近3年'], errors="coerce")
    # temp_df['近5年'] = pd.to_numeric(temp_df['近5年'], errors="coerce")
    # temp_df['今年来'] = pd.to_numeric(temp_df['今年来'], errors="coerce")
    # temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    return exchange_explain(temp_df, is_explain)


@to_numeric
@validate_request
def get_fund_hk_rank(token: str, is_explain: bool = False) -> pd.DataFrame:
    """
    东方财富网-数据中心-香港基金排行
    https://overseas.1234567.com.cn/FundList
    :return: 香港基金排行
    :rtype: pandas.DataFrame
    """
    format_date = datetime.datetime.now().date().isoformat()
    url = "https://overseas.1234567.com.cn/overseasapi/OpenApiHander.ashx"
    params = {
        'api': 'HKFDApi',
        'm': 'MethodFundList',
        'action': '1',
        'pageindex': '0',
        'pagesize': '5000',
        'dy': '1',
        'date1': format_date,
        'date2': format_date,
        'sortfield': 'Y',
        'sorttype': '-1',
        'isbuy': '0',
        '_': '1610790553848',
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "http://fund.eastmoney.com/fundguzhi.html",
    }
    r = requests_obj.get(url, params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["Data"])
    temp_df.reset_index(inplace=True)
    temp_df["index"] = list(range(1, len(temp_df) + 1))
    temp_df.columns = [
        "序号",
        "_",
        "香港基金代码",
        "基金代码",
        "_",
        "基金简称",
        "可购买",
        "日期",
        "单位净值",
        "日增长率",
        "_",
        "近1周",
        "近1月",
        "近3月",
        "近6月",
        "近1年",
        "近2年",
        "近3年",
        "今年来",
        "成立来",
        "币种",
    ]
    temp_df = temp_df[
        [
            "序号",
            "基金代码",
            "基金简称",
            "币种",
            "日期",
            "单位净值",
            "日增长率",
            "近1周",
            "近1月",
            "近3月",
            "近6月",
            "近1年",
            "近2年",
            "近3年",
            "今年来",
            "成立来",
            "可购买",
            "香港基金代码",
        ]
    ]
    # temp_df['日期'] = pd.to_datetime(temp_df['日期']).dt.date
    temp_df['单位净值'] = pd.to_numeric(temp_df['单位净值'], errors="coerce")
    temp_df['日增长率'] = pd.to_numeric(temp_df['日增长率'], errors="coerce")
    # temp_df['近1周'] = pd.to_numeric(temp_df['近1周'], errors="coerce")
    # temp_df['近1月'] = pd.to_numeric(temp_df['近1月'], errors="coerce")
    # temp_df['近3月'] = pd.to_numeric(temp_df['近3月'], errors="coerce")
    # temp_df['近6月'] = pd.to_numeric(temp_df['近6月'], errors="coerce")
    # temp_df['近1年'] = pd.to_numeric(temp_df['近1年'], errors="coerce")
    # temp_df['近2年'] = pd.to_numeric(temp_df['近2年'], errors="coerce")
    # temp_df['近3年'] = pd.to_numeric(temp_df['近3年'], errors="coerce")
    # temp_df['今年来'] = pd.to_numeric(temp_df['今年来'], errors="coerce")
    # temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    # temp_df['成立来'] = pd.to_numeric(temp_df['成立来'], errors="coerce")
    temp_df['可购买'] = temp_df['可购买'].map(lambda x: "可购买" if x == "1" else "不可购买")
    return exchange_explain(temp_df, is_explain)
