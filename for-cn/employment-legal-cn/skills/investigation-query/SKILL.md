---
name: investigation-query
description: >
  对一个打开的调查日志提问——证人说了什么、陈述在哪里冲突、存在什么缺口、
  每个问题上最强的证据是什么。触发场景：需要查询调查记录而不必重读每一条。
argument-hint: "[事项名] [问题]"
---

# /investigation-query

回答对调查日志的提问——证人说了什么、陈述在哪里冲突、存在什么缺口、每个问题上最强的证据是什么。

## 说明

1. 加载 `internal-investigation` 参考技能并跑模式 3（查询）。
2. 答案中总是引用日志条目 ID。
3. 若日志中无与问题相关的内容，明确说出来——「在这个调查日志中我没看到关于 [主题] 的任何信息（已审查 [N] 条）」——并提供把它标记为缺口。

## 示例

```
/employment-legal-cn:investigation-query [事项名]
被调查人关于十二月团队聚餐说了什么？
```

```
/employment-legal-cn:investigation-query [事项名]
举报人和被调查人的陈述在哪里冲突？
```

```
/employment-legal-cn:investigation-query [事项名]
我们还缺什么？
```

> 详细的日志查询流程、引用规则和缺口标记模板在 `internal-investigation` 参考技能里——做实质工作前先加载它。
