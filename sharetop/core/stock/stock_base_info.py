import pandas as pd
from typing import Dict, List, Union
from ..common.common_base import CommonFunc
from ..common.explain_change import exchange_explain
from ..utils import validate_request

common_func_obj = CommonFunc()


def get_stock_base_info(stock_codes: Union[str, List[str]], is_explain: bool = False
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    获取股票的基本信息
    :param is_explain:
    :param stock_codes: 一个或者多个股票代码
    :return: 股票的基本信息
    """
    base_func_name = get_stock_base_info.__name__
    return exchange_explain(common_func_obj.get_common_func(stock_codes, base_func_name), is_explain)
