from sharetop.core.stock.quarterly_report import get_company_report


d = get_company_report("601933", "半年报")
print(d)

r = d.to_dict("records")
print(r)
