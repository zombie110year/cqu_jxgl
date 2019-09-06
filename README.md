这是为重庆大学教学管理网站编写的 Python 工具，支持以下功能：

- [x] 将课程表导出为 ics 文件

```python
# 例子
from cqu_jxgl.app import App
from cqu_jxgl.data.time import 沙坪坝校区作息时间
from datetime import datetime

app = App("********", "********")
app.writeICS(20190, datetime(2019,9,2), 沙坪坝校区作息时间)
```

- [ ] 查询选课信息
- [ ] 提交选课表单
