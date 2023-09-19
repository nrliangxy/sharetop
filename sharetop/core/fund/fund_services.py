from .fund_list import get_fund_codes
from .get_fund_rank import get_fund_exchange_rank


class FundServices:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def fund_to_zq(self, **kwargs):
        is_explain = kwargs.get("is_explain", False)
        params = {'is_explain': is_explain, "ft": "zq", "token": self.token}
        return get_fund_codes(**params)

    def fund_to_etf(self, **kwargs):
        is_explain = kwargs.get("is_explain", False)
        params = {'is_explain': is_explain, "token": self.token}
        fund_name_field = "基金简称" if is_explain else "fund_name"
        df = get_fund_exchange_rank(**params)
        new_df = df[df[fund_name_field].str.contains('国债', case=False)]
        return new_df
