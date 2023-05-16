import pandas as pd
from .config import oil_reserves_url, oil_reserves_field_dict, oil_products_field_dict, oil_products_url, \
    oil_consumption_url, oil_consumption_field_dict, oil_refinerythroughput_field_dict, oil_refinerythroughput_url, \
    oil_refinerycapacity_url, oil_refinerycapacity_field_dict, oil_crudeoilpricehistory_field_dict, \
    oil_crudeoilpricehistory_url
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj


@to_numeric
def get_oil_data_common(oil_url: str, field_dict: dict, data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param field_dict: 字段对应关系
    :param oil_url:  具体是石油数据url
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    base_url_list.append(oil_url)
    data = {}
    if data_type:
        data["data_type"] = data_type
    if limit:
        data['limit'] = limit
    r = requests_obj.get("".join(base_url_list), data=data)
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_oil_reserves(data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return get_oil_data_common(oil_reserves_url, oil_reserves_field_dict, data_type, limit)


def get_oil_products(data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return get_oil_data_common(oil_products_url, oil_products_field_dict, data_type, limit)


def get_oil_consumption(data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return get_oil_data_common(oil_consumption_url, oil_consumption_field_dict, data_type, limit)


def get_oil_refinerythroughput(data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return get_oil_data_common(oil_refinerythroughput_url, oil_refinerythroughput_field_dict, data_type, limit)


def get_oil_refinerycapacity(data_type: str = None, limit: int = None) -> pd.DataFrame:
    """
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return get_oil_data_common(oil_refinerycapacity_url, oil_refinerycapacity_field_dict, data_type, limit)


def get_oil_crudeoilpricehistory(limit: int = None) -> pd.DataFrame:
    """
    :param limit: 数据限制
    :return:
    """
    return get_oil_data_common(oil_crudeoilpricehistory_url, oil_crudeoilpricehistory_field_dict, limit=limit)
