---
name: matter-workspace
description: >
  管理事项工作区——创建、列出、切换、关闭活动事项，或取消活动事项，使得多客户执业者可以
  把一个客户的上下文与其他客户分开。任何需要知道自己在哪个事项中工作的实质性技能都会读它。
  在中国语境下，事项 = 交易/案件/项目文件夹（并购项目、章程修订、股权重组、投融资）。触发场景：
  用户说「新事项」「切换事项」「列出事项」「关闭事项」，或想只在执业层工作。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业者跨多个客户和事项工作。事项工作区把一个客户或委托事项的上下文与其他分开。本技能管理这些工作区。

## 子命令

- `/corporate-legal-cn:matter-workspace new <slug>` — 创建新事项工作区，跑简短的立案访谈，写 `matter.md`
- `/corporate-legal-cn:matter-workspace list` — 列出事项，含状态和当前活动标记
- `/corporate-legal-cn:matter-workspace switch <slug>` — 设置活动事项
- `/corporate-legal-cn:matter-workspace close <slug>` — 归档事项（移至 `~/.claude/plugins/config/claude-for-legal-cn/corporate-legal-cn/matters/_archived/`，永不删除）
- `/corporate-legal-cn:matter-workspace none` — 取消活动事项，只在执业层工作

## 说明

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/corporate-legal-cn/CLAUDE.md`——确认 `## 事项工作区` 章节已填。若 `启用` 为 `✗`，告诉用户：「事项工作区是关闭的——你被配置为单客户法务，插件从执业层上下文自动工作。若你实际跨多客户工作，重跑 `/corporate-legal-cn:cold-start-interview --redo` 并选律师事务所执业环境。否则，你根本不需要 `/matter-workspace`。」不要报错——对法务用户来说，关闭状态是预期状态。
2. 用下面的工作流。
3. 按 `$ARGUMENTS` 第一个词分派：
   - `new` → 跑立案访谈，写 `~/.claude/plugins/config/claude-for-legal-cn/corporate-legal-cn/matters/<slug>/matter.md`，种入 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-cn/corporate-legal-cn/matters/*/matter.md`，打印表格，标记活动事项。
   - `switch` → 更新执业档案中 `活动事项：` 行。
   - `close` → 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`，在 `history.md` 记录关闭日期。
   - `none` → 把 `活动事项：` 设为 `无——仅执业层上下文`。
4. 向用户展示改动，写入前确认。

## 注释

- 除非执业档案中 `跨事项上下文` 为 `开`，技能从不跨事项读取。
- 归档不是删除。已关闭事项仍可读取，用于档案保管与利益冲突检查。
- Slug 用小写加连字符。若 slug 在归档和活动中重复，归档的在 `_archived/<slug>/` 下保留。

---

多客户执业者（律师事务所——个人所、小型所、大所）跨多个事项工作。一个事项的上下文绝不能泄漏到另一个。本技能是让这件事为真的薄薄文件管理层。

**默认状态是关闭。** 法务用户从来看不到这个——它们只在执业层运行。事项工作区在冷启动时对律师事务所用户开启，或通过编辑执业档案 `## 事项工作区` 章节开启。若 `启用` 为 `✗`，本技能不运行；`/corporate-legal-cn:matter-workspace` 解释关闭状态并建议实际需要事项隔离的用户运行 `/corporate-legal-cn:cold-start-interview --redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/corporate-legal-cn/
├── CLAUDE.md                       # 执业档案
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖项
    │   ├── history.md              # 有日期的事件、决定、草稿、审核日志
    │   ├── notes.md                # 自由格式工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子文件夹）
    └── _archived/
        └── <slug>/                 # 已关闭事项——可读但非活动
```

Slug 用小写加连字符。示例：`beijing-abc-ma-2026`、`zhonglian-caseA`、`vendor-xyz-nda`。

## 活动事项在执业档案中

执业档案 `## 事项工作区` 下的 `活动事项：` 行是唯一真实来源。切换事项编辑该行。无单独的状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 不在 `matters/<slug>/` 或 `matters/_archived/<slug>/`。重复时请用户选另一个。
2. 跑立案访谈：
   - **客户**（我们代理的一方，法务时是内部业务单元）
   - **相对方**（另一侧——可能多个）
   - **事项类型**（读插件执业档案中常见类别；corporate-legal-cn 用：并购买方 | 并购卖方 | 融资 | 董事会/股东会事项 | 实体重组 | 交割后整合 | 章程修订 | 其他）
   - **保密级别**（标准 | 高 | 洁净团队——高级别在跨事项设置下提示额外注意）
   - **关键事实**（2-5 句：事项是关于什么、利益相关方、关切）
   - **本事项对执业 playbook 的覆盖**（如「客户要求 12 个月责任限额上限而非本所标准 3 个月」「相对方是战略合作伙伴——语气保留关系」）
   - **相关事项**（关联事项的 slug）
3. 用下面的模板写 `matters/<slug>/matter.md`。
4. 种入 `matters/<slug>/history.md`，写一条「开立」条目。
5. 创建空的 `matters/<slug>/notes.md`。
6. **不要**自动切换到新事项。问：「切换到 `<slug>` 吗？（`/corporate-legal-cn:matter-workspace switch <slug>`）」

### `list`

枚举 `matters/*/matter.md`。读每份文件的 frontmatter 或前几行提取状态。打印表格：

| Slug | 客户 | 事项类型 | 状态 | 开立 | 活动 |
|---|---|---|---|---|---|

活动事项用 `*` 标记。若有归档项，另起「已归档」标题下列。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。若否，提供 `/corporate-legal-cn:matter-workspace new <slug>`。
2. 编辑执业档案的 `活动事项：` 行为 `活动事项: <slug>`。
3. 向用户展示 matter.md 摘要，方便确认在正确事项上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 追加「关闭」条目，附今日日期。
3. 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`。
4. 若关闭的事项是活动事项，把 `活动事项：` 设为 `无——仅执业层上下文`。

