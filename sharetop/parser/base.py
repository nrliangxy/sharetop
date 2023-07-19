import pandas as pd
from lxml import etree
import re
from jsonpath import jsonpath
from typing import Any, Callable, Dict, List, TypeVar, Union
from .config import STOCK_BASE_INFO_DICT, CAPITAL_FLOW_DICT


class BaseParse:
    def __int__(self, *args, **kwargs):
        self.stock_base_info_dict = STOCK_BASE_INFO_DICT

    def parse_html(self, html):
        return etree.HTML(html)

    def parse_json(self, json_response, json_par='$..klines[:]'):
        json_r: List[str] = jsonpath(json_response, json_par)
        return json_r

    def parse_fund_json(self, text_response):
        results = re.findall('\[.*\]', text_response)
        json_data = eval(results[0])
        return json_data

    def parse_god_cup_json(self, data_json, country_field_dict):
        data = data_json['data']
        df = pd.DataFrame(data)
        df.rename(columns=country_field_dict, inplace=True)
        return df

    def parse_capital_flow_json(self, data_json, field_map=None):
        data = data_json['data']['diff']
        df = pd.DataFrame(data)
        if field_map:
            use_map = field_map
        else:
            use_map = CAPITAL_FLOW_DICT
        df.rename(columns=use_map, inplace=True)
        return df

    def parse_stock_base_info(self, base_data):
        status = base_data.get("status")
        if status and status == -1:
            return pd.DataFrame([base_data])
        jbzl = base_data['jbzl'][0]
        fxxg = base_data['fxxg'][0]
        fxxg = {k.lower(): v for k, v in fxxg.items()}
        jbzl = {k.lower(): v for k, v in jbzl.items()}
        secucode = jbzl['secucode']
        code, mk_code = secucode.split(".")
        name = jbzl['security_name_abbr']
        org_name = jbzl['org_name']
        org_name_en = jbzl['org_name_en']
        uscc = jbzl['reg_num']
        security_type = jbzl['security_type']
        trade_market = jbzl['trade_market']
        em_industry = jbzl['em2016']
        industrycsrc1 = jbzl['industrycsrc1']
        chairman = jbzl['chairman']
        legal_person = jbzl['legal_person']
        president = jbzl['president']
        secretary = jbzl['secretary']
        secpresent = jbzl['secpresent']
        reg_capital = jbzl['reg_capital']
        found_date = fxxg['found_date']
        listing_date = fxxg['listing_date']
        province = jbzl['province']
        city = ""
        introduction = jbzl['org_profile']
        business_scope = jbzl['business_scope']
        website = jbzl['org_web']
        org_tel = jbzl['org_tel']
        org_fax = jbzl['org_fax']
        email = jbzl['org_email']
        reg_address = jbzl['reg_address']
        office_address = jbzl['address']
        emp_num = jbzl['emp_num']
        manager_num = jbzl['tatolnumber']
        law_office = jbzl['law_firm']
        accounting_firm = jbzl['accountfirm_name']
        if "深交" in security_type:
            exchange_code = "SZSE"
        elif "上交" in security_type:
            exchange_code = "SSE"
        elif "北京证券" in security_type:
            exchange_code = "BSE"
        else:
            exchange_code = ""
        last_result = {
            "secucode": secucode, "code": code, "mk_code": mk_code, "name": name, "org_name": org_name,
            "org_name_en": org_name_en,
            "uscc": uscc, "security_type": security_type, "trade_market": trade_market, "em_industry": em_industry,
            "industrycsrc1": industrycsrc1,
            "chairman": chairman, "legal_person": legal_person, "president": president, "secretary": secretary,
            "secpresent": secpresent, "reg_capital": reg_capital,
            "found_date": found_date, "listing_date": listing_date, "province": province, "city": city,
            "introduction": introduction, "business_scope": business_scope,
            "website": website, "org_tel": org_tel, "org_fax": org_fax, "email": email, "reg_address": reg_address,
            "office_address": office_address, "emp_num": emp_num,
            "manager_num": manager_num, "law_office": law_office, "accounting_firm": accounting_firm,
            "exchange_code": exchange_code
        }
        last_result = {STOCK_BASE_INFO_DICT.get(k, ""): v for k, v in last_result.items()}
        return pd.DataFrame([last_result])
