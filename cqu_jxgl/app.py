"""app

主要的应用逻辑
"""
from .login import Session

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
