---
name: investigation-add
description: >
  向一个打开的调查添加数据——文档、谈话记录或观察。按记录的调取标准批量处理，
  浮现重要项，并记录所有已审查内容以便覆盖核验。触发场景：新证据、谈话记录或
  文档材料为一个打开的调查进来。
argument-hint: "[事项名或 slug，然后粘贴或附上数据]"
---

# /investigation-add

向一个打开的调查日志添加数据。用记录的调取标准处理文档批次，浮现重要项，记录所有已审查内容以便覆盖核验。

## 说明

1. 加载 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md`。
2. 加载 `internal-investigation` 参考技能并跑模式 2（添加数据）。
3. 处理后，展示浮现比率和浮现项清单。
4. 若数据覆盖了清单中的某来源项，提示更新来源清单。

## 示例

```
/employment-legal-cn:investigation-add [事项名]
[粘贴谈话记录]
```

```
/employment-legal-cn:investigation-add [事项名]
[附上邮件导出]
```

> 详细的关键信息识别流程、日志条目格式、浮现比率规则和来源清单追踪在 `internal-investigation` 参考技能里——做实质工作前先加载它。
