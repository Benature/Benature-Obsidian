import requests
from bs4 import BeautifulSoup as bs
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import re

from markdown import MarkdownMetadataHandler

filename_change_dict = {
    r'\s*[\|\/]\s*': '丨',
    'Vol': '',
    ':': ' ',
}

podcaster_change_dict = {
    "What's Next｜科技早知道": "科技早知道",
}

root_path = Path(__file__).parent.parent.parent
dir_rel_path = '输入/podcast'
dir_path = root_path / dir_rel_path


class Podcast():

    def __init__(self, url):
        self.url = url

    def extract(self):
        url = self.url
        session = requests.session()

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

        publish_time = datetime.strptime(
            info_div.select("time")[0]['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        publish_time = datetime.strftime(publish_time, "%Y-%m-%d %H:%M:%S")

        series_num = re.findall(r"(?:Vol|No|\#)\.?\s*(\d+)",
                                title,
                                flags=re.IGNORECASE)
        if series_num:
            series_num = series_num[0].strip()
        else:
            series_num = ""

        md_fn = title  # markdown filename
        md_fn = re.sub(r"(?:Vol|No|\#)\.?\s*\d+\s*",
                       "",
                       md_fn,
                       flags=re.IGNORECASE)
        for old, new in filename_change_dict.items():
            md_fn = re.sub(old, new, md_fn)
        md_fn = md_fn.lstrip('# ').strip(' .')
        self.md_fn = md_fn

        for old, new in podcaster_change_dict.items():
            podcaster = podcaster.replace(old, new)
        podcaster = podcaster.replace(' ', '').replace("'", "")

        if 'xiaoyuzhoufm' in url:
            url = url.split('?')[0]

        parsed_url = urlparse(url)

        self.content = f'''---
title: "{title}"
url: {parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path}
podcaster: {podcaster} 
duration: {duration}
publishTime: {publish_time}
seriesNum: {series_num}
---

'''

    def export(self):
        file_path = dir_path / f"{self.md_fn}.md"
        # file_path = dir_path / f"{md_fn} - {podcaster.strip()}.md"

        print(file_path)
        if False and not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(content)
        else:
            print(f"{self.md_fn} exists")
            import richxerox
            richxerox.copy(text=self.content)


if __name__ == '__main__':
    if sys.argv[1] == 'BATCH':
        from subprocess import Popen
        url_scheme_pre = "obsidian://open?vault=Obsidian&file="
        for md_path in dir_path.glob("*.md"):
            url_scheme = f"{url_scheme_pre}{dir_rel_path}/{md_path.stem}.md"
            print(md_path)
            with open(md_path, "r") as f:
                content = f.read()
            if "#podcaster" not in content:
                continue
            Popen(["open", url_scheme])
            print(md_path)
            xyz_url = re.findall(
                r"(https://www.xiaoyuzhoufm.com/episodes?/.*?)(?:\s|\)|$)",
                content)
            xyz_url = xyz_url[0]
            print(xyz_url)
            mmh = MarkdownMetadataHandler(md_path)
            meta = mmh.extract_metadata()
            if len(meta) > 0:
                input("has metadata")
                continue
            pc = Podcast(xyz_url)
            pc.extract()
            # meta_str = pc.content
            # input("stop")
            with open(md_path, "w") as f:
                f.write(pc.content + content)
            print()
            input("check")
    else:
        url = sys.argv[1]
        pc = Podcast(url)
        pc.extract()
        pc.export()
