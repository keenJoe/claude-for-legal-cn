---
name: matter-workspace
description: >
  管理事项工作区 —— 新建、列表、切换、关闭、脱离（执业档案层）。
  仅律所（多客户执业）用得上；公司法务默认关闭。
  在跨客户/事项工作时，用工作区让一个事项的上下文不外溢到另一个。
argument-hint: "<new | list | switch | close | none> [事项标识]"
---

# /matter-workspace

律所从业者在多个客户与事项间切换工作。事项工作区把一个客户或委托的上下文与其他分开。这个技能管理这些工作区。

## 子命令

- `/product-legal-cn:matter-workspace new <标识>` —— 新建一个事项工作区，做一段短访谈，写 `matter.md`
- `/product-legal-cn:matter-workspace list` —— 列出事项，含状态与当前事项标记
- `/product-legal-cn:matter-workspace switch <标识>` —— 切换到某事项
- `/product-legal-cn:matter-workspace close <标识>` —— 归档一个事项（移到 `~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/matters/_archived/`，永不删除）
- `/product-legal-cn:matter-workspace none` —— 脱离当前事项，回到执业档案层

## 执行指令

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 已填。`启用` 是 `✗` 就告诉用户：「事项工作区是关的 —— 你被配置为面向一家公司的内部产品法务，插件自动使用执业档案层上下文。如果你实际上跨多客户工作，重跑 `/product-legal-cn:cold-start-interview --redo` 并选律所环境。否则不需要用 `/matter-workspace`。」不要抛错 —— 关闭状态对内部用户是预期状态。
2. 按下述存储布局与子命令逻辑执行。
3. 按 `$ARGUMENTS` 的第一个 token 分派：
   - `new` → 走访谈，写 `~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/matters/<标识>/matter.md`，初始化 `history.md` 与 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/matters/*/matter.md`，打印一张表，标出当前事项。
   - `switch` → 更新执业档案 CLAUDE.md 里的 `当前事项：` 行。
   - `close` → 把 `~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/matters/<标识>/` 移到 `matters/_archived/<标识>/`，在 `history.md` 里追加关闭日期。
   - `none` → 把 `当前事项：` 设为 `无 —— 仅执业档案层上下文`。
4. 把变更展示给用户，确认后再写。

## 说明

- 除非执业档案 CLAUDE.md 里 `跨事项上下文` 为 `on`，本技能绝不跨事项读文件。
- 归档不是删除 —— 已关事项仍可读，用于合规留痕/利益冲突排查/客户档案保全。
- 事项标识用小写字母加连字符。标识跨归档与在办重复时，归档者保留在 `_archived/<标识>/` 下。

---

# 事项工作区

多客户从业者（律所 —— 个人/团队/大所）跨多个事项工作。一个事项的上下文不能外溢到另一个。这个技能是让这件事成立的**薄薄一层文件管理**。

**默认关闭。** 内部用户永远看不到本节 —— 他们只在执业档案层运行。事项工作区在律所用户的冷启动时开启，或通过编辑执业档案 CLAUDE.md 的 `## 事项工作区` 打开。`启用` 是 `✗` 时，本技能不运行；`/matter-workspace` 命令解释关闭状态，建议真的需要事项隔离的用户跑 `/cold-start-interview --redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/product-legal-cn/
├── CLAUDE.md                       # 执业档案层
└── matters/
    ├── <标识>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖项
    │   ├── history.md              # 事件/决定/初稿/审查的日志（按日期）
    │   ├── notes.md                # 自由格式工作笔记
    │   └── outputs/                # 该事项的技能输出（可选子目录）
    └── _archived/
        └── <标识>/                 # 已关事项 —— 可读，不参与当前工作
```

标识用小写字母加连字符。示例：`acme-launch-2026`、`zenith-marketing-review`、`vendor-xyz-sdk`。

## 当前事项在执业档案 CLAUDE.md 里

执业档案 CLAUDE.md 里 `## 事项工作区` 下的 `当前事项：` 行是唯一真实来源。切换事项即编辑这一行。没有独立的状态文件。

## 子命令逻辑

### `new <标识>`

1. 确认 `matters/<标识>/` 或 `matters/_archived/<标识>/` 都没占用。占用了就请用户换一个标识。
2. 走访谈：
   - **客户**（我们代理的一方，或内部业务方）
   - **相对方**（另一侧 —— 可能多方）
   - **事项类型**（读插件档案的常见分类；对 product-legal-cn：发布 | 功能审查 | 营销文案审查 | 风险深评 | 产品线（长期）| 其他）
   - **保密级别**（标准 | 强化 | 洁净团队 —— 强化时在跨事项设置里额外小心）
   - **关键事实**（2-5 句：事项是什么、干系人有谁、影响是什么）
   - **对执业档案的事项级覆盖项**（例如「客户要求文案立场比默认更严 —— 绝对化用语零容忍」「相对方是战略伙伴 —— 保关系语气」）
   - **相关事项**（其他相关事项的标识）
3. 按下模板写 `matters/<标识>/matter.md`。
4. 在 `matters/<标识>/history.md` 里种下一条「开立」记录。
5. 建一个空的 `matters/<标识>/notes.md`。
6. **不**自动切换到新事项。问：「要切到 `<标识>` 吗？（`/product-legal-cn:matter-workspace switch <标识>`）」

### `list`

枚举 `matters/*/matter.md`。读每个文件的头部或前几行抽状态。打印表：

| 标识 | 客户 | 事项类型 | 状态 | 开立日期 | 当前 |
|---|---|---|---|---|---|

当前事项用 `*` 标出。若有归档，另起「已归档」小节列 `_archived/*`。

### `switch <标识>`

1. 确认 `matters/<标识>/matter.md` 存在。不存在就提议 `/product-legal-cn:matter-workspace new <标识>`。
2. 编辑执业档案 CLAUDE.md 的 `当前事项：` 行为 `当前事项：<标识>`。
3. 把该 matter.md 摘要展示给用户，让他确认走对了事项。

### `close <标识>`

1. 确认 `matters/<标识>/` 存在。
2. 在 `matters/<标识>/history.md` 追加一条「关闭」记录，含今日日期。
3. 把 `matters/<标识>/` 移到 `matters/_archived/<标识>/`。
4. 若关闭的是当前事项，把 `当前事项：` 设为 `无 —— 仅执业档案层上下文`。

### `none`

把执业档案 CLAUDE.md 的 `当前事项：` 设为 `无 —— 仅执业档案层上下文`。与用户确认。

## `matter.md` 模板

```markdown
[草稿头 —— 按插件档案 ## 输出 —— 按角色不同；见执业档案 `## 谁在用`]

# 事项：[客户] —— [简述]

**标识：** [标识]
**开立日期：** [YYYY-MM-DD]
**状态：** 在办
**保密级别：** [标准 / 强化 / 洁净团队]

---

## 各方

**客户：** [名称]
**相对方：** [名称]

## 事项类型

[发布 | 功能审查 | 营销文案审查 | 风险深评 | 产品线（长期）| 其他 —— 一行说明]

## 关键事实

[2-5 句。事项是什么。干系人有谁。影响是什么。相对默认 playbook 特殊在哪。]

## 事项级覆盖项

*任何偏离执业档案的、只适用于本事项的立场。*

- [例如「文案立场：客户零容忍绝对化用语，比默认更严」]
- [例如「语气：保关系 —— 相对方是战略伙伴」]
- [例如「适用法律：客户要求为境外法律 —— 触发跨法域全面审查」]

## 相关事项

- [标识 —— 一行说明为什么相关]

## 保密备注

[若强化或洁净团队，说明为什么。谁可看事项文件。是否即便全局跨事项上下文为 on，本事项也不参与。]
```

## `history.md` 种子

```markdown
# 历史：[客户] —— [简述]

只追加事件日志。最新在上。

---

## [YYYY-MM-DD] —— 事项开立

访谈完成。标识：`[标识]`。状态：在办。
[值得保留的初始上下文（超出 matter.md 的） —— 例如「因相对方提交的 PRD 收到审查请求而开立」。]
```

## 跨事项上下文

执业档案 CLAUDE.md 有 `跨事项上下文：` 开关。为 `off`（默认）时，在事项 A 工作的技能**绝不读**任何其他 `matters/B/` 下的文件。这是这个设置存在的目的：保密性保证。

为 `on` 时，技能可跨事项文件读，但只在用户明确要求时（例如「对比过去五个客户在这类文案上的立场」）。即便 `on`，默认也只加载当前事项，除非用户点了跨事项视图。

## 本 skill 不做的事

- **做利益冲突检查。** 冲突排查是从业者/律所的活；访谈只登记用户声明的内容。
- **执行留存政策。** 关闭是归档，不删除。留存政策不在本技能范围。
- **自动路由输出。** 实体技能决定往哪写；本技能只告诉它**哪个文件夹**当前是激活的，不管里面放什么。
- **判断是否可跨事项。** 它读开关并遵守。

## 转换决策自检

- **A 级直转：** 事项工作区机制是通用的文件隔离方案，与法域无关。子命令、存储布局、跨事项开关、归档不删除的规范全部直转。
- **B 级微改：** 事项类型的默认分类改为中国产品法务的常见分类（发布/功能审查/营销文案审查/风险深评/产品线）；路径从 `claude-for-legal/product-legal/` 改为 `claude-for-legal-cn/product-legal-cn/`；命令前缀改为 `/product-legal-cn:`；覆盖项示例改为中国实务常见（绝对化用语零容忍、保关系语气、境外法律触发跨法域审查）。中文表述自然化。
