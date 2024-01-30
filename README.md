# Benature-Obsidian

相关文章介绍：
- Obsidian 跨越研究生生涯的 4 年年度回顾  
[微信公众号](https://mp.weixin.qq.com/s/PwEO8uJMV1kIOcETG82EVQ) / [少数派](https://sspai.com/post/85339) / [知乎](https://zhuanlan.zhihu.com/p/678256692) / [notion](https://benature.notion.site/Obsidian-4-fb430726a5cd4ebc8bb2e829e85f4923)
- ~~视频分享正在路上 🐦~~

模板库: https://github.com/Benature/obsidian-sample-vault

## 仓库结构

- `.obsidian/snippets`: css
- `setting`
  - `js`: js code for plugins CustomJS + Dataview
  - templates
- `src`: some codes to generate note from network
  - `podcast.py`: 小宇宙播客
  - [`notion`](./src/notion/): Notion 同步

## 配置

### Citations

<obsidian://show-plugin?id=obsidian-citation-plugin>

```md
---
alias: {{titleShort}}
tags: 
year: {{year}}
title: "{{title}}"
container: "{{containerTitle}}"
url: {{#if URL}}{{URL}}{{else}}{{#if DOI}}https://doi.org/{{DOI}}{{/if}}{{/if}}
---
- [ ] 《{{title}}》[🆉]({{zoteroSelectURI}}) ^read

authors:: {{#each entry.author}} [[{{given}} {{family}}]],{{/each}}
related:: 
affiliation:: 

---

- abbr.

#### comment

## 0 Abstract

## 1 Intro
```

## 支持
![support.png](https://s2.loli.net/2024/01/30/jQ9fTSyBxvXRoOM.png)