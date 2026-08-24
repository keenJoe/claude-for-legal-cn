---
name: matter-workspace
description: >
  管理事项工作区——新建、列出、切换、关闭或解绑（回到执业层）。创建、列出、切换、
  关闭、解绑活跃事项，让一个客户事务的上下文永不泄漏到另一个。触发场景：多客户
  执业者说「新事项」「切换事项」「列出我的事项」「关闭这个事项」，或需要管理
  哪个事项是活跃的。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业者跨多个客户和事项工作。事项工作区把一个客户或委托事务的上下文与所有其他隔离。本技能管理那些工作区。

## 子命令

- `/employment-legal-cn:matter-workspace new <slug>` —— 新建事项工作区，跑简短受理，写 `matter.md`
- `/employment-legal-cn:matter-workspace list` —— 列出事项，附状态和活跃标记
- `/employment-legal-cn:matter-workspace switch <slug>` —— 设活跃事项
- `/employment-legal-cn:matter-workspace close <slug>` —— 归档事项（移到 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/matters/_archived/`，绝不删除）
- `/employment-legal-cn:matter-workspace none` —— 从任何活跃事项解绑，仅在执业层工作

## 说明

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 章节已填。若 `启用` 为 `✗`，告诉用户：「事项工作区关着——你被配置为一家公司法务，插件从执业层上下文自动工作。若你实际跨多个客户工作，重跑 `/employment-legal-cn:cold-start-interview --redo` 并选择私人执业设置。否则你不需要 `/matter-workspace`。」不要报错——公司法务用户的默认状态就是关。
2. 使用下面的子命令逻辑。
3. 分派 `$ARGUMENTS` 的第一个词：
   - `new` → 跑受理访谈，写 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/matters/<slug>/matter.md`，种子 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/matters/*/matter.md`，打印表格，标出活跃事项。
   - `switch` → 更新执业层 CLAUDE.md 的 `活跃事项：` 行。
   - `close` → 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`，在 `history.md` 记录关闭日。
   - `none` → 设 `活跃事项：` 为 `none — 仅执业层上下文`。
4. 展示什么变了，写入前让用户确认。

## 备注

- 除非执业层 CLAUDE.md 中 `跨事项上下文` 为 `on`，技能绝不跨事项读取。
- 归档不是删除——关闭的事项按留档/冲突用途仍可读。
- Slug 为小写连字符。归档与活跃 slug 重用时，归档的保留在 `_archived/<slug>/`。

---

## 参考

多客户执业者（私人执业——个人、小所、大所）跨多个事项工作。一个的上下文不能泄漏到另一个。本技能是让这件事成立的薄薄文件管理层。

**默认状态是关。** 公司法务用户从不看到这个——他们只在执业层运行。事项工作区在私人执业用户的冷启动时打开，或通过编辑执业层 CLAUDE.md 的 `## 事项工作区` 打开。若 `启用` 为 `✗`，本技能不运行；而是解释关闭状态并建议实际需要事项隔离的用户运行 `/employment-legal-cn:cold-start-interview --redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/employment-legal-cn/
├── CLAUDE.md                       # 执业层执业档案
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖
    │   ├── history.md              # 事件、决定、草稿、审查的按日志
    │   ├── notes.md                # 自由格式工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子目录）
    └── _archived/
        └── <slug>/                 # 已关闭事项——可读但不活跃
```

Slug 为小写连字符。示例：`acme-termination-2026`、`zenith-non-compete`、`vendor-xyz-outsource-dispute`。

## 活跃事项在执业层 CLAUDE.md 中

执业层 CLAUDE.md 的 `## 事项工作区` 下的 `活跃事项：` 行是单一事实来源。切换事项就是编辑这一行。没有单独的状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 未出现在 `matters/<slug>/` 或 `matters/_archived/<slug>/`。若重用，让用户选另一个 slug。
2. 跑受理访谈：
   - **客户**（我们代表的一方，或公司法务时的内部业务单元）
   - **相对方**（对方——可能是多个）
   - **事项类型**（劳动用工插件的典型类别：招聘 | 解除 | 调查 | 休假医疗期 | 三期女职工 | 用工形式认定 | 跨境用工 | 制度项目 | 竞业限制 | 仲裁应诉 | 其他）
   - **保密级别**（标准 | 加强 | 净团队 —— 加强会在跨事项设置里提示额外注意）
   - **关键事实**（2–5 句：这个事项是关于什么的、谁是相关方、什么是紧要的）
   - **对执业 playbook 的事项特定覆盖**（如「本事项的仲裁地约定必须在客户所在地」「相对方是战略伙伴——保持关系导向语气」）
   - **相关事项**（任何相关事项的 slug）
3. 用下面的模板写 `matters/<slug>/matter.md`。
4. 用单条「开启」条目种子 `matters/<slug>/history.md`。
5. 创建空的 `matters/<slug>/notes.md`。
6. **不**自动切换到新事项。问：「现在切换到 `<slug>` 吗？（`/employment-legal-cn:matter-workspace switch <slug>`）」

### `list`

枚举 `matters/*/matter.md`。读每个文件的前几行提取状态。打印表格：

| Slug | 客户 | 事项类型 | 状态 | 开启日 | 活跃 |
|---|---|---|---|---|---|

用 `*` 标当前活跃事项。若有归档，在单独的「已归档」标题下含 `_archived/*`。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。若不，提供 `/employment-legal-cn:matter-workspace new <slug>`。
2. 编辑执业层 CLAUDE.md 的 `活跃事项：` 行为 `活跃事项: <slug>`。
3. 展示 matter.md 摘要让用户确认在正确事项上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 追加一条今天日期的「关闭」条目。
3. 移 `matters/<slug>/` → `matters/_archived/<slug>/`。
4. 若被关闭的是活跃事项，设 `活跃事项：` 为 `none — 仅执业层上下文`。

### `none`

设执业层 CLAUDE.md 的 `活跃事项：` 为 `none — 仅执业层上下文`。让用户确认。

## `matter.md` 模板

```markdown
[工作成果头部 —— 按执业层 CLAUDE.md 的 `## 输出` —— 因角色而异；见 `## 谁在用`]

# 事项：[客户] — [简短描述]

**Slug：** [slug]
**开启：** [YYYY-MM-DD]
**状态：** active
**保密：** [标准 / 加强 / 净团队]

---

## 各方

**客户：** [名]
**相对方：** [名(s)]

## 事项类型

[招聘 | 解除 | 调查 | 休假医疗期 | 三期女职工 | 用工形式认定 | 跨境用工 | 制度项目 | 竞业限制 | 仲裁应诉 | 其他 —— 附一行理由]

## 关键事实

[2–5 句。这个事项是关于什么的。谁是相关方。什么是紧要的。为什么与默认 playbook 不同。]

## 事项特定覆盖

*适用于此事项且仅此事项的任何对执业层 playbook 的偏离。*

- [如「补偿档位：本客户偏保守，除非非常清楚，否则按 2N 敞口预留」]
- [如「语气：保持关系导向——相对方是战略伙伴」]
- [如「争议解决地约定：必须客户所在地」]

## 相关事项

- [slug — 一行为什么相关]

## 关于保密的备注

[若加强或净团队，描述为什么。谁可以看事项文件。跨事项上下文即使全局为 on 是否仍允许。]
```

## `history.md` 种子

```markdown
# 历史：[客户] — [简短描述]

追加式事件日志。最新在最上。

---

## [YYYY-MM-DD] — 事项开启

受理完成。Slug：`[slug]`。状态：active。
[matter.md 之外值得保存的任何初始上下文——如「因客户被劳动仲裁申请书送达而开启」。]
```

## 跨事项上下文

执业层 CLAUDE.md 有 `跨事项上下文：` 标志。为 `off`（默认）时，一个技能在事项 A 里工作，对任何其他 `B`，**绝不读** `matters/B/` 里的文件。周期。这就是该设置存在要提供的保密保证。

为 `on` 时，技能只有在用户明确要求时才可以跨事项文件夹读（如「比较过去五个解除事项里我们对补偿档位的立场」）。即使 `on`，默认也仅加载活跃事项，除非用户请求跨事项视图。

## 本技能不做的事

- **跑冲突检查。** 冲突是执业者/律所的工作；受理捕获用户所声明的。
- **强制留档期限。** 关闭归档一个事项；它不删除。留档政策超出范围。
- **自动路由输出。** 实质技能决定写到哪儿；本技能告诉它*哪个文件夹*是活跃的，不是往里放什么。
- **决定跨事项是否合适。** 它读取标志并遵守。
