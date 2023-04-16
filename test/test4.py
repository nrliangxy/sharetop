import requests
from sharetop.core.stock import get_all_company_quarterly_report

# d = get_all_company_quarterly_report('2020-03-31')


# r = d.to_dict("records")

# print(r)

# {'股票代码': '601933', '股票简称': '永辉超市', '公告日期': '2020-04-29 00:00:00', '营业收入': 29256581788.22, '营业收入同比增长': 31.5735762141, '营业收入季度环比': 37.1387, '净利润': 1567503383.38,
#  '净利润同比增长': 39.47, '净利润季度环比': 6073.4245, '每股收益': 0.17, '每股净资产': 2.267349045, '净资产收益率': 7.64, '销售毛利率': 22.8390891756, '每股经营现金流量': 0.440180275222}

url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308812788184778955_1681551007075&sortColumns=REPORTDATE&sortTypes=-1&pageSize=50&pageNumber=1&columns=ALL&filter=(SECURITY_CODE="900942")(DATEMMDD="年报")&reportName=RPT_LICO_FN_CPD'

r = requests.get(url)
print(r.text)