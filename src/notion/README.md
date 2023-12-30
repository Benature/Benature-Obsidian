# Notion2Obsidian

Notion Database 同步置顶顺序到 Obsidian 笔记中。

- 支持自定义 yaml 顺序

## 使用 

配置

<https://developers.notion.com/reference/intro>

```python
# config.py
from pathlib import Path

TOKEN = "secret_xxxxx"

DB_ID_BOOK = "xxxxx"

OB_ROOT_PATH = Path(
    "Documents/Obsidian"
)
```

运行

```shell
python books
```