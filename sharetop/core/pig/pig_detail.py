import pandas as pd
from .config import pig_fcr_url, pig_fcr_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj


@to_numeric
def get_pig_data_common(pig_url: str, field_dict: dict, start_date: str, end_date: str, limit: int) -> pd.DataFrame:
    """
    :param field_dict:
    :param pig_url:
    :param start_date:
    :param end_date: 字段对应关系
    :param limit:
    :return:
    """
    base_url_list.append(pig_url)
    data = {}
    if start_date:
        data["start_date"] = start_date
    if end_date:
        data['end_date'] = end_date
    if limit:
        data['limit'] = limit
    r = requests_obj.get("".join(base_url_list), data=data)
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_fcr(start_date: str = None, end_date: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param end_date:
    :param start_date:
    :param limit:
    :return:
    """
    return get_pig_data_common(pig_fcr_url, pig_fcr_field_dict, start_date, end_date,  limit)
