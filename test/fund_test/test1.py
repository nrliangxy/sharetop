from sharetop.core.fund import get_fund_codes

d = get_fund_codes("zq")
# item = "013261,太平睿享混合C,TPRXHHC,-1.44,,0,2021-09-17,1,1,2023-04-21,0.9856,0.9856,2021-09-17,1,0.00%,,,,"
# item = "017676,广发积极养老目标五年持有期混合发起式(FOF),GFJJYLMBWNCYQHHFQSFOF,,,0,,,,,,,2022-12-28,3,0.10%,1,0.10%,1,1.00%"
item = "006360,财通资管鸿益中短债债券A,CTZGHYZDZZQA,,0.096,14,2018-09-03,1,1,2023-04-21,1.0597,1.1557,2018-09-03,1,0.04%,1,0.04%,1,0.40%"
# print(d)
#
# h = d.to_dict("records")
#
# print(h)
# 006360
# l = '["180003,银华-道琼斯88指数,YHDQS88ZS,544.781612,2.2333,12,2004-08-11,1,1,2023-04-20,1.1912,3.4245,2004-08-11,1,0.15%,1,0.15%,1,1.50%","310318,申万菱信沪深300指数增强A,SWLXHS300ZSZQA,504.507877,0.7925,12,2004-11-29,1,1,2023-04-20,3.0828,3.8753,2004-11-29,1,0.12%,1,0.12%,1,1.20%"]'

# print(eval(l))


def fund_data(item):
    r1_list = item.split(",")
    print(r1_list)
    code = r1_list[0]
    name = r1_list[1]
    base_yield = r1_list[3]
    # funded_time = r1_list[6]
    funded_time = r1_list[12]
    now_time = r1_list[9]
    unit_value = r1_list[10]
    accumulate_value = r1_list[11]
    value_list = [code, name, base_yield, funded_time, now_time, unit_value, accumulate_value]
    key_list = ["基金代码", "基金名称", "自成立以来收益(%)", "成立时间", "净值时间", "单位净值", "累计净值"]
    return dict(zip(key_list, value_list))

# print(fund_data(item))