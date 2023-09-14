import pkgutil
import six


class ModuleProxyCache(dict):
    def __missing__(self, key):
        if '.' not in key:
            return __import__(key)

        module_name, class_name = key.rsplit('.', 1)
        _module = __import__(module_name, {}, {}, [class_name])
        handler = getattr(_module, class_name)
        self[key] = handler

        return handler


def import_string(path):
    result = _cache[path]
    return result


def import_submodules(context, root_module, path):
    for loader, module_name, is_pkg in pkgutil.walk_packages(path, root_module + '.'):
        module = __import__(module_name, globals(), locals(), ['__name__'])
        for k, v in six.iteritems(vars(module)):
            if not k.startswith('_'):
                context[k] = v
        context[module_name] = module


_cache = ModuleProxyCache()

print("_cache===========", _cache)
