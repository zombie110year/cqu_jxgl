import re
from datetime import datetime
from getpass import getpass
from sys import argv

from . import __version__
from .data.time import 沙坪坝校区作息时间, 虎溪校区作息时间
from .app import App


class CommandParser:
    def __init__(self):
        self.username = input("用户名: ").strip()
        self.password = getpass("密码: ").strip()
        self.term = self.getTerm()
        self.startdate = self.getStartDate()
        self.作息时间 = self.get作息时间()

    def getTerm(self) -> int:
        term = input("学期号: ").strip()
        if re.fullmatch(r"(?P<year>\d{4,})(?P<term>\d)", term):
            return term
        else:
            raise ValueError(f"{term} 不是一个有效的学期号, 应为类似于 20190 这样的数字")

    def getStartDate(self) -> datetime:
        date = input("学期开始日期: ").strip()
        m = re.fullmatch(
            r"(?P<year>\d{4,})(?P<month>\d{2})(?P<day>\d{2})", date)
        if m:
            year = int(m["year"])
            mon = int(m["month"])
            day = int(m["day"])
            date = datetime(year, mon, day)
            return date
        else:
            raise ValueError(f"{date} 不是有效的日期号，应为类似于 20190101 这样的数字")

    def get作息时间(self) -> dict:
        print("选择作息时间：")
        print("1) 沙坪坝校区")
        print("2) 虎溪校区")
        code = int(input("1|2> ").strip())
        assert code in [1, 2]
        choice = {
            1: 沙坪坝校区作息时间,
            2: 虎溪校区作息时间
        }[code]
        return choice

    @staticmethod
    def help():
        print((
            "Usage: cqu_schedule\n"
            "    登录并获取学生课程表 ics 文件"
        ))


def main():
    if len(argv) == 1:
        args = CommandParser()
        app = App(username=args.username, password=args.password)
        app.writeICS(args.term, args.startdate, args.作息时间)
    else:
        CommandParser.help()
