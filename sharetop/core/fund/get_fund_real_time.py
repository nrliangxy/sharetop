import time
import requests
import datetime
import threading
import uuid
from typing import Any, Callable, Dict, List, TypeVar, Union
from ...crawl.settings import fund_valuation_url_list

data_source = []


def get_fund_price(fund_code):
    global data_source
    str_uuid = str(uuid.uuid4()).upper()
    # if not check_time():
    #     return
    print('正在获取[' + str(fund_code) + ']的价格...')
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


def check_time():
    china_time = time.localtime(time.mktime(datetime.datetime.now().timetuple()))
    c_current_hour = int(time.strftime('%H', china_time))
    c_current_minute = int(time.strftime('%M', china_time))
    c_current_time = c_current_hour + c_current_minute / 100
    c_current_week = int(time.strftime('%w', china_time))

    if c_current_week != 6 and c_current_week != 0:  # 非周六周日
        if 9.25 < c_current_time < 11.35 or 12.55 < c_current_time < 15.20:  # 囊括国内开盘时间
            return True
    return False


def get_fund_real_time_god(fund_codes: Union[str, List[str]], **kwargs):
    today = datetime.datetime.now().date()
    # is_workday_r = is_workday(today)
    # if not is_workday_r:
    #     return
    # valid_fund_list = get_fund()
    fund_list = [fund_codes] if isinstance(fund_codes, str) else fund_codes
    threads = []
    for item in fund_list:
        threads.append(threading.Thread(target=get_fund_price, args=(item, )))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(data_source)


# if __name__ == '__main__':
#     get_fund_real_time_god("004997")