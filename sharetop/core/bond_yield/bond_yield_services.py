import requests
import datetime
import pandas as pd
from sharetop.core.utils import to_numeric, requests_obj, parse_obj


class BondYieldServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.url = "https://hq.sinajs.cn/?rn=1694440934177&list=globalbd_{bond_name}"
        self.headers = {
            "Referer": "https://stock.finance.sina.com.cn/forex/globalbd/gcny10.html"
        }

    def real_time(self, **kwargs):
        bond_name = kwargs.get("bond_name")
        bond_url = self.url.format(bond_name=bond_name)
        r = requests_obj.get(bond_url, data={}, headers=self.headers)
        data = r.text
        data = data.replace(f'var hq_str_globalbd_{bond_name}="', "").replace('";', "")
        data_list = data.split(",")
        bond_name = data_list[0]
        open_price = data_list[1]
        previous_close = data_list[2]
        now_price = data_list[3]
        high_price = data_list[4]
        low_price = data_list[5]
        percentage_change = float(data_list[7]) * 100
        price_change = data_list[8]
        update_time = datetime.datetime.fromtimestamp(int(data_list[11]))
        item = {"bond_name": bond_name, "open_price": open_price, "previous_close": previous_close,
                "now_price": now_price,
                "high_price": high_price, "low_price": low_price,
                "percentage_change": percentage_change, "price_change": price_change, "update_time": update_time}
        df = pd.DataFrame([item])
        return df


