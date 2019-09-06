"""app

主要的应用逻辑
"""
from datetime import datetime

from .data.time import 沙坪坝校区作息时间, 虎溪校区作息时间
from .login import Session
from .table import make_ical


class App:
    def __init__(self, username: str, password: str):
        self.session = Session(username, password)

    def getRawClassTable(self, 学年学期) -> str:
        """获取原始的 HTML，包含课程表"""
        url = "http://jxgl.cqu.edu.cn/znpk/Pri_StuSel_rpt.aspx"
        param = {
            "Sel_XNXQ": 学年学期,
            "rad": "on",  # 未知含义
            "px": 1,  # 排序
            # （1 表示按时间排序，0表示按课程/环节排序，由于解析课表的程序是以时间顺序写的，所以不要改）
        }
        resp = self.session.post(url, data=param)
        if resp.status_code == 200:
            return resp.text
        else:
            return ""

    def writeICS(self, 学年学期: int, 学期开始日期: datetime, 作息时间: dict):
        """获取课程表, 解析并写入 icalendar 文件"""
        html = self.getRawClassTable(学年学期)
        ical = make_ical(html, 学期开始日期, 作息时间)
        with open("class-table.ics", "wb") as out:
            out.write(ical)
            print("write file: class-table.ics")
