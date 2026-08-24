---
name: investigation-open
description: >
  开启一个新的内部调查事项——跑受理、生成来源清单、创建持续的调查日志。
  触发场景：投诉或指控进来，需要建立一个保密的调查工作区。
argument-hint: "[指控的简要描述]"
---

# /investigation-open

开启一个新的调查事项——跑受理、生成来源清单、创建持续的调查日志。

## 说明

1. 加载 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md`。
2. 加载 `internal-investigation` 参考技能并跑模式 1（开新事项）。
3. 若同 slug 的事项已存在，覆盖前警告。

## 示例

```
/employment-legal-cn:investigation-open
针对上海办公室一位经理的性骚扰投诉。
```

```
/employment-legal-cn:investigation-open
（技能会问细节）
```

> 详细的受理、保密形成要求、来源清单和日志模板在 `internal-investigation` 参考技能里——做实质工作前先加载它。
