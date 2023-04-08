from lxml import etree


class BaseParse:
    def __int__(self, *args, **kwargs):
        pass

    def parser_obj(self, html):
        return etree.HTML(html)
