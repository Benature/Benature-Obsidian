import requests
from config import *

import re
import yaml
from pathlib import Path
from collections import OrderedDict


class MarkdownMetadataHandler:

    def __init__(self, md_file_path, prekeys=None):
        self.md_file_path = Path(md_file_path)
        self.metadata_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n',
                                           re.MULTILINE | re.DOTALL)
        self.prekeys = [] if prekeys is None else prekeys

    def extract_metadata(self):
        with self.md_file_path.open('r', encoding='utf-8') as file:
            content = file.read()
            match = self.metadata_pattern.search(content)
            if match:
                metadata_str = match.group(1)
                return yaml.safe_load(metadata_str)
            else:
                return {}

    def sort_metadata(self, metadata):
        """Force some keys in custom order"""
        ordered_metadata = OrderedDict()
        for key in self.prekeys:
            if key in metadata:
                ordered_metadata[key] = metadata[key]
        for key, value in metadata.items():
            if key in ordered_metadata:
                continue
            ordered_metadata[key] = value
        return ordered_metadata

    def generate_metadata(self, new_metadata):
        """
        yaml.dump() 对缩进支持有问题，且对于文本没有使用引号包围（双括号`[[文本]]`需要）。
        因此造轮子
        """
        updated_metadata_str = "---\n"
        ordered_metadata = self.sort_metadata(new_metadata)
        for key, value in ordered_metadata.items():
            if isinstance(value, list):
                updated_metadata_str += f"{key}:\n"
                for item in value:
                    if isinstance(item, str) and '[' in item and ']' in item:
                        updated_metadata_str += f"  - \"{item}\"\n"
                    else:
                        updated_metadata_str += f"  - {item}\n"
            elif isinstance(value, str):
                value = "" if value == 'None' else value
                updated_metadata_str += f'{key}: "{value}"\n'
            else:
                updated_metadata_str += f'{key}: {value or ""}\n'
        updated_metadata_str += "---\n"
        return updated_metadata_str

    def update_metadata(self, new_metadata):
        with self.md_file_path.open('r', encoding='utf-8') as file:
            content = file.read()
        metadata_match = self.metadata_pattern.search(content)
        if metadata_match is None:
            return
        m_start = metadata_match.start()
        m_end = metadata_match.end()

        metadata_str = self.generate_metadata(new_metadata)

        content = content[:m_start] + metadata_str + content[m_end:]
        with self.md_file_path.open('w', encoding='utf-8') as file:
            file.write(content)


response = requests.request(
    "POST",
    f"https://api.notion.com/v1/databases/{DB_ID_BOOK}/query",
    headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    },
    json={"filter": {
        "property": "读/听完",
        "checkbox": {
            "equals": True
        }
    }})

prekeys = [
    "done", "beginDate", "finishDate", "tags", "author", "title", "subTitle",
    "category", "publisher", "publishTime"
]

for page in response.json()['results']:
    props = page['properties']
    dates = props['阅读时间']['date']
    title = props['书名']['title'][0]['plain_text']
    done = props['读/听完']['checkbox']
    tags = [s['name'] for s in props['Tags']['multi_select']]

    print(title, dates, done, tags)

    md_path = OB_ROOT_PATH / f"输入/书籍/《{title}》.md"
    if not md_path.exists():
        print("not exists")
        continue
    input()
    handler = MarkdownMetadataHandler(md_path, prekeys=prekeys)
    meta = handler.extract_metadata()
    if dates is not None:
        if dates['end'] is not None:
            meta['finishDate'] = dates['end']
            meta['beginDate'] = dates['start']
        else:
            meta['finishDate'] = dates['start']
    meta['done'] = done
    if isinstance(meta['tags'], str):
        meta['tags'] = [meta['tags']]
    for t in tags:
        if t in meta['tags']: continue
        t_p = Path(t).parent
        while str(t_p) != '.':
            if str(t_p) in meta['tags']: meta['tags'].remove(str(t_p))
            t_p = t_p.parent
        meta['tags'].append(t)
    handler.update_metadata(meta)
