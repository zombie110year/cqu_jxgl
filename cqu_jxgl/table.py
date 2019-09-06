"""table

解析课程表，生成 icalendar 文件
"""
import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, Tag

from .data.time import 沙坪坝校区作息时间, 虎溪校区作息时间, 周, 周_中文转数字

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


def make_week_offset(string: str, 作息时间: dict) -> (timedelta, timedelta):
    """解析形如 "三[1-4节]" 的节次字符串这样的节次字符串，
    返回其相对于一周的开始的 上课、下课 时间偏移量"""
    pattern = re.compile(r"([一二三四五六日])\[([\d\-]+)节\]")
    m = pattern.match(string)
    周名 = m[1]
    周偏移 = 周[周_中文转数字[周名]]
    课时范围 = m[2]

    if "-" in 课时范围:
        # 连接课时
        start, end = map(lambda x: int(x), 课时范围.split("-"))
        上课 = 作息时间[start][0]
        下课 = 作息时间[end][-1]
    elif 课时范围 == "14":
        # 表示全天
        上课 = 作息时间[1][0]
        下课 = 作息时间[11][-1]
    elif re.match(r"\d+", 课时范围):
        # 单独课时
        课堂时间 = 作息时间[int(课时范围)]
        上课, 下课 = 课堂时间
    else:
        # 无法处理
        raise ValueError(f"无法识别的节次: {string}")

    return 上课 + 周偏移, 下课 + 周偏移
