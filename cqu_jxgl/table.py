"""table

解析课程表，生成 icalendar 文件
"""
import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, Tag
from icalendar import Calendar, Event

from .data.time import 沙坪坝校区作息时间, 虎溪校区作息时间, 周, 周_中文转数字


def text_or_hidevalue(td: Tag) -> str:
    """取出 HTML 标签内部文本，如果没有或者为空白，则取出 hidevalue 属性的值

    :param td: 一个 HTML td 标签"""
    value = td.text
    if value:
        return value
    else:
        return td.attrs.get("hidevalue", "Unknown")


def make_range(string: str) -> 'tuple[range]':
    """将 ``1-9``, ``1-4,6-9`` 这样的字符串解析为 range 组成的序列。
    源字符串中 ``s-e`` 表示一个闭区间
    """
    ans = list()
    for component in string.split(","):
        r = tuple(map(lambda x: int(x), component.split("-")))
        ans.append(range(r[0], r[-1] + 1))
    return tuple(ans)


def flat_ranges(ranges: list) -> list:
    """展开 ranges 组成的列表
    """
    ans = []
    for r in ranges:
        ans.extend(r)
    return ans


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


class 课程:
    """一个课程的基本要素"""

    __slots__ = ("_课程代码", "_课程名", "_学分", "_总学时", "_讲授学时", "_上机学时",
                 "_任课教师", "_周次", "_节次", "_地点", "_作息时间")

    def __init__(self, 课程, 学分, 总学时, 讲授学时, 上机学时, 任课教师, 周次, 节次, 地点,
                 作息时间: dict):
        """所有参数都是字符串, 解析工作由类自动完成。
        除了 作息时间 必须是 沙坪坝或虎溪作息时间
        """
        m课程 = re.match(r"\[([a-zA-Z0-9]+)\](\S+)", 课程)
        self._课程代码 = m课程[1]
        self._课程名 = m课程[2]
        self._学分 = float(学分)
        self._总学时 = float(总学时)
        self._讲授学时 = float(讲授学时)
        self._上机学时 = float(上机学时)
        self._任课教师 = 任课教师
        self._周次 = 周次
        self._节次 = 节次
        self._地点 = 地点
        self._作息时间 = 作息时间

    @property
    def 课程代码(self) -> str:
        """形如 MSE30005 的课程代码"""
        return self._课程代码

    @property
    def 课程名(self) -> str:
        """课程名称"""
        return self._课程名

    @property
    def 课程(self) -> str:
        """课程代码 + 课程名"""
        return f"[{self._课程代码}]{self._课程名}"

    @property
    def 学分(self) -> float:
        return self._学分

    @property
    def 总学时(self) -> float:
        return self._总学时

    @property
    def 上机学时(self) -> float:
        return self._上机学时

    @property
    def 讲授学时(self) -> float:
        return self._讲授学时

    @property
    def 任课教师(self) -> str:
        return self._任课教师

    @property
    def 地点(self) -> str:
        return self._地点

    @property
    def 课程时间(self) -> (timedelta, timedelta):
        """生成本学期内此课程的第一节课的上课下课时间(相对于学期开始)
        """
        第一课周次 = flat_ranges(make_range(self._周次))[0]
        base = timedelta(days=7) * (第一课周次 - 1)
        上课, 下课 = make_week_offset(self._节次, self._作息时间)
        return base + 上课, base + 下课

    @property
    def ical_title(self):
        raise Exception("在子类实现")

    @property
    def ical_summary(self):
        raise Exception("在子类实现")

    @property
    def ical_location(self):
        raise Exception("在子类实现")


class 理论课(课程):
    __slots__ = ("类别", "授课方式", "考核方式")

    def __init__(self, 课程, 学分, 总学时, 讲授学时, 上机学时, 类别, 授课方式,
                 考核方式, 任课教师, 周次, 节次, 地点, 作息时间: dict):
        """
        """
        super().__init__(课程, 学分, 总学时, 讲授学时, 上机学时, 任课教师,
                         周次, 节次, 地点, 作息时间)
        self.类别 = 类别
        self.授课方式 = 授课方式
        self.考核方式 = 考核方式

    @property
    def ical_title(self):
        return f"{self.课程名}"

    @property
    def ical_summary(self):
        return f"考核方式: {self.考核方式}, 类别: {self.类别}"

    @property
    def ical_location(self):
        return f"{self.地点}"


class 实验课(课程):
    __slots__ = ("课程项目", "实验值班教师")

    def __init__(self, 课程, 学分, 总学时, 讲授学时, 上机学时, 课程项目, 任课教师,
                 实验值班教师, 周次, 节次, 地点, 作息时间: dict):
        super().__init__(课程, 学分, 总学时, 讲授学时, 上机学时, 任课教师,
                         周次, 节次, 地点, 作息时间)
        self.课程项目 = 课程项目
        self.实验值班教师 = 实验值班教师

    @property
    def ical_title(self):
        return f"{self.课程名}-{self.课程项目}"

    @property
    def ical_summary(self):
        return f"课程项目: {self.课程项目}; 实验值班教师: {self.实验值班教师}"

    @property
    def ical_location(self):
        return f"{self.地点}"


def parse_课程(html: BeautifulSoup, 作息: dict) -> "generate[课程]":
    """从获取的 html 中解析出课程实例
    """
    for attributes, table in zip(html.select("div.page_group > table > tr > td"), html.select("body > table.page_table")):
        if "讲授/上机" in attributes.text:
            # 理论课
            for tr in table.select("tbody > tr"):
                yield parse_理论课(tr, 作息)
        elif "实验" in attributes.text:
            # 实验课
            for tr in table.select("tbody > tr"):
                yield parse_实验课(tr, 作息)

def parse_理论课(tr: Tag, 作息: dict) -> 理论课:
    # [1:] 是为了把序号去掉
    tds = list(map(text_or_hidevalue, tr.select("td")))[1:]
    return 理论课(*tds, 作息)

def parse_实验课(tr: Tag, 作息: dict) -> 实验课:
    # [1:] 是为了把序号去掉
    tds = list(map(text_or_hidevalue, tr.select("td")))[1:]
    return 实验课(*tds, 作息)

def make_ical(html: str, 学期开始日期: datetime, 作息: dict) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//Zombie110year//CQU Class Table//")
    cal.add("version", "2.0")
    for 课程 in parse_课程(BeautifulSoup(html, 'lxml'), 作息):
        cal.add_component(build_event(课程, 学期开始日期))
    return cal.to_ical()

def build_event(课程, 学期开始日期: datetime) -> Event:
    ev = Event()
    ev.add("summary", 课程.ical_title)
    ev.add("location", 课程.ical_location)
    ev.add("description", 课程.ical_summary)
    上课, 下课 = 课程.课程时间
    ev.add("dtstart", 上课 + 学期开始日期)
    ev.add("dtend", 下课 + 学期开始日期)
    ev.add("rrule", {
        "freq": "weekly",
        "count": len(flat_ranges(make_range(课程._周次)))
    })
    return ev
