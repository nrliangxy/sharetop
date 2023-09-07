import pandas as pd
import copy
from .config import logistics_index_url, logistics_index_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain

index_type_list = {
    "1": "电商物流指数"
}


@to_numeric
def get_logistics_data_common(token: str, index_url: str, field_dict: dict, index_type: str = None,
                              start_date: str = None,
                              end_date: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param token:
    :param field_dict: 字段对应关系
    :param car_url:  具体是石油数据url
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    copy_base_url_list = copy.deepcopy(base_url_list)
    copy_base_url_list.append(index_url)
    data = {"index_type": index_type, "start_date": start_date, "end_date": end_date, "limit": limit}
    headers = {"token": token}
    r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    for item in data_json.get('data', []):
        item['index_type'] = index_type_list.get(item['index_type'], item['index_type'])
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_logistics_index(token: str, index_type: str = None, start_date: str = None, end_date: str = None,
                        limit: int = 100,
                        is_explain: bool = False) -> pd.DataFrame:
    """
    获取猪周期的历史猪肉价格和猪粮比
    :param is_explain:
    :param index_type:
    :param start_date:
    :param end_date:
    :param token:
    :param limit:
    :return:
    """
    return exchange_explain(
        get_logistics_data_common(token, logistics_index_url, logistics_index_field_dict, index_type,
                                  start_date, end_date, limit), is_explain)
