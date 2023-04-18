from sharetop.core.stock import get_history_data
# d = get_history_data("002594")

d = get_history_data(["002594", "300033", "601933", "000333", "002186", "000001", "601633", "000430", "515220",
                      "159825", "301246", "002475", "603281", "002597", "300363", "600153", "688275", "601633", "300454"])
# d = get_history_data([{"code": "002594", "klt": 102}, {"code": "000333", "klt": 102}])
# d = get_history_data("002594", klt=102)
print(d)
