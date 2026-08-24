---
name: expansion-update
description: >
  更新一个进行中的人员跨境安排项目的状态——重新计算现在解锁了什么、标记逾期项、
  浮现下一步优先级。触发场景：上次会话以来有进展，扩张追踪器需要反映当前状态。
argument-hint: "[国家/地区名]"
---

# /expansion-update

回到一个打开的扩张追踪器，根据上次会话以来发生的事更新事项状态。重新计算现在解锁了什么、标记逾期项、浮现下一步优先级。

## 说明

1. 加载 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md`。

2. 识别追踪器文件：`~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/expansion-[slug].yaml`。若不存在，回应：「未找到[国家]的扩张追踪器。运行 `/employment-legal-cn:expansion-kickoff [国家]` 来开始一个。」

3. 读追踪器。展示当前状态：

```
[国家] 扩张 — 最后更新 [日期]
待办：[N] | 进行中：[N] | 完成：[N] | 受阻：[N]

下一步优先级（最早到期或依赖度最高的待办项）：
  [事项] — 负责人：[负责人]
  [事项] — 负责人：[负责人]
```

4. 以单个提示询问更新——不要逐项询问：

   > 上次以来哪些事项有变动？告诉我什么变了（例如「EOR 决定了——用 Deel」「外部律师已聘——周四通话」「PE 分析还开着，等税务」）。你也可以加新事项或改到期日。

5. 应用更新到追踪器文件。对任何新标为 `done` 的事项，检查它是否解锁其他事项并标记为现在可行动。

6. 若任何事项到期日已过且仍为 `open` 或 `in-progress`，标记：

```
⚠️ 逾期：[事项] — 原定 [日期]，负责人：[负责人]
```

7. 写更新后的追踪器。确认：

```
追踪器已更新 — [N] 项关闭，[N] 项仍开着。
下一步优先：[最靠前的待办项]。
```

## 示例

```
/employment-legal-cn:expansion-update 新加坡
```

```
/employment-legal-cn:expansion-update
（若有多个追踪器会问是哪个国家）
```

> 详细的追踪器结构、事项状态规则和依赖逻辑在 `international-expansion` 参考技能里——做实质工作前先加载它。
