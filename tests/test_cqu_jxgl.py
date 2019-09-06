from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from cqu_jxgl import __version__
from cqu_jxgl.data.time import 沙坪坝校区作息时间
from cqu_jxgl.table import (build_event, flat_ranges, make_range,
                            make_week_offset, parse_实验课, parse_理论课,
                            text_or_hidevalue, 实验课, 理论课, 课程)


def test_version():
    assert __version__ == '0.1.0'


def test_text_or_hidevalue():
    raw = """
    <td style='width:4%;text-align:center'>1<br></td>
    <td style='width:15%;text-align:left'>[MSE31001]材料X射线衍射与电子显微学<br></td>
    <td style='width:4%;text-align:right'>3.00<br></td>
    <td style='width:4%;text-align:right'>48.0<br></td>
    <td style='width:4%;text-align:right'>40.0<br></td>
    <td style='width:4%;text-align:right'>0.0<br></td>
    <td style='width:15%;text-align:left'>MSE31001-001德拜相机与X射线衍射仪构造及使用<br></td>
    <td style='width:10%;text-align:left'>刘传璞<br></td>
    <td style='width:10%;text-align:left'>辛仁龙<br></td>
    <td style='width:9%;text-align:left'>03<br></td>
    <td style='width:8%;text-align:left'>一[9-10节]<br></td>
    <td style='width:13%;text-align:left'>A综合实验楼410<br></td>
    <td style='width:4%;text-align:center'>13<br></td>
    <td style='width:15%;text-align:left' hidevalue='[MSE32121]材料力学性能实验'><br></td>
    <td style='width:4%;text-align:right' hidevalue='0.50'><br></td>
    <td style='width:4%;text-align:right' hidevalue='8.0'><br></td>
    <td style='width:4%;text-align:right' hidevalue='0.0'><br></td>
    <td style='width:4%;text-align:right' hidevalue='0.0'><br></td>
    <td style='width:15%;text-align:left'>MSE32121-005低温冲击试验<br></td>
    <td style='width:10%;text-align:left'>王柯,冉春华<br></td>
    <td style='width:10%;text-align:left'>冉春华<br></td>
    <td style='width:9%;text-align:left'>10<br></td>
    <td style='width:8%;text-align:left'>三[5-6节]<br></td>
    <td style='width:13%;text-align:left'>A综合实验楼235<br></td>
    """
    html = BeautifulSoup(raw, 'lxml')
    ans = ["1", "[MSE31001]材料X射线衍射与电子显微学", "3.00", "48.0",
           "40.0", "0.0", "MSE31001-001德拜相机与X射线衍射仪构造及使用",
           "刘传璞", "辛仁龙", "03", "一[9-10节]", "A综合实验楼410", "13",
           "[MSE32121]材料力学性能实验", "0.50", "8.0", "0.0", "0.0",
           "MSE32121-005低温冲击试验", "王柯,冉春华", "冉春华", "10",
           "三[5-6节]", "A综合实验楼235"]
    res = list(map(lambda td: text_or_hidevalue(td), html.select("td")))
    for a, r in zip(ans, res):
        assert a == r


def test_make_range():
    assert make_range("1-9") == (range(1, 10), )
    assert make_range("1-4,6-9") == (range(1, 5), range(6, 10))
    assert make_range("1,6,9") == (range(1, 2), range(6, 7), range(9, 10))
    assert make_range("11,15-17") == (range(11, 12), range(15, 18))
    assert make_range("14") == (range(14, 15), )
    assert make_range("03") == (range(3, 4), )


def test_flat_ranges():
    assert flat_ranges([range(1, 3), range(4, 9)]) == [1, 2, 4, 5, 6, 7, 8]
    assert flat_ranges([range(1, 3), ]) == [1, 2]
    assert flat_ranges([range(4), ]) == [0, 1, 2, 3]
    assert flat_ranges([]) == []


def test_make_week_offset():
    # 以沙坪坝作息时间测试
    assert make_week_offset(
        "一[1-2节]", 沙坪坝校区作息时间) == (timedelta(hours=8), timedelta(hours=9, minutes=40))
    assert make_week_offset("一[9-10节]", 沙坪坝校区作息时间) == (
        timedelta(hours=19, minutes=30), timedelta(hours=21, minutes=10))
    assert make_week_offset("三[3-4节]", 沙坪坝校区作息时间) == (timedelta(
        days=2, hours=10, minutes=10), timedelta(days=2, hours=11, minutes=50))
    assert make_week_offset("五[1-4节]", 沙坪坝校区作息时间) == (
        timedelta(days=4, hours=8), timedelta(days=4, hours=11, minutes=50))
    assert make_week_offset("六[7-8节]", 沙坪坝校区作息时间) == (timedelta(
        days=5, hours=16, minutes=40), timedelta(days=5, hours=18, minutes=20))
    assert make_week_offset("日[5-8节]", 沙坪坝校区作息时间) == (timedelta(
        days=6, hours=14, minutes=30), timedelta(days=6, hours=18, minutes=20))


def test_课程():
    x = 课程("[MSE31001]材料X射线衍射与电子显微学", "3.0", "48.0", "40.0", "0.0",
           "辛仁龙", "03", "一[9-10节]", "A综合实验楼410", 沙坪坝校区作息时间)
    assert x.课程代码 == "MSE31001"
    assert x.课程名 == "材料X射线衍射与电子显微学"
    assert x.课程时间 == (timedelta(hours=19, minutes=30),
                      timedelta(hours=21, minutes=10))


