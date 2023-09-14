import requests
import threading
import copy
import pandas as pd
import json
from typing import List, Union
from ...crawl.settings import fund_valuation_url_list
from ..common.explain_change import exchange_explain

data_source = []


def get_fund_price(fund_code: str):
    global data_source
    params = {"code": fund_code}
    FUND_ESTIMATION_BASE_URL = "".join(fund_valuation_url_list)
    fund_base_url = FUND_ESTIMATION_BASE_URL.format(**params)
    r = requests.get(fund_base_url)
    data = r.text
    deal_data = data.replace("jsonpgz(", "").replace(");", "")
    expansion = json.loads(deal_data)
    short_name = expansion.get("name")
    gz = float(expansion.get("gsz"))  # 估值价格
    fund_range = float(expansion.get("gszzl"))  # 估值涨跌幅
    diff_value = round(gz * (float(fund_range) / 100), 3)  # 涨跌值
    gz_time = expansion.get("gztime")  # 估值时间
    data_source.append((short_name, fund_code, gz, diff_value, fund_range, gz_time))


def get_fund_real_time_god(fund_codes: Union[str, List[str]], is_explain: bool = False, **kwargs) -> pd.DataFrame:
    global data_source
    fund_list = [fund_codes] if isinstance(fund_codes, str) else fund_codes
    threads = []
    for item in fund_list:
        threads.append(threading.Thread(target=get_fund_price, args=(item,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    export_data_source = copy.deepcopy(data_source)
    columns = ["基金名称", "基金代码", "净值估算", "涨跌值", "估算涨跌幅", "更新时间"]
    df = pd.DataFrame(export_data_source, columns=columns)
    data_source = []
    return exchange_explain(df, is_explain)
