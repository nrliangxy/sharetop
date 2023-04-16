from sharetop.core.stock import get_daily_billboard

d = get_daily_billboard("2023-04-11", "2023-04-13")

r = d.to_dict("records")

print(r)