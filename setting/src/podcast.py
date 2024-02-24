import requests
from bs4 import BeautifulSoup as bs
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import re
import icecream as ic

from markdown import MarkdownMetadataHandler
from notify import notify

filename_change_dict = {
    r'\s*[\|\/]\s*': '丨',
    'Vol': '',
    ':': ' ',
}

podcaster_change_dict = {
    "What's Next｜科技早知道": "科技早知道",
    "松茸的世界丨正念冥想": "松茸的世界",
}
podcaster_short_title_dict = {
    "随机波动StochasticVolatility": "随机波动",
    "BlowYourMind(BYMS02)": "BYM",
    "英美剧漫游指南KillingTV": "英美剧漫游指南",
    "翻转台电（翻电）": "翻电",
}

root_path = Path(__file__).parents[2]
dir_rel_path = '输入/podcast'
dir_path = root_path / dir_rel_path
print(root_path)


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
            series_num = re.findall(r"\d+(?!\s?分钟)", title)
            if len(series_num) == 1:
                series_num = int(series_num[0])
            else:
                series_num = ""

        md_fn = title  # markdown filename
        md_fn = re.sub(r"(?:Vol|No|\#)\.?\s*\d+\s*",
                       "",
                       md_fn,
                       flags=re.IGNORECASE)
        for old, new in filename_change_dict.items():
            md_fn = re.sub(old, new, md_fn)
        md_fn = md_fn.lstrip('# :：').strip(' .')
        self.md_fn = md_fn

        for old, new in podcaster_change_dict.items():
            podcaster = podcaster.replace(old, new)
        podcaster = podcaster.replace(' ', '').replace("'", "").strip()

        if 'xiaoyuzhoufm' in url:
            url = url.split('?')[0]

        parsed_url = urlparse(url)

        self.meta = dict(title=title,
                         url=parsed_url.scheme + "://" + parsed_url.netloc +
                         parsed_url.path,
                         podcaster=podcaster,
                         duration=duration,
                         publishTime=publish_time,
                         seriesNum=series_num)

        self.content = f'''---
title: "{title}"
url: {parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path}
podcaster: "[[{podcaster}]]"
duration: {duration}
publishTime: {publish_time}
seriesNum: {series_num}
---


````dataviewjs
const {{Podcast}} = customJS
Podcast.episode_display(dv)
````
'''

    def export(self):
        filename = f'{self.md_fn} - {podcaster_short_title_dict.get(self.meta["podcaster"], self.meta["podcaster"])}.md'

        # file_path = dir_path / f"{self.md_fn}.md"
        podcaster_dir_path = (dir_path / self.meta["podcaster"])
        if podcaster_dir_path.exists():
            file_path = podcaster_dir_path / filename
        else:
            file_path = dir_path / filename

        print(file_path)
        if not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(self.content)
        else:
            print(f"{self.md_fn} exists")
            import richxerox
            richxerox.copy(text=self.content)
        notify(filename, "Podcast")


if __name__ == '__main__':
    if sys.argv[1] == 'BATCH':
        import os
        from subprocess import Popen
        url_scheme_pre = "obsidian://open?vault=Obsidian&file="
        for md_path in dir_path.glob("*.md"):
            url_scheme = f"{url_scheme_pre}{dir_rel_path}/{md_path.stem}.md"
            print(md_path)
            # with open(md_path, "r") as f:
            #     content = f.read()
            # if "#podcaster" not in content:
            #     continue
            # Popen(["open", url_scheme])
            # print(md_path)
            # xyz_url = re.findall(
            #     r"(https://www.xiaoyuzhoufm.com/episodes?/.*?)(?:\s|\)|$)",
            #     content)
            # xyz_url = xyz_url[0]
            # print(xyz_url)
            mmh = MarkdownMetadataHandler(md_path)
            meta = mmh.extract_metadata()
            if len(meta) == 0:
                print("has no metadata")
                continue
            if "url" not in meta:
                print("no url")
                continue

            pc = Podcast(meta["url"])
            try:
                pc.extract()
            except:
                continue
            ic.ic(pc.md_fn)
            filename = f'{pc.md_fn} - {podcaster_short_title_dict.get(pc.meta["podcaster"], pc.meta["podcaster"])}.md'

            ic.ic(filename)
            podcaster_dir_path = (dir_path / pc.meta["podcaster"])
            if podcaster_dir_path.exists():
                file_path = podcaster_dir_path / filename
            else:
                file_path = dir_path / filename
            ic.ic(file_path.relative_to(dir_path))
            md_path.replace(file_path)
            # os.rename(md_path, file_path)
            # # meta_str = pc.content
            # # input("stop")
            # with open(md_path, "w") as f:
            #     f.write(pc.content + content)
            # print()
            input("check")
            # break
    else:
        url = sys.argv[1]
        pc = Podcast(url)
        pc.extract()
        pc.export()
