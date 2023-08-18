import copy
import pandas as pd
from .config import ship_indicators_url, ship_indicators_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain


@to_numeric
def get_ship_data_common(token: str, ship_url: str, field_dict: dict, org_name: str, year: str, ship_indicators: str,
                         limit: int) -> pd.DataFrame:
    """
    :param ship_indicators:
    :param token:
    :param field_dict:
    :param ship_url:
    :param org_name:
    :param year: 字段对应关系
    :param limit:
    :return:
    """
    headers = {"token": token}
    copy_base_url_list = copy.deepcopy(base_url_list)
    copy_base_url_list.append(ship_url)
    data = {}
    if limit:
        data['limit'] = limit
    if org_name:
        data['org_name'] = org_name
    if year:
        data['year'] = year
    if ship_indicators:
        data['ship_indicators'] = ship_indicators
    r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_ship_indicators(token: str, org_name: str = None, year: str = None, ship_indicators: str = None, limit: int = 100,
                is_explain: bool = False) -> pd.DataFrame:
    """
    获取猪周期的历史猪肉价格和猪粮比
    :param is_explain:
    :param ship_indicators:
    :param year:
    :param org_name:
    :param token:
    :param limit:
    :return:
    """
    return exchange_explain(get_ship_data_common(token, ship_indicators_url, ship_indicators_field_dict, org_name, year,
                                                 ship_indicators, limit),
                            is_explain)
