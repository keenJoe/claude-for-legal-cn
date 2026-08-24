---
name: plain-language-letters
description: >
  已弃用（reference-only）—— 常规通信用 /client-letter；实质进展说明用 /status client。
  v2 重构时拆分为两个更聚焦的 skill。保留本文件作迁移重定向。
user-invocable: false
---

# [已弃用] 通俗语言信函 → 请用 `/client-letter` 与 `/status client`

本 skill 在 v2 重构时拆分为：

- **常规通信**（预约确认、材料清单、简短「已提交」进展）→ `skills/client-letter/` —— 用 `/legal-clinic-cn:client-letter [类型]`
- **实质受援人状态说明** → `skills/status/` 的面向受援人模式 —— 用 `/legal-clinic-cn:status client`

两者都应用 CLAUDE.md 里的通俗语言标准（可读性、无术语）。

完整工作流见对应 SKILL.md。

---

## 转换决策自检

- **A 级直转：** 保留 user-invocable: false 与迁移重定向结构，命令换成 `/legal-clinic-cn:client-letter` 与 `/legal-clinic-cn:status client`。
- **无 B/C/D。** 属纯粹的迁移页。
