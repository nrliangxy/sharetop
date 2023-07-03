import pandas as pd
from .config import country_base_url, country_field_dict
from ...crawl.settings import *
from ..utils import to_numeric, requests_obj, parse_obj


@to_numeric
def get_country_base_info(token: str, limit: int = None) -> pd.DataFrame:
    base_url_list.append(country_base_url)
    data = {"limit": limit}
    r = requests_obj.get("".join(base_url_list), data=data)
    data_json = r.json()
    df = parse_obj.parse_god_cup_json(data_json, country_field_dict)
    return df
