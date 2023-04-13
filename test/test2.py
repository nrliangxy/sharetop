from sharetop.core.stock import get_real_time_data, get_market_real_time

# d = get_real_time_data(["XPEV", '300033'])

# print(d)

h = get_market_real_time(['ETF'])
print(h)
# j = h.to_dict("records")
# print(j)
