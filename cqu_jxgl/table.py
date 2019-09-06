"""table

解析课程表，生成 icalendar 文件
"""
from bs4 import BeautifulSoup, Tag

def text_or_hidevalue(td: Tag) -> str:
    """取出 HTML 标签内部文本，如果没有或者为空白，则取出 hidevalue 属性的值

    :param td: 一个 HTML td 标签"""
    value = td.text
    if value:
        return value
    else:
        return td["hidevalue"]
