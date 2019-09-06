"""一些关于时间的数据"""

from datetime import timedelta

# 作息时间，按节次计算
# key: 一天的第几节课
# value: (上课, 下课)；都是相对于当天 00:00 的 timedelta
沙坪坝校区作息时间 = {
    1: (timedelta(hours=8, minutes=0), timedelta(hours=8, minutes=45)),
    2: (timedelta(hours=8, minutes=55), timedelta(hours=9, minutes=40)),
    3: (timedelta(hours=10, minutes=10), timedelta(hours=10, minutes=55)),
    4: (timedelta(hours=11, minutes=5), timedelta(hours=11, minutes=50)),
    5: (timedelta(hours=14, minutes=30), timedelta(hours=15, minutes=15)),
    6: (timedelta(hours=15, minutes=25), timedelta(hours=16, minutes=10)),
    7: (timedelta(hours=16, minutes=40), timedelta(hours=17, minutes=25)),
    8: (timedelta(hours=17, minutes=35), timedelta(hours=18, minutes=20)),
    9: (timedelta(hours=19, minutes=30), timedelta(hours=20, minutes=15)),
    10: (timedelta(hours=20, minutes=25), timedelta(hours=21, minutes=10)),
    11: (timedelta(hours=21, minutes=10), timedelta(hours=22, minutes=5)),
}
# 作息时间，按节次计算
# key: 一天的第几节课
# value: (上课, 下课)；都是相对于当天 00:00 的 timedelta
虎溪校区作息时间 = {
    1: (timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=15)),
    2: (timedelta(hours=9, minutes=25), timedelta(hours=10, minutes=10)),
    3: (timedelta(hours=10, minutes=30), timedelta(hours=11, minutes=15)),
    4: (timedelta(hours=11, minutes=25), timedelta(hours=12, minutes=10)),
    5: (timedelta(hours=14, minutes=0), timedelta(hours=14, minutes=45)),
    6: (timedelta(hours=14, minutes=55), timedelta(hours=15, minutes=40)),
    7: (timedelta(hours=16, minutes=0), timedelta(hours=16, minutes=45)),
    8: (timedelta(hours=16, minutes=55), timedelta(hours=17, minutes=40)),
    9: (timedelta(hours=19, minutes=0), timedelta(hours=19, minutes=45)),
    10: (timedelta(hours=19, minutes=55), timedelta(hours=20, minutes=40)),
    11: (timedelta(hours=20, minutes=50), timedelta(hours=21, minutes=35)),
}

周 = {
    1: timedelta(days=0), # 星期一
    2: timedelta(days=1), # 星期二
    3: timedelta(days=2), # 星期三
    4: timedelta(days=3), # 星期四
    5: timedelta(days=4), # 星期五
    6: timedelta(days=5), # 星期六
    7: timedelta(days=6), # 星期日
}

周_中文转数字 = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "日": 7,
    "天": 7,
}
