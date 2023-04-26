# from sharetop.core.stock import get_history_data
# d = get_history_data("002594")

# d = get_history_data("微软")
# d = get_history_data([{"code": "002594", "klt": 102}, {"code": "000333", "klt": 102}])
# d = get_history_data("002594", klt=102)
import sharetop as sp
stock_code = ['300033', '516110']
# stock_code = '300033'
# d = sp.stock.get_real_time_data(stock_code)
# print(d)

d = sp.stock.get_daily_billboard()

print(d)