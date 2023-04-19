from sharetop.core.stock.bill_monitor import get_history_bill, get_real_time_bill

d = get_real_time_bill("002714")

h = d.to_dict("records")
print(d)
print(h)
