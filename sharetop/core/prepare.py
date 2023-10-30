import glob
import importlib
import os

__all__ = ["BasicTop"]

import pandas as pd


def _camel_to_snake(camel_case_str):
    """驼峰命名 转换 下划线命名"""
    snake_case_str = ""
    for index in range(len(camel_case_str)):
        char = camel_case_str[index]
        if char.isupper() and index == 0:
            snake_case_str += char.lower()
        elif char.isupper() and index != 0:
            snake_case_str += "_" + char.lower()
        else:
            snake_case_str += char
    return snake_case_str


def _get_all_services_map():
    """获取所有 service 对象映射

    return {
        presto_sql: PrestoSqlServices,
        mongo_orm: MongoOrmServices,
    }
    """
    map_dic = dict()
    all_file_names = []
    dir_path = os.path.dirname(os.path.abspath(__file__))
    bond_yield_paths = glob.glob(f"{dir_path}/bond_yield/*_services.py")
    car_paths = glob.glob(f"{dir_path}/car/*_services.py")
    fund_paths = glob.glob(f"{dir_path}/fund/*_services.py")
    pig_paths = glob.glob(f"{dir_path}/pig/*_services.py")
    stock_paths = glob.glob(f"{dir_path}/stock/*_services.py")
    news_paths = glob.glob(f"{dir_path}/news/*_services.py")
    for item_paths in [bond_yield_paths, car_paths, fund_paths, pig_paths, stock_paths, news_paths]:
        for _ in item_paths:
            all_file_names.append(os.path.basename(_).replace(".py", ""))
    for module in all_file_names:
        if module.startswith("_"):
            continue
        try:
            # > 自动获取 所有文件中的 XxxxServices
            # module_obj = importlib.import_module(f"sharetop.core.bond_yield.{module}")
            package_name = module.replace("_services", "")
            module_obj = importlib.import_module(f"sharetop.core.{package_name}.{module}")
            services_cls_strs = [_ for _ in dir(module_obj) if _.endswith("Services")]

            for services_cls_str in services_cls_strs:
                # 驼峰->下划线 AaaBbServices -> aaa_bb
                services_cls_str_snake = _camel_to_snake(services_cls_str).replace("_services", "")
                map_dic[services_cls_str_snake] = getattr(module_obj, services_cls_str)
        except Exception:
            import traceback
            # traceback.print_exc()
            raise ValueError(f"从{module}文件中导入服务类异常: {traceback.format_exc()}")

    return map_dic


_MAP_DIC = _get_all_services_map()


class BasicTop:

    def __init__(self, token):
        self.token = token
        self.__class_map = _MAP_DIC

    def common_exec_func(self, exec_code: str, func_params=None, class_params=None):
        return_data = []
        if func_params is None:
            func_params = {}
        if class_params is None:
            class_params = {}
        try:
            class_code = exec_code.split("_to_")[0]
            if class_code not in self.__class_map.keys():
                self.__class_map = _get_all_services_map()
                raise ValueError(f"{class_code}不合法, 请输入 {list(self.__class_map.keys())} 中内容 !")
            cls_obj = self.__class_map[class_code]
            class_params.update({"token": self.token})
            func_obj = getattr(cls_obj(**class_params), f"{exec_code}")
            return_data = func_obj(**func_params)
        except Exception as err:
            import traceback
            traceback.print_exc()
            return_data = pd.DataFrame()
            return_data = dict(status="error", message=str(err), detail_message=str(traceback.format_exc()))
        finally:
            res_data = return_data
            # res_data = dict(status="success", data=return_data)
        return res_data

# if __name__ == '__main__':
#     token = "000"
#     sharetop_obj = BasicTop(token)
#     d = sharetop_obj.common_exec_func("bond_yield", "real_time", {}, {"bond_name": "gcny10"})
#     print(d)
