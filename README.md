# Benature-Obsidian

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