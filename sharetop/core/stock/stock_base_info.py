import pandas as pd
from typing import Dict, List, Union
from ..common.common_base import CommonFunc

common_func_obj = CommonFunc()


def get_stock_base_info(stock_codes: Union[str, List[str]],
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    base_func_name = get_stock_base_info.__name__
    return common_func_obj.get_common_func(stock_codes, base_func_name)