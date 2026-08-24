---
name: form-generation
description: >
  已弃用（reference-only）—— 请使用 /draft。原表单生成职能已并入 draft skill，
  由 draft 处理各纠纷类型的文书生成（含起诉状、仲裁申请书、答辩状、律师函等模板与办案地感知格式）。
  保留本文件作迁移重定向。
user-invocable: false
---

# [已弃用] 表单生成 → 请用 `/draft`

本 skill 在 v2 重构时并入 `skills/draft/`。`/legal-clinic-cn:draft` 命令处理诊所文书的初稿生成，含表单填充（劳动仲裁申请书、离婚起诉状、人身安全保护令申请书、答辩状等），
按纠纷类型模板与办案地格式产出。

**请改用 `/legal-clinic-cn:draft [文书类型]`。**

完整工作流见 `skills/draft/SKILL.md`。

---

## 转换决策自检

- **A 级直转：** 保留 user-invocable: false 与迁移重定向结构，只把命令名换成 `/legal-clinic-cn:draft`。
- **无 B/C/D。** 属纯粹的迁移页；实体法内容不涉及。
