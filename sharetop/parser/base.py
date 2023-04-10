from lxml import etree
from jsonpath import jsonpath
from typing import Any, Callable, Dict, List, TypeVar, Union


class BaseParse:
    def __int__(self, *args, **kwargs):
        pass

    def parse_html(self, html):
        return etree.HTML(html)

    def parse_json(self, json_response, json_par='$..klines[:]'):
        json_r: List[str] = jsonpath(json_response, json_par)
        return json_r