### `none`

把执业档案的 `活动事项：` 设为 `无——仅执业层上下文`。与用户确认。

## `matter.md` 模板

```markdown
[待审核草稿头——按档案 ## 输出——因角色而异；见 ## 谁在用]

# 事项：[客户] — [简短描述]

**Slug：** [slug]
**开立：** [YYYY-MM-DD]
**状态：** 活动
**保密：** [标准 / 高 / 洁净团队]

---

## 各方

**客户：** [名称]
**相对方：** [名称]

## 事项类型

[并购买方 | 并购卖方 | 融资 | 董事会事项 | 实体重组 | 交割后整合 | 章程修订 | 其他——一行说明理由]

## 关键事实

[2-5 句。事项是关于什么。利益相关方。关切。与默认 playbook 不同之处。]

## 事项特有覆盖

*任何偏离执业层 playbook、仅适用本事项的立场。*

- [如：「责任限额上限：客户要求 12 个月，而非本所标准 3 个月。」]
- [如：「语气：保留关系——相对方是战略合作伙伴。」]
- [如：「适用法律：客户要求约定新加坡法，而非中国法。」]

## 相关事项

- [slug — 一行关联理由]

## 保密说明

[若为高级或洁净团队，说明原因。谁可查看事项文件。即便全局跨事项开启，本事项是否允许跨事项上下文。]
```

## `history.md` 种入

```markdown
# 历史：[客户] — [简短描述]

只追加事件日志。最新在最上。

---

## [YYYY-MM-DD] — 事项开立

立案完成。Slug：`[slug]`。状态：活动。
[matter.md 之外任何值得保留的初始上下文——如「因 [相对方] 发来的主协议草稿开立」。]
```

## 跨事项上下文

执业档案有 `跨事项上下文：` 标志。为 `关` 时（默认），一个事项 A 中工作的技能**从不读**任何其他事项 B 的文件。这是本设置存在的保密保证。

为 `开` 时，技能仅在用户明确要求时才能跨事项读文件（如「比较我们最近五个并购事项中对赌条款的立场」）。即便 `开`，默认也只加载活动事项，除非用户要求跨事项视图。

## 本 skill 不做的事

- **不做利益冲突检查。** 冲突是执业者/律所自己的事；立案捕获用户申报的内容。
- **不强制保管期限。** 关闭归档事项；不删除。保管政策超出范围。
- **不自动路由输出。** 实质性技能决定写到哪；本技能告诉它*哪个文件夹*是活动的，不告诉它*放什么*。
- **不决定是否合适跨事项。** 它读标志并遵守。

## 质量自检

本次转换决策：本技能为 A 级直转。事项工作区是通用文件管理层，与法域无关——保留全部逻辑（子命令、Slug 规则、跨事项标志、活动事项行、归档不删除）。替换的：路径从 `claude-for-legal/corporate-legal/` 改为 `claude-for-legal-cn/corporate-legal-cn/`；事项类型例子改为中国实务（并购买方/卖方、融资、董事会事项、实体重组、章程修订、交割后整合）；执业环境说明改为「律师事务所（个人所、小型所、大所）」中国语境；示例 slug 改为中文语境（beijing-abc-ma-2026、zhonglian-caseA）；覆盖项示例改为中国实务（责任限额、适用法律新加坡 vs 中国）；保密工作产品头改为待审核草稿头。无实体法引用需 `[待核验条文号]`。
