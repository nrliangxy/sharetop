import copy
import pandas as pd
from .config import pig_fcr_url, pig_fcr_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain


@to_numeric
def get_pig_data_common(token: str, pig_url: str, field_dict: dict, start_date: str, end_date: str, limit: int) -> pd.DataFrame:
    """
    :param token:
    :param field_dict:
    :param pig_url:
    :param start_date:
    :param end_date: 字段对应关系
    :param limit:
    :return:
    """
    headers = {"token": token}
    copy_base_url_list = copy.deepcopy(base_url_list)
    copy_base_url_list.append(pig_url)
    data = {}
    if start_date:
        data["start_date"] = start_date
    if end_date:
        data['end_date'] = end_date
    if limit:
        data['limit'] = limit
    r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_pig_fcr(token: str, start_date: str = None, end_date: str = None, limit: int = None, is_explain: bool = False) -> pd.DataFrame:
    """
    获取猪周期的历史猪肉价格和猪粮比
    :param token:
    :param end_date:
    :param start_date:
    :param limit:
    :return:
    """
    return exchange_explain(get_pig_data_common(token, pig_fcr_url, pig_fcr_field_dict, start_date, end_date,  limit), is_explain)
