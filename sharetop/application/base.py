import pandas as pd
import math
from typing import List
from jsonpath import jsonpath
from datetime import datetime
from ..core.common.config import MARKET_NUMBER_DICT


class BaseApplication:
    def __init__(self, json_data, *args, **kwargs):
        self.json_data = json_data

    def parse_json(self, json_par):
        json_r: List[str] = jsonpath(self.json_data, json_par)
        return json_r

    def deal_k_data(self, columns, quote_id, json_par='$..klines[:]'):
        k_lines = self.parse_json(json_par)
        if not k_lines:
            columns.insert(0, '代码')
            columns.insert(0, '名称')
            return pd.DataFrame(columns=columns)
        rows = [kline.split(',') for kline in k_lines]
        name = self.json_data['data']['name']
        code = quote_id.split('.')[-1]
        df = pd.DataFrame(rows, columns=columns)
        df.insert(0, '代码', code)
        df.insert(0, '名称', name)
        return df

    def deal_fields(self, data, fields_list):
        f59 = data['f59']
        for _ in fields_list:
            item = data[_] / math.pow(10, f59)
            data[_] = item
        return data

    def deal_price_fields(self, data, fields_list):
        f152 = data['f152']
        for _ in fields_list:
            item = data[_] / math.pow(10, f152)
            data[_] = item
        return data

    def deal_real_time_data(self, columns, fields_k_v):
        data = self.json_data['data']
        if not data:
            columns.insert(0, '代码')
            columns.insert(0, '名称')
            return pd.DataFrame(columns=columns)
        deal_real_time_price = ["f170"]
        deal_fields_list = ["f43", "f169", "f44", "f45", "f46", "f60", "f71", "f164", "f167", "f171"]
        data = self.deal_fields(data, deal_fields_list)
        data = self.deal_price_fields(data, deal_real_time_price)
        r = {v: data.get(k) for k, v in fields_k_v.items()}
        return pd.DataFrame([r])

    def deal_market_realtime(self, columns):
        df = pd.DataFrame(self.json_data['data']['diff'])
        df = df.rename(columns=columns)
        df: pd.DataFrame = df[columns.values()]
        # df['行情ID'] = df['市场编号'].astype(str) + '.' + df['代码'].astype(str)
        df['市场类型'] = df['市场编号'].astype(str).apply(lambda x: MARKET_NUMBER_DICT.get(x))
        df['更新时间'] = df['更新时间戳'].apply(lambda x: str(datetime.fromtimestamp(x)))
        df['最新交易日'] = pd.to_datetime(df['最新交易日'], format='%Y%m%d').astype(str)
        tmp = df['最新交易日']
        del df['最新交易日']
        df['最新交易日'] = tmp
        del df['更新时间戳']
        return df

    def deal_quarterly_report(self, columns):
        df = pd.DataFrame(self.json_data['result']['data'])
        df = df.drop(['TRADE_MARKET_CODE', 'SECURITY_TYPE_CODE', 'PAYYEAR', 'PUBLISHNAME', 'ORG_CODE', 'TRADE_MARKET_ZJG',
                 'ISNEW', 'DATAYEAR', 'DATEMMDD', 'EITIME', 'SECUCODE', 'QDATE'], axis=1)
        df = df.rename(columns=columns)
        return df

    def deal_bill(self, columns, quote_id, json_par='$..klines[:]'):
        klines: List[str] = self.parse_json(json_par)
        if not klines:
            columns.insert(0, '代码')
            columns.insert(0, '名称')
            return pd.DataFrame(columns=columns)
        rows = [kline.split(',') for kline in klines]
        name = jsonpath(self.json_data, '$..name')[0]
        code = quote_id.split('.')[-1]
        df = pd.DataFrame(rows, columns=columns)
        df.insert(0, '代码', code)
        df.insert(0, '名称', name)
        return df

    def deal_fund_list(self):
        def fund_data(item):
            r1_list = item.split(",")
            code = r1_list[0]
            name = r1_list[1]
            base_yield = r1_list[3]
            funded_time = r1_list[12]
            now_time = r1_list[9]
            unit_value = r1_list[10]
            accumulate_value = r1_list[11]
            value_list = [code, name, base_yield, funded_time, now_time, unit_value, accumulate_value]
            key_list = ["基金代码", "基金名称", "自成立以来收益(%)", "成立时间", "净值时间", "单位净值", "累计净值"]
            return dict(zip(key_list, value_list))
        return pd.DataFrame(list(map(fund_data, self.json_data)))
