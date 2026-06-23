<a href="https://flomoapp.com/"><img src="https://raw.githubusercontent.com/Benature/flomo/main/flomo/media/logo-192x192.png" height="100" align="right"></a>

# flomo 浮墨

[![PyPI](https://img.shields.io/pypi/v/flomo)](https://pypi.org/project/flomo/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flomo)
[![GitHub stars](https://img.shields.io/github/stars/Benature/flomo)](https://github.com/Benature/flomo)

一个非官方的 API python 玩具盒 👀

> *prefer python3.7+*  
> 欢迎 Star 🌟、Fork 🍴、Issue 💬、PR. 一起让 flomo 用的更加得心应手

最新版在 dev 分支

This fork adds full **CRUD** support — create, update, and delete memos — on top of the original read-only API.

## Usage 使用

```shell
pip install -U flomo
```

### Python 封装

```python
from flomo import Flomo, Parser

authorization = "Bearer xxxxxxxxxxx"
flomo = Flomo(authorization)

# Read
memos = flomo.get_all_memos()
memo = Parser(memos[-1])
print(memo.text) # memo 纯文本
print(memo.url)  # memo 链接
print(memo.tags)

# Create
new_memo = flomo.create("今天学到了一些新东西 #study")

# Update
flomo.update(new_memo["slug"], "修改后的内容 #study")

# Delete
flomo.delete(new_memo["slug"])
```

或参考 `main_simple.py` (by [MarkShawn2020](https://github.com/MarkShawn2020))

`authorization` 是用户 flomo 登录后获取的 token，可在浏览器的开发者工具中查看。

### CLI 命令行

```shell
# 配置token
flomo config --token 'your_token'

# 列出前5条备忘录，表格格式
flomo list -l 5 -f table

# 搜索包含关键词的备忘录
flomo search "知识管理" -f markdown

# 创建备忘录
flomo create "今天学到了一些新东西 #study"

# 更新备忘录（需要slug）
flomo update <slug> "修改后的内容 #study"

# 删除备忘录（需要slug）
flomo delete <slug>
```

> **Tip:** slug 可以从 `flomo list -f json` 的输出中获取。

credit to [MarkShawn2020](https://github.com/MarkShawn2020)

## Local Install 本地安装

```shell
git clone https://github.com/pauloil/flomo.git
cd flomo
pip install -e .
```


## Relative Project 相关项目

- upstream: [Benature/flomo](https://github.com/Benature/flomo)
- workflow: [Benature/flomo workflow](https://github.com/Benature/flomo-workflow)
- npm: [geekdada/flomo api helper](https://github.com/geekdada/flomo-api-helper)
