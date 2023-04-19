from sharetop.core.stock import get_history_data
# d = get_history_data("002594")

d = get_history_data("588200")
# d = get_history_data([{"code": "002594", "klt": 102}, {"code": "000333", "klt": 102}])
# d = get_history_data("002594", klt=102)
print(d)
