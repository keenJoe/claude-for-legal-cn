---
name: log-leave
description: >
  向休假台账添加一条新休假记录，含开始追踪期限所需的最少信息。触发场景：
  员工进入休假状态（医疗期、工伤停工留薪期、产假、哺乳期等），希望跟踪器
  从第一天就盯期限。
argument-hint: "[描述休假——员工/角色、假别、用工地、开始日]"
---

# /log-leave

向 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/leave-register.yaml` 添加一条新休假记录，含开始追踪期限所需的最少信息。触发场景：员工进入休假状态，希望跟踪器从第一天就盯期限。

## 说明

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md` → 用工地表和系统章节。

2. 以单个提示询问以下全部——不要逐条问：

   > 几个快速问题设置休假跟踪：
   >
   > - 员工姓名或角色（匿名化也可）
   > - 用工在哪个省市？（决定适用哪些地方规则——产假天数等）
   > - 假别：医疗期 / 工伤停工留薪期 / 产假 / 哺乳期 / 事假 / 年假 / 其他
   > - 累计工作年限、本单位工作年限（医疗期长度按此计算）
   > - 休假开始日期
   > - 预计返岗日期（若已知——不知就留空）
   > - 已下达相关书面通知？（工伤认定书、医疗期通知书、产假申请批复等）
   > - 已请求医疗证明/工伤鉴定？若是，什么时候？

3. 使用 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md` 中的用工地表，查该用工地此假别的适用天数（如产假：国家 98 天 + 地方增加天数）。

4. 根据信息算出下一个即将到来的节点：
   - 医疗期未确定长度 → 先按累计工龄和本单位工龄确定 3-24 个月的档位
   - 医疗期届满前 30 日 → 报警节点
   - 工伤停工留薪期未鉴定 → 期满前 30 日报警
   - 产假 → 产假期满和哺乳期结束（婴儿满 1 周岁）两个节点
   - 竞业限制补偿 → 每月支付节点

5. 向 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/leave-register.yaml` 写新条目，用 leave-tracker agent 的休假台账格式。文件不存在就创建。

6. 单行确认：
   > 「已记录。[员工/角色] — [假别] — [用工地] — 开始于 [日期]。第一个节点：[什么事 + 何时]。休假跟踪器会自动提醒。」

## 示例

```
/employment-legal-cn:log-leave
```

```
/employment-legal-cn:log-leave
王工（高级工程师，用工地上海）今天开始医疗期，累计工龄 12 年，本单位 8 年——按规定应享受 12 个月医疗期。
```

```
/employment-legal-cn:log-leave
李某某（用工地广东）今天开始产假，正常分娩。
```
