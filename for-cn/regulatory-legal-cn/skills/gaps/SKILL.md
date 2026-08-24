---
name: gaps
description: >
  合规缺口追踪器 —— 列出已发现但尚未关闭的合规缺口。触发场景：用户说
  「有哪些未闭环的缺口」「缺口清单」「合规整改状态」「哪些缺口已经关闭了」，
  或需要关闭（--close GAP-ID）/风险接受（--accept GAP-ID）某条缺口。
argument-hint: "[可选：--close GAP-ID | --accept GAP-ID]"
---

# /gaps

1. 读取缺口追踪文件 `~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/gap-tracker.yaml`。
2. 若参数为 `--close`：将该缺口置为已关闭，记录整改结论。
3. 若参数为 `--accept`：记录风险接受理由与决定人，状态置为「风险接受」。
4. 否则：按年龄和严重程度输出未闭环缺口清单。

> 追踪表结构、状态报告格式、责任人通知逻辑（发送前必须逐条确认，无例外）、
> 提醒节奏、关闭 / 风险接受模式、以及涉及合规确认的动作前置门槛，
> 全部在 **gap-surfacer** 参考技能中定义 —— 执行实质工作前先加载它。
