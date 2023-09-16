import pandas as pd
import copy
from .config import car_sales_url, car_sales_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain

car_type_list = {
    "1": "轿车",
    "2": "suv",
    "3": "mpv"
}

source_list = {
    "1": "太平洋汽车",
    "2": "懂车帝"
}


@to_numeric
def get_car_data_common(token: str, car_url: str, field_dict: dict, car_type: str = None, pub_date: str = None,
                        source: str = None,
                        limit: int = None) -> pd.DataFrame:
    """
    :param token:
    :param field_dict: 字段对应关系
    :param car_url:  具体是石油数据url
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    copy_base_url_list = copy.deepcopy(base_url_list)
    copy_base_url_list.append(car_url)
    data = {"car_type": car_type, "pub_date": pub_date, "source": source, "limit": limit}
    headers = {"token": token}
    r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    for item in data_json.get('data', []):
        item['car_type'] = car_type_list.get(item['car_type'], item['car_type'])
        item['source'] = source_list.get(item['source'], item['source'])
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_car_sales(token: str, car_type: str = None, pub_date: str = None, source: str = None, limit: int = 100,
                  is_explain: bool = False) -> pd.DataFrame:
    """
    :param is_explain:
    :param car_type:
    :param pub_date:
    :param source:
    :param token:
    :param limit:
    :return:
    """
    return exchange_explain(get_car_data_common(token, car_sales_url, car_sales_field_dict, car_type, pub_date,
                                                source, limit),
                            is_explain)
