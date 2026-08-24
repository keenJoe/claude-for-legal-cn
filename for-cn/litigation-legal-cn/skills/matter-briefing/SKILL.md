---
name: matter-briefing
description: >
  就单个案件生成简报 —— 当前节点、近期变化、下一个期限、悬而未决问题、
  风险再评估提示，用于汇报前、外聘律师沟通前、董事会/管理层通报前的准备。
  触发场景：用户说「简报一下 [案件名]」「[案件名] 到哪一步了」「brief me on
  matter」，或需要一个案件的当前读数。
argument-hint: "[slug 案件短名]"
---

# /matter-briefing

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/CLAUDE.md` —— 获取风险分级标准和相关内部利益相关方。
2. 按下方工作流执行。
3. 读 `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/matters/[slug]/matter.md` + `history.md` + `_log.yaml` 中对应行。
4. 生成简报：当前节点、自上次更新以来的变化、下一个期限、悬而未决问题、风险再评估提示（"`risk:` 字段是否仍反映实际情况？"）。
5. 陈旧标记：若 `last_updated` 距今超过 30 天，顶部标 ⚠️ STALE。

---

# 案件简报

## 目的

让律师/法务在走去会议室的时间里，对一个案件形成干净的读数：现在在哪、变了什么、接下来是什么、需要重新想什么。

## 加载上下文

- `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/matters/_log.yaml` —— 结构化行
- `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/matters/[slug]/matter.md` —— 叙事性立案信息
- `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/matters/[slug]/history.md` —— 事件流水
- `~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/CLAUDE.md` —— 风险分级（让 "risk: 高" 有明确含义，不是泛化标签）

**利益冲突门槛 —— 不可绕过。** 简报前，检查 `_log.yaml` 是否有此 slug。若不在：

> "在案件台账中没找到 [slug]。先运行 `/litigation-legal-cn:matter-intake` —— 利益冲突检查是这一门槛，未做过立案检查的案件不允许生成简报。"

## 输入

slug（必需）。若歧义或缺失，让用户从活跃案件列表中选。

## 简报

```markdown
本文件由 AI 辅助生成，是待律师审核的工作草稿，不构成法律意见。
审查人：[姓名]  日期：[今日]  已读范围：[matter.md v[N] + history.md 近 [N] 条 + _log.yaml 行]

# [案件名] —— 截至 [今日] 的简报

**状态：** [立案 / 一审举证 / 一审审理 / 一审判决 / 上诉 / 二审 / 再审 / 执行]
**风险：** [高/中/低] ([严重程度] × [可能性])
**重要性：** [提准备金 / 需披露 / 监控 / 无需特别处理]
**外聘律师：** [律所 —— 主办律师]
**最后更新：** [日期] [若 >30 天标 ⚠️ 陈旧]
**利益冲突：** [已清理 / 待办 → ⚠️ / 未做 → ⚠️]

---

## 一段话概述

[当前节点。我们在做什么、为什么。若已捕捉「关键事实」也点出来。]

## 近期变化

[history.md 近 3-5 条，最新在上。若历史稀薄就说明。]

## 下一步

- **紧邻期限：** [下一个 next_deadline + 是什么。举证期限？开庭？上诉期？]
- **临近里程碑：** [matter.md 或近期 history 中带日期的]
- **待决问题：** [matter.md 中标注的 open questions]

## 风险敞口

[金额区间 + 自立案以来的变化。若已提准备金，当前准备金金额 + 是否需要重新校准。]

## 内部相关方

[谁被拉入圈内；是否有该拉入但没拉入的（如 CFO 需评估准备金但未通知）]

## 风险再评估提示

*是提示，不是答案。*

- `risk: [现值]` 是否仍然合理？案件是否已经移动？
- `materiality: [现值]` 是否仍匹配？新事实可能推动准备金/披露判断。
- 是否需要新的相关方？（例如证据发现涉及数据出境 → CISO/数据合规负责人）

## 悬而未决问题

[从 matter.md 和 history 中提取的未解决项]

## 谈话准备

[若用户指定了目的 —— "和外聘律师沟通前简报" —— 定制此节：要问的问题、要拿到的决定、要提取的更新。若未指定，省略此节。]
```

## 陈旧

若 `last_updated > 30 天前`：顶部标注，并建议会后运行 `/litigation-legal-cn:matter-update [slug]` 更新。

## 语气

不是营销文案。已知的说，未知的标。案件刚立案历史稀薄的，简报就短 —— 这是对的，别硬凑。

## 收尾：下一步决策树

按 CLAUDE.md `## 输出` 结尾的决策树收尾。默认五个分支（起草某某、升级上报、补事实、观望、其他）是起点不是锁定，按本次输出定制。

## 转换决策

- 分级：**B 大改**。原版功能保留（案件读数视图）。实体层改动：`stage` 术语按中国审级替换（立案/一审举证/一审审理/一审判决/上诉/二审/再审/执行），"reserve/disclosed" 保留（对应中国财报的诉讼预计负债披露与准备金）；FRCP/Rule 术语删除，改为民诉法阶段。

## 这个 skill 不做的事

- 预测胜败。风险评级是已捕捉的判断，不是预测。
- 推荐策略。抛出问题，律师作答。
- 重新分级。用户想重新分级 → 那是 `/matter-update` 带字段变更 —— 本 skill 只读不写。
