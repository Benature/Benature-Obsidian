import requests
from bs4 import BeautifulSoup as bs
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

filename_change_dict = {
    '/': '丨',
    # ' | ': '丨',
    # '|': '丨',
    'Vol': '',
    ':': ' ',
}

podcaster_change_dict = {
    "What's Next｜科技早知道": "科技早知道",
}

session = requests.session()

url = sys.argv[1]
root_path = Path(__file__).parent.parent
dir_path = root_path / '输入/podcast'
# dirpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '输入/podcast')

response = session.get(url)
soup = bs(response.text, 'lxml')

# extract information
title = soup.select('.title')[1].text
podcaster = soup.select('.name')[0].text.strip()
info_div = soup.select('.info')[0]

duration = ""
for c in info_div.contents:
    if c.strip():
        duration = c
        break
# duration = duration.replace("分钟", "").strip()

publish_time = datetime.strptime(
    info_div.select("time")[0]['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
publish_time = datetime.strftime(publish_time, "%Y-%m-%d %H:%M:%S")

md_fn = title  # markdown filename
for old, new in filename_change_dict.items():
    md_fn = md_fn.replace(old, new)
md_fn = md_fn.lstrip('# ').strip(' .')

for old, new in podcaster_change_dict.items():
    podcaster = podcaster.replace(old, new)
podcaster = podcaster.replace(' ', '').replace("'", "")

file_path = dir_path / f"{md_fn}.md"
file_path = dir_path / f"{md_fn} - {podcaster.strip()}.md"

if 'xiaoyuzhoufm' in url:
    url = url.split('?')[0]

parsed_url = urlparse(url)

content = f'''---
title: "{title}"
url: {parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path}
podcaster: {podcaster} 
duration: {duration}
publishTime: {publish_time}
---

'''

print(file_path)
if not file_path.exists():
    with open(file_path, 'w') as f:
        f.write(content)
else:
    print(f"{md_fn} exists")
    import richxerox
    richxerox.copy(text=content)
