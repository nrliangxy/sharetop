import pandas as pd
import copy
from .config import oil_reserves_url, oil_reserves_field_dict, oil_products_field_dict, oil_products_url, \
    oil_consumption_url, oil_consumption_field_dict, oil_refinerythroughput_field_dict, oil_refinerythroughput_url, \
    oil_refinerycapacity_url, oil_refinerycapacity_field_dict, oil_crudeoilpricehistory_field_dict, \
    oil_crudeoilpricehistory_url
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain


@to_numeric
def get_oil_data_common(token: str, oil_url: str, field_dict: dict, data_type: str = None,
                        limit: int = None) -> pd.DataFrame:
    """
    :param token:
    :param field_dict: 字段对应关系
    :param oil_url:  具体是石油数据url
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    copy_base_url_list = copy.deepcopy(base_url_list)
    copy_base_url_list.append(oil_url)
    data = {}
    headers = {"token": token}
    if data_type:
        data["data_type"] = data_type
    if limit:
        data['limit'] = limit
    r = requests_obj.get("".join(copy_base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, field_dict)
    return df


def get_oil_reserves(token: str, data_type: str = '1', limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取机构的石油储量
    :param token:
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_reserves_url, oil_reserves_field_dict, data_type, limit), is_explain)


def get_oil_products(token: str, data_type: str = '1', limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取机构的石油产量
    :param token:
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_products_url, oil_products_field_dict, data_type, limit), is_explain)


def get_oil_consumption(token: str, data_type: str = '1', limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取机构的消费量
    :param token:
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_consumption_url, oil_consumption_field_dict, data_type, limit), is_explain)


def get_oil_refinerythroughput(token: str, data_type: str = '1', limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取石油的加工量
    :param token:
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_refinerythroughput_url, oil_refinerythroughput_field_dict, data_type, limit), is_explain)


def get_oil_refinerycapacity(token: str, data_type: str = '1', limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取石油的产能
    :param token:
    :param data_type: 1为国家数据 2为机构数据 4为大洲数据
    :param limit:
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_refinerycapacity_url, oil_refinerycapacity_field_dict, data_type, limit), is_explain)


def get_oil_crudeoilpricehistory(token: str, limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    获取石油的历史价格
    :param token:
    :param limit: 数据限制
    :return:
    """
    return exchange_explain(get_oil_data_common(token, oil_crudeoilpricehistory_url, oil_crudeoilpricehistory_field_dict, limit=limit), is_explain)
