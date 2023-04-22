import requests
import threading
import pandas as pd
import uuid
from typing import List, Union
from ...crawl.settings import fund_valuation_url_list

data_source = []


def get_fund_price(fund_code: str):
    global data_source
    str_uuid = str(uuid.uuid4()).upper()
    params = {"code": fund_code, "deviceid": str_uuid}
    FUND_ESTIMATION_BASE_URL = "".join(fund_valuation_url_list)
    fund_base_url = FUND_ESTIMATION_BASE_URL.format(**params)
    r = requests.get(fund_base_url)
    data = r.json()
    expansion = data.get("Expansion")
    short_name = expansion.get("SHORTNAME")
    gz = expansion.get("GZ")   # 估值价格
    diff_value = expansion.get("GZZF")  # 涨跌值
    gz_time = expansion.get("GZTIME") # 估值时间
    fund_range = expansion.get("GSZZL")  # 估值涨跌幅
    data_source.append((short_name, fund_code, gz, diff_value, fund_range, gz_time))


def get_fund_real_time_god(fund_codes: Union[str, List[str]], **kwargs) -> pd.DataFrame:
    fund_list = [fund_codes] if isinstance(fund_codes, str) else fund_codes
    threads = []
    for item in fund_list:
        threads.append(threading.Thread(target=get_fund_price, args=(item, )))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    columns = ["基金名称", "基金代码", "净值估算", "涨跌值", "估算涨幅", "估值时间"]
    df = pd.DataFrame(data_source, columns=columns)
    return df
