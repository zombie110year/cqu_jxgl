"""将形如
08:00-08:45
08:55-09:40
10:10-10:55
11:05-11:50
14:30-15:15
15:25-16:10
16:40-17:25
17:35-18:20
19:30-20:15
20:25-21:10
21:10-22:05

的时间表转换为与课程对应的字典:

{
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
"""

import re
from sys import stdin

text = map(lambda line: line.strip(), stdin.readlines())

print("{")

for i, line in enumerate(text):
    # line 为形如 08:00-08:45 的字符串
    # i 的初始值为 0
    start, end = line.split("-")
    # 处理 start
    m = re.match(r"(\d{,2}):(\d{,2})", start)
    s_start = f"timedelta(hours={int(m.group(1))}, minutes={int(m.group(2))})"
    # 处理 end
    m = re.match(r"(\d{,2}):(\d{,2})", end)
    s_end = f"timedelta(hours={int(m.group(1))}, minutes={int(m.group(2))})"

    print(f"    {i + 1}: ({s_start}, {s_end}),")

print("}")
