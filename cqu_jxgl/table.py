"""table

解析课程表，生成 icalendar 文件
"""
import re

from bs4 import BeautifulSoup, Tag


def text_or_hidevalue(td: Tag) -> str:
    """取出 HTML 标签内部文本，如果没有或者为空白，则取出 hidevalue 属性的值

    :param td: 一个 HTML td 标签"""
    value = td.text
    if value:
        return value
    else:
        return td["hidevalue"]


def make_range(string: str) -> 'tuple[int]':
    """将 ``1-9``, ``1-4,6-9`` 这样的字符串解析为数字序列。
    区间是闭合的
    """
    ans = list()
    for component in string.split(","):
        r = tuple(map(lambda x: int(x), component.split("-")))
        for i in range(r[0], r[-1] + 1):
            ans.append(i)
    return tuple(ans)
