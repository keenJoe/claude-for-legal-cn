# claude-for-legal-cn —— 中国法域插件集

`anthropics/claude-for-legal` 的**中国法定制版**。保留原版工作流架构（冷启动访谈 → 执业档案 → 审查 → 分级 → 护栏 → 交付），替换实体法层：民法典、劳动合同法、公司法（2023 修订）、个人信息保护法、数据安全法、网络安全法、商标法、专利法、著作权法、民事诉讼法，覆盖境内监管与数据出境合规路径。

## 安装

```bash
/plugin marketplace add <本仓库路径>/for-cn

# 安装需要的插件（以商务合同为例）
/plugin install commercial-legal-cn@claude-for-legal-cn

# 重启后运行冷启动访谈，生成执业档案
/commercial-legal-cn:cold-start-interview
```

## 转换方法

见 `references/conversion-spec.md`（法域映射总表 + 质量门槛）、`references/cold-start-protocol.md`（冷启动访谈共享协议）、`references/claude-md-template-spec.md`（执业档案模板规范）。

## 目录

```
for-cn/
  .claude-plugin/marketplace.json   # 市场清单（12 个插件）
  <插件名>-cn/                      # 每个插件的 CN 版
    .claude-plugin/plugin.json
    CLAUDE.md                       # 执业档案模板
    skills/<技能>/SKILL.md          # 技能（中文）
    agents/                         # 定时 agent（如有）
    hooks/hooks.json
    .gitignore
  references/                       # 转换规范、冷启动协议、档案模板规范
  scripts/                          # 校验脚本
```

## 校验

```bash
python3 scripts/validate-cn.py          # marketplace/plugin 合法性 + 英美法残留扫描
```

## 与原版的关系

- 原版「官方英文」插件目录保留在一级目录，供上游同步对照。
- 本目录所有文件为中文法域内容；改动只应影响本目录。
- 每次上游 `anthropics/claude-for-legal` 更新后：对照检查新技能 → 按 conversion-spec.md 转成 CN 版。
