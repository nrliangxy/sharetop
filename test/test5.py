from sharetop.core.stock.quarterly_report import get_company_report


d = get_company_report("601933")
print(d)

r = d.to_dict("records")
print(r)

def h(k=0, l=1, **kwargs):
    print(kwargs)
    print(k)
    print(l)

h(3, 8, n=9)