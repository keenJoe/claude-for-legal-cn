---
name: investigation-memo
description: >
  从调查日志起草或更新保密调查备忘录。触发场景：调查进展到可以写第一版备忘录，
  或有新数据加入、现有草稿需要更新。
argument-hint: "[事项名]"
---

# /investigation-memo

从日志起草保密调查备忘录的第一版，或在有新数据加入时更新现有草稿。

## 说明

1. 加载 `internal-investigation` 参考技能并跑模式 4（起草或更新备忘录）。
2. 若首次起草，若高优先级来源在清单上仍打开着，警告。
3. 若是更新，重写前展示什么变了。
4. 所有输出标注为保密工作成果头部（按用户角色——见执业档案 `## 输出`）。

## 示例

```
/employment-legal-cn:investigation-memo [事项名]
```

```
/employment-legal-cn:investigation-memo [事项名]
（若已存在备忘录则更新）
```

> 详细的备忘录结构、可信度评估框架和更新规则在 `internal-investigation` 参考技能里——做实质工作前先加载它。
