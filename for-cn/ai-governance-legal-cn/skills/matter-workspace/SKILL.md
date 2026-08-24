---
name: matter-workspace
description: >
  管理事项工作区 —— 新建、列出、切换、关闭、脱离（回到执业级）。
  文件管理逻辑：把一个客户或一次委托的上下文与其它隔离。触发场景：跨多个客户
  或事项工作时，用户说「新事项」「切事项」「列出事项」「关闭事项」，或任何实质
  技能需要知道自己在哪个事项里运行时。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

从业者在多个客户和事项之间工作。事项工作区把一个客户或委托的上下文与其它隔离。这个技能管理这些工作区。

在中国语境下，「事项工作区」= 案件/交易/委托文件夹（如 AI 用例专项审查、供应商 AI 合同评审、监管约谈应对、AI 影响评估委托）。

## 子命令

- `/ai-governance-legal-cn:matter-workspace new <slug>` —— 新建事项工作区，做一轮短问询，写 `matter.md`
- `/ai-governance-legal-cn:matter-workspace list` —— 列出事项，带状态和活跃标记
- `/ai-governance-legal-cn:matter-workspace switch <slug>` —— 设活跃事项
- `/ai-governance-legal-cn:matter-workspace close <slug>` —— 归档事项（移到 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/matters/_archived/`，绝不删除）
- `/ai-governance-legal-cn:matter-workspace none` —— 脱离任何活跃事项，只在执业级工作

## 指令

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 已填写。若 `启用` 为 `✗`，告诉用户：「事项工作区已关 —— 你被配置为只有一个客户的公司法务实践，插件自动从执业级上下文工作。若你实际跨多个客户工作，重跑 `/ai-governance-legal-cn:cold-start-interview --redo` 并选私人执业环境。否则，你根本不需要 `/matter-workspace`。」不要报错 —— 关闭态是法务部用户的预期状态。
2. 用下方工作流。
3. 按 `$ARGUMENTS` 的第一个 token 分发：
   - `new` → 走问询，写 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/matters/<slug>/matter.md`，种下 `history.md` 与 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/matters/*/matter.md`，打印一张表，标出活跃事项。
   - `switch` → 更新执业级 CLAUDE.md 中的 `活跃事项：` 行。
   - `close` → 把 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/matters/<slug>/` 移到 `~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/matters/_archived/<slug>/`，在 `history.md` 记关闭日期。
   - `none` → 把 `活跃事项：` 设为 `无 —— 仅执业级上下文`。
4. 展示改动，写入前请用户确认。

## 备注

- 除非执业级 CLAUDE.md 中 `跨事项上下文` 为 `on`，本技能绝不跨事项读文件。
- 归档不是删除 —— 关闭的事项仍可读，供留档、利益冲突查询用。
- slug 用小写和连字符。若归档中和活跃中都有相同 slug，归档版被保留在 `_archived/<slug>/`。

---

多客户执业者（律所 —— 个人、小所、大所）跨多个事项工作。一个的上下文不能泄漏到另一个。这个技能是让这件事为真的薄薄一层文件管理。

**默认关闭。** 法务部用户永远看不到 —— 他们只在执业级工作。事项工作区在冷启动为私人执业用户打开，或通过编辑执业级 CLAUDE.md 的 `## 事项工作区` 打开。若 `启用` 为 `✗`，本技能不运行；上面的工作流解释关闭态并建议真正需要事项隔离的用户跑 `/ai-governance-legal-cn:cold-start-interview --redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/ai-governance-legal-cn/
├── CLAUDE.md                       # 执业级执业档案
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖
    │   ├── history.md              # 事件、决定、草稿、审查的日期日志
    │   ├── notes.md                # 自由格式工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭事项 —— 可读但非活跃
```

slug 用小写和连字符。示例：`acme-aia-2026`、`xyz-vendor-review`、`hr-recruit-ai`。

## 活跃事项在执业级 CLAUDE.md 中

执业级 CLAUDE.md 中 `## 事项工作区` 下的 `活跃事项：` 行是唯一事实来源。切换事项就是编辑那一行。没有单独的状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 未在 `matters/<slug>/` 或 `matters/_archived/<slug>/` 中出现。已重用，请用户换。
2. 运行问询：
   - **客户**（我们代表的一方，或若是法务部则是内部业务单元）
   - **相对方**（对方 —— 可能多个）
   - **事项类型**（读插件执业档案的典型类别；对 ai-governance-legal-cn：用例专项审查（内部）| 供应商 AI 审查 | AIA 委托 | 监管应对 | 制度项目 | 其它）
   - **保密级别**（标准 | 加强 | 净团队 —— 加强在跨事项设置下要求额外注意）
   - **关键事实**（2-5 句：这个事项是关于什么、利益相关方是谁、有什么风险）
   - **对执业级 playbook 的事项级覆盖**（如「客户要求 AI 供应商责任上限不低于年费 200%，不用房内标准 100%」「相对方是战略伙伴 —— 保关系语气」）
   - **相关事项**（任何相关事项的 slug）
3. 用下方模板写 `matters/<slug>/matter.md`。
4. 种下 `matters/<slug>/history.md`，一条「开立」记录。
5. 创建空的 `matters/<slug>/notes.md`。
6. **不**自动切到新事项。问：「现在切到 `<slug>` 吗？（`/ai-governance-legal-cn:matter-workspace switch <slug>`）」

### `list`

枚举 `matters/*/matter.md`。读每个文件的前几行提取状态。打印表：

| Slug | 客户 | 事项类型 | 状态 | 开立 | 活跃 |
|---|---|---|---|---|---|

用 `*` 标当前活跃事项。如有 `_archived/*`，放在单独的「已归档」标题下。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。不存在则提议 `/ai-governance-legal-cn:matter-workspace new <slug>`。
2. 把执业级 CLAUDE.md 的 `活跃事项：` 行编辑为 `活跃事项：<slug>`。
3. 展示 matter.md 摘要让用户确认走对了事项。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 追加今日「关闭」记录。
3. 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`。
4. 若关闭的事项是活跃事项，把 `活跃事项：` 设为 `无 —— 仅执业级上下文`。

### `none`

把执业级 CLAUDE.md 的 `活跃事项：` 设为 `无 —— 仅执业级上下文`。请用户确认。

## `matter.md` 模板

```markdown
[工作产品头 —— 按插件配置 ## 输出 —— 因角色而异；见执业级 CLAUDE.md `## 谁在用`]

# 事项：[客户] —— [简短描述]

**Slug：** [slug]
**开立日期：** [YYYY-MM-DD]
**状态：** 活跃
**保密级别：** [标准 / 加强 / 净团队]

---

## 各方

**客户：** [名称]
**相对方：** [名称]

## 事项类型

[用例专项审查 | 供应商 AI 审查 | AIA 委托 | 监管应对 | 制度项目 | 其它 —— 附一句话理由]

## 关键事实

[2-5 句。这个事项关于什么。利益相关方是谁。有什么风险。与默认 playbook 有什么不同。]

## 事项级覆盖

*任何偏离执业级 playbook、只对本事项适用的项。*

- [如「AI 供应商责任上限：客户要求年费 200%，不用房内标准 100%」]
- [如「语气：保关系 —— 相对方是战略伙伴」]
- [如「适用法律：必须约定中国法，不用相对方所在地法」]

## 相关事项

- [slug —— 一行说明为何相关]

## 保密说明

[若加强或净团队，说明原因。谁可看事项文件。即便全局跨事项上下文开启，本事项是否仍不允许。]
```

## `history.md` 种子

```markdown
# 历史：[客户] —— [简短描述]

只追加事件日志。最新在最前。

---

## [YYYY-MM-DD] —— 事项开立

问询完成。Slug：`[slug]`。状态：活跃。
[任何值得留存的初始上下文 —— 如「因 [相对方] 送来 AI 服务协议草稿而开立」。]
```

## 跨事项上下文

执业级 CLAUDE.md 有一个 `跨事项上下文：` 标记。它是 `off`（默认）时，事项 A 里工作的技能对任何其它事项 B 的文件**绝不读取**。就这样。这是这个设置存在的保密保证。

它是 `on` 时，技能只在用户显式要求时才能跨事项读文件（如「比较过去五份供应商 AI 审查的责任立场」）。即便 `on`，默认只加载活跃事项，除非用户要求跨事项视图。

## 本技能不做的事

- **不做利益冲突检查。** 利益冲突是从业者/律所的职责；问询记录用户声明的内容。
- **不强制留存。** 关闭把事项归档；不删除。留存策略在本技能范围外。
- **不自动路由输出。** 由实质技能决定往哪写；本技能只告诉它**哪个文件夹**是活跃的，不管里面放什么。
- **不判断跨事项是否合适。** 它读标记并遵守。
