from sharetop.core.stock.bill_monitor import get_history_bill

d = get_history_bill("002714")

h = d.to_dict("records")
print(d)
print(h)

