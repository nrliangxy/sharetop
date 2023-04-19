from sharetop.core.stock.quarterly_report import get_company_report_base


d = get_company_report_base(["601933", "002714"])
print(d)

r = d.to_dict("records")
print(r)

