import pandas as pd
from .config import country_base_url
from ...crawl.settings import *
from ..utils import get_quote_id, to_numeric, requests_obj


def get_country_base_info(limit: int = None) -> pd.DataFrame:
    base_url_list.append(country_base_url)
    data = {"limit": limit}
    r = requests_obj.get("".join(base_url_list), data=data)
    data_json = r.json()
    
    return r.text
