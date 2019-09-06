from datetime import timedelta

from bs4 import BeautifulSoup

from cqu_jxgl import __version__
from cqu_jxgl.table import make_range, make_week_offset, text_or_hidevalue, 课程
from cqu_jxgl.data.time import 沙坪坝校区作息时间


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
    assert make_range("1-9") == (1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert make_range("1-4,6-9") == (1, 2, 3, 4, 6, 7, 8, 9)
    assert make_range("1,6,9") == (1, 6, 9)
    assert make_range("11,15-17") == (11, 15, 16, 17)
    assert make_range("14") == (14, )
    assert make_range("03") == (3, )


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
    assert list(x.课程时间) == [(timedelta(days=14, hours=19, minutes=30), timedelta(
        days=14, hours=21, minutes=10)), ]
