# 登录过程

获取 Cookie 的过程很重要.

## 加载主页

首先, 以原始状态用 **GET** 方法访问 `http://jxgl.cqu.edu.cn/home.aspx`, 将会得到 text/html 响应:

```html
<html><head><script>
function load_url()
{
document.cookie='DSafeId=B5B27C19B5B29DBEEEE7364F;';
self.location='/home.aspx';
}
setTimeout("load_url()",680);
</script>
</head><body></body></html>
```

cookie 值是时刻变化的.

使用以下脚本模拟此行为:

```python
import requests as r
from time import sleep
import re

def getHomePage():
    url = "http://jxgl.cqu.edu.cn/home.aspx"
    pattern = "(?<=document.cookie=')(DSafeId=[A-Z0-9]+;)(?=';)"
    headers = {
        'host': "jxgl.cqu.edu.cn",
        'connection': "keep-alive",
        'cache-control': "max-age=0",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'referer': "http://jxgl.cqu.edu.cn/MAINFRM.aspx",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9"
        }
    resp = r.get(url, headers=headers)
    cookie = re.search(pattern, resp.text).group(1)
    headers["cookie"] = cookie
    sleep(680)
    resp = r.get(url, headers=headers)
    return resp.headers["set-cookie"]

print(getHomePage())
```

成功得到了首页的正确响应, 并得到了 Cookie

```
ASP.NET_SessionId=jtajn3r1zjlt1b2p3rvkpz55; path=/, _D_SID=B5B29DBE0E7F60E6EC6434A7D712E509; path=/;HttpOnly
```

## 登录表单

**POST** 登录表单，此表单有 10 个键值对：

键|含义
:-:|-
`__VIEWSTATE`|`//*[@id="Logon"]/input[1]`
`__VIEWSTATEGENERATOR`|`//*[@id="Logon"]/input[2]`
`Sel_Type`|登录者身份，`STU` 代表学生
`txt_dsdsdsdjkjkjc`|学号
`txt_dsdfdfgfouyy`|原始密码，但最终它的值将被清空，而加密的密码将会存储在 `efdfdfuuyyuuckjg` 键中
`txt_ysdsdsdskgf`|空字符串
`pcInfo`|空字符串
`typeName`|空字符串
`aerererdsdxcxdfgfg`|空字符串
`efdfdfuuyyuuckjg`|`//*[@id="efdfdfuuyyuuckjg"]`, 其值由密码计算而来, 计算方法为

```javascript
schoolcode = "10611";
md5(学号 + md5(密码).substring(0, 30).toUpperCase() + schoolcode).substirng(0, 30).toUpperCase();
```

其中的 md5 函数可用 Python Hashlib 中的 MD5 函数如此代替:

```python
from hashlib import md5 as rawmd5

def md5(string):
    return rawmd5(string.encode()).hexdigest().upper()
```

可以用以下脚本模拟密码的检验:

```python
from hashlib import md5 as rawmd5
def md5(string) -> str:
    return rawmd5(string.encode()).hexdigest().upper()

def chkpwd(username, password) -> "赋值给: efdfdfuuyyuuckjg":
    schoolcode = "10611"
    return md5(username + md5(password)[0:30].upper() + schoolcode)[0:30].upper()
```

---

以下是 http://jxgl.cqu.edu.cn/_data/index_login.aspx 中定义的密码/验证码检查函数:

```javascript
/**
 * Check Password
 *
 * @param {obj} 输入密码的 input 元素
 */
function chkpwd(obj) {
    var schoolcode = "10611";
    var yhm = document.all.txt_dsdsdsdjkjkjc.value;
    if (obj.value != "") {
        if (document.all.Sel_Type.value == "ADM")
            yhm = yhm.toUpperCase();
        var s = md5(yhm + md5(obj.value).substring(0, 30).toUpperCase() + schoolcode).substring(0, 30).toUpperCase();
        document.all.efdfdfuuyyuuckjg.value = s;
    } else {
        document.all.efdfdfuuyyuuckjg.value = obj.value;
    }
}
/**
 * Check Yan Zheng Ma | 检查验证码
 *
 * @param {obj} 输入验证码的 input 元素
 */
function chkyzm(obj) {
    var schoolcode = "10611";
    if (obj.value != "") {
        var s = md5(md5(obj.value.toUpperCase()).substring(0, 30).toUpperCase() + schoolcode).substring(0, 30).toUpperCase();
        document.all.aerererdsdxcxdfgfg.value = s;
    }
    else {
        document.all.aerererdsdxcxdfgfg.value = obj.value;
    }
}
```

之后就算成功登录了， Cookie 可以用很久。
