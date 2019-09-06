# 获取课表

向 `http://jxgl.cqu.edu.cn/znpk/Pri_StuSel_rpt.aspx` **POST** 表单:

```
Sel_XNXQ=20190&rad=on&px=1
```

分别表示 学年学期, 排序(1 代表按时间排序, 0 代表按课程/环节排序) 中间的 `rad` 项含义未知。
注意，此参数应当在请求体中传递，不能放在 URL 里。

响应体的 HTML 中, 选择器 `table.page_table > tbody > tr` 对应的元素就是表单数据中的各行.

---

学年学期值的规律暂时未知，猜测 `20190` 表示 2019-2020 学年第一学期。
但 2019-2020 第二学期不确定，可能为 `20191`。

## 解析课表

课表可以分为理论课/实验课两类，两种课表在 table 中的格式不一样。

理论课表头存在字符串 `讲授/上机`，实验课则是 `实验`。

在 html 页面中，是这样的结构：

```html
<div group="group" class="page_group"><!-- 声明下一个相邻表类型 --></div>
<table class="page_table"><!-- 表 --></table>
<!-- ... -->
<div group="group" class="page_group"><!-- 声明下一个相邻表类型 --></div>
<table class="page_table"><!-- 表 --></table>
```

由于数目与位置严格对应，因此用选择器:

```
# 注意没有 tbody
div.page_group[group="group"] > table > tr > td
# div.page_group 里也有 table.page_table，所以用 body 限制一下
body > table.page_table
```

分别选出两个列表，前者记录了对应的表属于理论课还是实验课，后者是各课程信息。

理论课中一个元组按

("序号", "课程", "学分", "总学时", "讲授学时", "上机学时",
"类别", "授课方式", "考核方式", "任课教师", "周次", "节次", "地点")

排列；实验课则是

("序号", "课程", "学分", "总学时", "讲授学时", "上机学时",
"项目代码名称", "任课教师", "实验值班教师", "周次", "节次", "地点")

如果当前元组和上一元组属于同一课程时，则部分属性的值不会显示，
而是存储在 td 元素的 `hidevalue` 属性中。

## 转换 ICalendar 格式

icalendar 格式的规范文档为 [RFC 5545](https://tools.ietf.org/html/rfc5545)

在 Python 的 icalendar 库中，定义了一系列 icalendar 组件，
在本项目中使用 Calendar 和 Event 两个。

Calendar 类初始化时可以不用参数，但之后必须设定以下属性:

```python
cal = Calendar()
# 符合 [ISO.9070.1991] 规范的发行者 ID，
# 规范要求全球唯一，但我们没有，所以随便用一个。
cal.add("prodid", "-//Zombie110year//CQU Class Table//")
# 目前 icalendar 规范是 2.0 版本
cal.add("version", "2.0")
```

Event 类同理，但需要注意日期格式

```python
ev = Event()
ev.add("summary", "总结性文本")
ev.add("location", "标注一个位置")
ev.add("description", "大多数日程管理软件把这个属性显示在标题位置")
ev.add("dtstart", "事件开始时间戳")
ev.add("dtend", "事件结束时间戳")
ev.add("rrule", {"freq": "dayly", "count": 14})
```

dtstart 和 dtend 就是时间的开始/结束时间。dt* 属性需要 UTC 格式时间戳，其形式类似于：

```
19970610T172345Z
```

用 strftime 格式字符串来表示的话就是

```
%Y%m%dT%H%M%SZ
```

末尾的 Z 表示采用 UTC 0 时区。

Event 可以设置重复规则 (Recurrence Rule)，可以设置多个键值对。

- FREQ，间隔单位，可选值有：
    - SECONDLY， 表示以秒为间隔单位进行重复。
    - MINUTELY， 表示以分钟为间隔单位进行重复。
    - HOURLY， 表示以小时为间隔单位进行重复。
    - DAILY， 表示以天为间隔单位进行重复。
    - WEEKLY， 表示以周为间隔单位进行重复。
    - MONTHLY， 表示以月为间隔单位进行重复。
    - YEARLY， 表示以年为间隔单位进行重复。
- INTERVAL，间隔量，以 FREQ 设定的单位为基础，默认值为 1。
- UNTIL，结束日期时间，用来限制重复次数。
- COUNT，重复次数的限制，如果 Event 既没有设置 COUNT， 也没有设置 UNTIL，那么将无限重复。

其他属性暂时不会用到，所以就不记录了。

对于 icalendar，此设置需要传入一个字典。

在得到 Event 实例后，可以调用 Calendar 的 `add_component` 方法将 Event 添加到 Calendar 中。

调用 Calendar 的 `to_ical` 方法，生成符合规范的 ics 文件内容（是 Python 中的 bytes 对象）。
