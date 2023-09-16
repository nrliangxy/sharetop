import glob
import importlib
import os


def camel_to_snake(camel_case_str):
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


def get_all_services_map():
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
    for item_paths in [bond_yield_paths, car_paths]:
        for _ in item_paths:
            all_file_names.append(os.path.basename(_).replace(".py", ""))
    # all_file_names = [os.path.basename(_).replace(".py", "") for _ in all_file_paths]
    print("all_file_names=======:", all_file_names)
    for module in all_file_names:
        if module.startswith("_"):
            continue
        try:
            # > 自动获取 所有文件中的 XxxxServices
            # module_obj = importlib.import_module(f"sharetop.core.bond_yield.{module}")
            package_name = module.replace("_services", "")
            print('package_name=========:', package_name)
            module_obj = importlib.import_module(f"sharetop.core.{package_name}.{module}")
            services_cls_strs = [_ for _ in dir(module_obj) if _.endswith("Services")]

            for services_cls_str in services_cls_strs:
                # 驼峰->下划线 AaaBbServices -> aaa_bb
                services_cls_str_snake = camel_to_snake(services_cls_str).replace("_services", "")
                map_dic[services_cls_str_snake] = getattr(module_obj, services_cls_str)
        except Exception:
            import traceback
            # traceback.print_exc()
            raise ValueError(f"从{module}文件中导入服务类异常: {traceback.format_exc()}")

    return map_dic


MAP_DIC = get_all_services_map()


class BasicTop:
    def __init__(self, token):
        self.token = token
        self.class_map = MAP_DIC

    def common_exec_func(self, class_code: str, func_code: str, func_params: dict, class_params=None):
        if class_params is None:
            class_params = {}
        try:
            print("self.class_map11111:", self.class_map)
            if class_code not in self.class_map.keys():
                self.class_map = get_all_services_map()
                print("self.class_map22222:", self.class_map)
                raise ValueError(f"{class_code}不合法, 请输入 {list(self.class_map.keys())} 中内容 !")
            cls_obj = self.class_map[class_code]
            print("cls_obj====:", cls_obj)
            class_params.update({"token": self.token})
            print("class_params===:", class_params)
            func_obj = getattr(cls_obj(**class_params), f"{class_code}_{func_code}")
            return_data = func_obj(**func_params)
            print("return_data=======:", return_data)
        except Exception as err:
            import traceback
            traceback.print_exc()
            return_data = dict(status="error", message=str(err), detail_message=str(traceback.format_exc()))
        finally:
            res_data = dict(status="success", data=return_data)
        return res_data


if __name__ == '__main__':
    token = "000"
    sharetop_obj = BasicTop(token)
    d = sharetop_obj.common_exec_func("bond_yield", "real_time", {}, {"bond_name": "gcny10"})
    print(d)
