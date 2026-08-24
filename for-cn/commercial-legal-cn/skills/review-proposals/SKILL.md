---
name: review-proposals
description: >
  审阅并批准（或否决）来自 playbook-monitor agent 的待定 playbook 更新提案，
  把批准的改动写入执业档案。触发场景：playbook-monitor agent 已标出提案时；
  用户说「看看 playbook 提案」「有哪些 playbook 更新在等审阅」，或想按偏差驱动的
  playbook 变更逐条走。
argument-hint: "[无参数 —— 从待定提案文件运行]"
---

# /review-proposals

逐条走一遍来自监控 agent 的待定 playbook 更新提案，把批准的改动写入 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md`。

## 说明

1. **加载 playbook-monitor agent** 并跑第 5 步（审阅与审批流）。

2. **若不存在提案文件或为空：** 回复*「无待定提案。Playbook 已是最新。」* 不再进行。

3. **一次一条提案。** 每条展示完整提案块，提供四个选项：接受、否决、编辑、延后。

4. **接受或编辑时：** 写入前先展示对 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md` 的精确差异。仅在律师明确确认后应用。

5. **否决或延后时：** 记录决定，不修改档案。

6. **全部提案处理完后：** 展示改了什么的摘要，然后归档提案文件。

## 示例

```
/commercial-legal-cn:review-proposals
```

```
/commercial-legal-cn:review-proposals
（在 playbook-monitor 通知后自动运行）
```

## 质量自检（本技能转换说明）

- **A 级直转：** 六步流程（加载 agent → 空文件回复 → 逐条展示四选项 → 差异预览 → 记录否决/延后 → 摘要归档）—— 方法论层原样保留。
- **B 级大改：** 无 —— 提案审阅逻辑不涉及实体法差异。
- **C 级删除：** 配置路径换为 claude-for-legal-cn。
- **D 级新增：** 无。
