import pkgutil
import importlib
import inspect


def get_classes_and_functions_in_package(package_name):
    items = {}  # 用于存储类和函数的字典

    # 使用 pkgutil.walk_packages 遍历包内的模块
    for loader, module_name, is_pkg in pkgutil.walk_packages(package_name.__path__):
        # 导入模块
        module = importlib.import_module(package_name.__name__ + '.' + module_name)

        # 获取模块内的成员
        for name, obj in inspect.getmembers(module):
            # 检查成员是否是函数或类
            if inspect.isfunction(obj) or inspect.isclass(obj):
                items[name] = obj

    return items


# 获取本项目中的包
import sharetop  # 替换成你的项目中的包名

# 调用函数，传入包的名称（模块）
classes_and_functions_in_package = get_classes_and_functions_in_package(sharetop)

# 打印包内的类和函数
for name, item in classes_and_functions_in_package.items():
    print(f"Name: {name}")
    if inspect.isfunction(item):
        print("Type: Function")
    elif inspect.isclass(item):
        print("Type: Class")
    print()
