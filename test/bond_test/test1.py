from sharetop.core.bond import get_bond_base_info, get_bond_realtime_quotes, get_bond_base_info_list,\
    get_bond_public, bond_treasure_issue_cninfo, bond_local_government_issue_cninfo, bond_corporate_issue_cninfo, \
    bond_cov_issue_cninfo, bond_cov_stock_issue_cninfo
from sharetop.core.stock import get_real_time_data, get_real_time_bill, get_history_bill

# d = get_bond_base_info("123077")

# d = get_bond_realtime_quotes()

# d = get_real_time_data("123077")

# d = get_real_time_bill("123077")

# d = get_history_bill("123077")

# d = get_bond_public()

d = bond_cov_issue_cninfo()

print(d)