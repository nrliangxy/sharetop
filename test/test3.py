from sharetop.core.stock import get_daily_billboard

d = get_daily_billboard()

r = d.to_dict("records")

print(r)