---
name: expansion-kickoff
description: >
  为一个新国家/地区启动人员跨境安排规划——收集受理信息、跑 EOR vs. 设立主体框架、
  起草跨职能问题、浮现该国特定标志、创建持续追踪器。触发场景：用户说
  「我们要在[国家]招人」「扩张到[国家]」「在[国家]的第一次招聘」。
argument-hint: "[国家/地区名]"
---

# /expansion-kickoff

为一个新国家启动人员跨境安排项目——收集受理信息、跑 EOR vs. 设立主体框架、起草跨职能问题、浮现该国特定标志、创建持续追踪器。

## 说明

1. 加载 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md` → 用工地域足迹、升级表。
2. 加载 `international-expansion` 参考技能并跑完整工作流。
3. 若该国已存在追踪器文件（`~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/expansion-[slug].yaml`），标记：「[国家]的扩张追踪器已存在。用 `/employment-legal-cn:expansion-update [国家]` 更新它，或确认你要重新开始。」
4. 完成时创建 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/expansion-[slug].yaml`。

## 示例

```
/employment-legal-cn:expansion-kickoff 新加坡
```

```
/employment-legal-cn:expansion-kickoff
（技能会问是哪个国家）
```

> 详细的 EOR vs. 设立主体框架、跨职能问题、简报模板和追踪器结构在 `international-expansion` 参考技能里——做实质工作前先加载它。
