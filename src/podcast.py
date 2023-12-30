import requests
from bs4 import BeautifulSoup as bs
import os
import sys

filename_change_dict = {
    '/': '丨',
    ' | ': '丨',
    '|': '丨',
    'Vol': '',
    ':': ' ',
}

podcaster_change_dict ={
    "What's Next｜科技早知道": "科技早知道",
}

session = requests.session()

url = sys.argv[1]
dirpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '输入/podcast')

response = session.get(url)
soup = bs(response.text, 'lxml')

title = soup.select('.title')[1].text
for old, new in filename_change_dict.items():
    title = title.replace(old, new)
title = title.lstrip('# ').strip(' .')

podcaster = soup.select('.name')[0].text.strip()
for old, new in podcaster_change_dict.items():
    podcaster = podcaster.replace(old, new)
podcaster = podcaster.replace(' ', '').replace("'", "")

filename = os.path.join(dirpath, title + ".md")

if 'xiaoyuzhoufm' in url:
    url = url.split('?')[0]
content = f'''### [{title}]({url})
#podcaster/{podcaster} 

---

'''

if not os.path.isfile(filename):
    with open(filename, 'w') as f:
        f.write(content)