def test_parse_理论课():
    html = BeautifulSoup("""<tr><td style="width:4%;text-align:center">20<br/></td>
    <td style="width:21%;text-align:left">[META30010]冶金学导论<br/></td>
    <td style="width:4%;text-align:right">2.00<br/></td>
    <td style="width:5%;text-align:right">32.0<br/></td>
    <td style="width:4%;text-align:right">32.0<br/></td>
    <td style="width:4%;text-align:right">0.0<br/></td>
    <td style="width:10%;text-align:left">专业基础选修课<br/></td>
    <td style="width:5%;text-align:left">理论<br/></td>
    <td style="width:5%;text-align:center">考试<br/></td>
    <td style="width:7%;text-align:left">刘守平<br/></td>
    <td style="width:9%;text-align:left">1-4,6-9<br/></td>
    <td style="width:9%;text-align:left">五[5-6节]<br/></td>
    <td style="width:13%;text-align:left">B二417<br/></td>
    </tr>""", "lxml")
    tr = html.select_one("tr")
    x = parse_理论课(tr, 沙坪坝校区作息时间)
    y = 理论课("[META30010]冶金学导论", "2.00", "32.0", "32.0", "0.0",
            "专业基础选修课", "理论", "考试", "刘守平", "1-4,6-9",
            "五[5-6节]", "B二417", 沙坪坝校区作息时间)

    assert x._课程代码 == y._课程代码
    assert x._课程名 == y._课程名
    assert x._学分 == y._学分
    assert x._总学时 == y._总学时
    assert x._讲授学时 == y._讲授学时
    assert x._上机学时 == y._上机学时
    assert x._任课教师 == y._任课教师
    assert x._周次 == y._周次
    assert x._节次 == y._节次
    assert x._地点 == y._地点
    assert x._作息时间 == y._作息时间
    assert x.类别 == y.类别
    assert x.授课方式 == y.授课方式
    assert x.考核方式 == y.考核方式


def test_parse_实验课():
    html = BeautifulSoup("""<tr>
    <td style='width:4%;text-align:center'>3<br></td>
    <td style='width:15%;text-align:left' hidevalue='[MSE31001]材料X射线衍射与电子显微学'><br></td>
    <td style='width:4%;text-align:right' hidevalue='3.00'><br></td>
    <td style='width:4%;text-align:right' hidevalue='48.0'><br></td>
    <td style='width:4%;text-align:right' hidevalue='40.0'><br></td>
    <td style='width:4%;text-align:right' hidevalue='0.0'><br></td>
    <td style='width:15%;text-align:left'>MSE31001-003点阵参数的精确测定<br></td>
    <td style='width:10%;text-align:left'>刘传璞<br></td>
    <td style='width:10%;text-align:left'>辛仁龙<br></td>
    <td style='width:9%;text-align:left'>06<br></td>
    <td style='width:8%;text-align:left'>一[9-10节]<br></td>
    <td style='width:13%;text-align:left'>A综合实验楼410<br></td>
    </tr>""", "lxml")
    tr = html.select_one("tr")
    x = parse_实验课(tr, 沙坪坝校区作息时间)
    y = 实验课("[MSE31001]材料X射线衍射与电子显微学", "3.00", "48.0", "40.0", "0.0",
            "MSE31001-003点阵参数的精确测定", "刘传璞", "辛仁龙", "06", "一[9-10节]",
            "A综合实验楼410", 沙坪坝校区作息时间)
    assert x._课程代码 == y._课程代码
    assert x._课程名 == y._课程名
    assert x._学分 == y._学分
    assert x._总学时 == y._总学时
    assert x._讲授学时 == y._讲授学时
    assert x._上机学时 == y._上机学时
    assert x._任课教师 == y._任课教师
    assert x._周次 == y._周次
    assert x._节次 == y._节次
    assert x._地点 == y._地点
    assert x._作息时间 == y._作息时间
    assert x.课程项目 == y.课程项目
    assert x.实验值班教师 == y.实验值班教师


def test_build_event():
    c = 理论课("[META30010]冶金学导论", "2.00", "32.0", "32.0", "0.0",
            "专业基础选修课", "理论", "考试", "刘守平", "1-4,6-9",
            "五[5-6节]", "B二417", 沙坪坝校区作息时间)
    ev = build_event(c, datetime(2019, 9, 2))
    out = ev.to_ical()
    assert out == b'BEGIN:VEVENT\r\nSUMMARY:\xe5\x86\xb6\xe9\x87\x91\xe5\xad\xa6\xe5\xaf\xbc\xe8\xae\xba\r\nDTSTART;VALUE=DATE-TIME:20190906T143000\r\nDTEND;VALUE=DATE-TIME:20190906T161000\r\nRRULE:FREQ=WEEKLY;COUNT=8\r\nDESCRIPTION:\xe8\x80\x83\xe6\xa0\xb8\xe6\x96\xb9\xe5\xbc\x8f: \xe8\x80\x83\xe8\xaf\x95\\, \xe7\xb1\xbb\xe5\x88\xab: \xe4\xb8\x93\xe4\xb8\x9a\xe5\x9f\xba\xe7\xa1\x80\xe9\x80\x89\xe4\xbf\xae\xe8\xaf\xbe\r\nLOCATION:B\xe4\xba\x8c417\r\nEND:VEVENT\r\n'
