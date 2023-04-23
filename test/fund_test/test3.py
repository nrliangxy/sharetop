from sharetop.core.fund import get_fund_history, get_invest_position, get_period_change, \
    get_types_percentage, get_base_info, get_industry_distribution

# h = get_fund_history("010434")

# print(h)

# l = get_invest_position("010434", "2021-03-31")
# print(l)

# k = get_period_change("010434")

# print(k)

# p = get_types_percentage("010434")
# print(p)

# b = get_base_info("010434")

b = get_industry_distribution("010434")

print(b)