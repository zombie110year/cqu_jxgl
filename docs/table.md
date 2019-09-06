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

注意时区设置。
