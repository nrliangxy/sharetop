import pandas as pd
from .config import country_base_url, country_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj
from ..common.explain_change import exchange_explain


@to_numeric
def get_country_list(token: str, limit: int = 100, is_explain: bool = False) -> pd.DataFrame:
    """
    国家基本信息列表
    :param token:
    :param limit:
    :return:
    """
    headers = {"token": token}
    base_url_list.append(country_base_url)
    data = {"limit": limit}
    r = requests_obj.get("".join(base_url_list), data=data, headers=headers)
    if isinstance(r, dict):
        return r
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, country_field_dict)
    return exchange_explain(df, is_explain)
