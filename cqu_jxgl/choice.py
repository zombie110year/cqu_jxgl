"""选课
"""

from bs4 import BeautifulSoup, Tag
from copy import deepcopy


class Choice:
    def __init__(self, id: str = None,
                 course_id: str = None, left: int = None,
                 schdule: list = None, location: list = None):
        self.id = id
        self.course_id = course_id
        self.left = left
        self.schdule = schdule
        self.location = location

    def from_dict(self, D: dict):
        self.id = D["id"]
        self.course_id = D["course_id"]
        self.left = D["left"]
        self.schdule = D["schdule"]
        self.location = D["location"]

    def to_dict(self) -> dict:
        return deepcopy(self.__dict__)


class ChoiceTable:
    """一门课程的候选班级表"""
    SELECTOR = "#pageRpt > tr > td > table"

    def __init__(self, text: str):
        self.html = BeautifulSoup(text, "lxml").select_one(self.SELECTOR)

    def to_dict(self) -> list:
        """将 html 解析成 List[Dict]
        一条选课选项保留

        1. 任课教师
        2. 可选人数
        3. 上课时间
        4. 上课地点

        信息。"""
        result = []
        # 去除表头
        content = self.html.select("tr")[2:]
        length = len(content)
        i = 0
        while i < length:
            workspace = {
                "teacher": None,
                "course_id": None,
                "left": 0,
                "schdule": [],
                "location": [],
            }
            # cr 当前行 current row
            cr = content[i]
            size = int(cr.select_one("td")["rowspan"])
            workspace["teacher"] = cr.select_one(
                "td:nth-child(2)").text.strip()
            workspace["course_id"] = cr.select_one(
                "td:nth-child(3)").text.strip()
            workspace["left"] = int(cr.select_one(
                "td:nth-child(7)").text.strip())
            workspace["schdule"].append(
                cr.select_one("td:nth-child(8)").text.strip().replace("\xa0", ""))
            for j in range(1, size):
                workspace["schdule"].append(
                    content[i + j].select_one("td:nth-child(1)").text.strip().replace("\xa0", ""))
            workspace["location"].append(
                cr.select_one("td:nth-child(9)").text.strip())
            for j in range(1, size):
                workspace["location"].append(
                    content[i + j].select_one("td:nth-child(2)").text.strip())
            result.append(deepcopy(workspace))
            i += size
        return result
