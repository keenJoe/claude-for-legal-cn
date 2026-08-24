---
name: matter-workspace
description: >
  管理事项工作区——新建、列出、切换、关闭事项，或断开到执业级。为多客户执业者把每个客户或
  委托业务的上下文与其他分开。触发场景：用户想开新事项、切事项、列事项、关闭/归档事项，
  或想只在执业级工作。
argument-hint: '<new | list | switch | close | none> [slug]'
---

# /matter-workspace

多客户执业者跨多个客户和委托业务工作。事项工作区把一个客户或一个委托业务的上下文与其他分开。本技能管理这些工作区。

## 子命令

- `/privacy-legal-cn:matter-workspace new <slug>` —— 新建事项，跑一段短的入口访谈，写 `matter.md`
- `/privacy-legal-cn:matter-workspace list` —— 列出事项及其状态与当前活动标记
- `/privacy-legal-cn:matter-workspace switch <slug>` —— 设定活动事项
- `/privacy-legal-cn:matter-workspace close <slug>` —— 归档事项（移到 `~/.claude/plugins/config/claude-for-legal-cn/privacy-legal-cn/matters/_archived/`，永不删除）
- `/privacy-legal-cn:matter-workspace none` —— 断开活动事项，仅按执业级工作

## 指令

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/privacy-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 已配置。若 `启用` 为 `✗`，告诉用户：「事项工作区已关——你被配置为服务单一公司的公司法务，插件从执业级上下文自动工作。如果你实际跨多个客户，请重跑 `/privacy-legal-cn:cold-start-interview --redo` 并选私人执业环境。否则你根本不需要 `/matter-workspace`。」不要报错——关闭状态就是公司法务用户的预期状态。
2. 使用下方子命令逻辑。
3. 按 `$ARGUMENTS` 的第一个 token 分派：
   - `new` → 跑入口访谈，写 `~/.claude/plugins/config/claude-for-legal-cn/privacy-legal-cn/matters/<slug>/matter.md`，播种 `history.md` 和 `notes.md`。
   - `list` → 枚举 `matters/*/matter.md`，打印表，标出活动事项。
   - `switch` → 更新执业级 CLAUDE.md 里的 `活动事项：` 行。
   - `close` → 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`，在 `history.md` 记关闭日。
   - `none` → 把 `活动事项：` 设为 `无 —— 仅执业级上下文`。
4. 向用户展示改动、写入前确认。

## 说明

- 除非执业级 CLAUDE.md 里 `跨事项上下文` 为 `on`，本技能永不跨事项读取。
- 归档不是删除——已关闭事项仍可读，用于保存期限/利益冲突目的。
- Slug 用小写连字符。若某个 slug 在归档和活动之间复用，归档那份保留在 `_archived/<slug>/`。

---

# 事项工作区

多客户执业者（私人执业——个人所、小所、大所）跨多个事项工作。一个事项的上下文不能泄到另一个。本技能是让这件事真正成立的薄文件管理层。

**默认状态是关。** 公司法务用户从不看到这个——他们仅按执业级运行。事项工作区在冷启动里为私人执业用户打开，或在执业级 CLAUDE.md 编辑 `## 事项工作区` 打开。若 `启用` 为 `✗`，本技能不跑;上述流程说明关闭状态并建议用户重跑 `/privacy-legal-cn:cold-start-interview --redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/privacy-legal-cn/
├── CLAUDE.md                       # 执业级执业档案
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖
    │   ├── history.md              # 日期化的事件、决策、草稿、审查日志
    │   ├── notes.md                # 自由格式的工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子目录）
    └── _archived/
        └── <slug>/                 # 已关闭事项 —— 可读但不活动
```

Slug 用小写连字符。例：`acme-pia-2026`、`zenith-dpa-review`、`vendor-xyz-cross-border`。

## 活动事项在执业 CLAUDE.md 中

执业级 CLAUDE.md `## 事项工作区` 下的 `活动事项：` 行是**唯一真相源**。切事项就是编辑那一行。无独立状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 未在 `matters/<slug>/` 或 `matters/_archived/<slug>/` 出现。已用就请用户换。
2. 跑入口访谈：
   - **客户**（我们代表的一方，或公司法务里的内部业务单元）
   - **相对方**（另一侧——可能多个）
   - **事项类型**（读插件执业档案里的典型类别；对 privacy-legal-cn：PIIA（处理活动）| 委托处理协议审查 | 个人权利请求 | 监管问询 | 数据出境路径审查 | 数据安全事件 | 其他）
   - **保密等级**（标准 | 加强 | 净室——加强在跨事项设置里会促加强注意）
   - **关键事实**（2-5 句：本事项讲什么、关键人是谁、利害在哪）
   - **事项特定的对执业 playbook 的覆盖**（如「客户要求境内存储，覆盖插件默认」「相对方是战略伙伴——保持关系的语气」）
   - **相关事项**（任何关联事项的 slug）
3. 用下方模板写 `matters/<slug>/matter.md`。
4. 播种 `matters/<slug>/history.md`，一条「已开」条目。
5. 建空的 `matters/<slug>/notes.md`。
6. **不**自动切到新事项。问：「现在切到 `<slug>` 吗？（`/privacy-legal-cn:matter-workspace switch <slug>`）」

### `list`

枚举 `matters/*/matter.md`。读每份 front-matter 或前几行提取状态。打印表：

| Slug | 客户 | 事项类型 | 状态 | 开启日 | 活动 |
|---|---|---|---|---|---|

活动事项用 `*` 标。有归档的另起「归档」标题列出。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。不存在则提供 `/privacy-legal-cn:matter-workspace new <slug>`。
2. 编辑执业级 CLAUDE.md 的 `活动事项：` 为 `活动事项：<slug>`。
3. 向用户展示 `matter.md` 摘要,让他们确认切对了。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 在 `matters/<slug>/history.md` 追加一条「关闭」条目,记今天。
3. 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`。
4. 若关闭的是活动事项,把 `活动事项：` 设为 `无 —— 仅执业级上下文`。

### `none`

把执业级 CLAUDE.md 的 `活动事项：` 设为 `无 —— 仅执业级上下文`。与用户确认。

## `matter.md` 模板

```markdown
[工作产物头部 —— 按插件配置 ## 输出——按角色不同]

# 事项：[客户] —— [简短描述]

**Slug：** [slug]
**开启日：** [YYYY-MM-DD]
**状态：** 活动
**保密等级：** [标准 / 加强 / 净室]

---

## 当事方

**客户：** [名称]
**相对方：** [名称（可多个）]

## 事项类型

[PIIA（处理活动） | 委托处理协议审查 | 个人权利请求 | 监管问询 | 数据出境路径审查 | 数据安全事件 | 其他 —— 一行理由]

## 关键事实

[2-5 句。本事项讲什么。关键人是谁。利害在哪。什么让它区别于默认 playbook。]

## 事项特定覆盖

*任何偏离执业级 playbook、仅适用于本事项的项。*

- [例：「数据存储：客户要求境内且指定 华东。」]
- [例：「语气：保持关系——相对方是战略伙伴。」]
- [例：「适用法律：必须约定英国法，非中国法（本事项跨境项目）」]

## 相关事项

- [slug —— 一行为何相关]

## 关于保密的说明

[若加强或净室，说明为什么。谁可见此事项文件。全局跨事项若已开是否仍允许。]
```

## `history.md` 播种

```markdown
# 历史：[客户] —— [简短描述]

追加式事件日志。最新在顶部。

---

## [YYYY-MM-DD] —— 事项开启

入口访谈完成。Slug：`[slug]`。状态：活动。
[任何超出 matter.md 值得留存的初始上下文——如「因收到[相对方]的委托处理协议草稿开启」。]
```

## 跨事项上下文

执业级 CLAUDE.md 有个 `跨事项上下文：` 开关。为 `off`（默认）时，事项 A 中的技能**永不读取**任何其他事项 B 的文件。就这么严。这是本设置存在要提供的保密保证。

为 `on` 时，技能可跨事项文件夹读取，但仅当用户明确要求时（如「比较过去五个供应商事项里我们对数据出境立场的处理」）。即便 `on`，默认也只加载活动事项，除非用户要求跨事项视图。

## 本技能不做的事

- **跑利益冲突检查。** 冲突是执业者/律所的活;入口只记录用户申报的。
- **执行保存期限。** 关闭归档;不删除。保存期限政策不在范围内。
- **自动路由输出。** 实质技能决定往哪写;本技能告诉它*哪个文件夹*是活动的,而不告诉它放什么进去。
- **决定跨事项是否合适。** 它读开关并遵从。

## 本文件转换说明

- 分级：**A 直转**。工作流架构（子命令 new/list/switch/close/none、matter.md 模板、跨事项开关、归档 vs 删除区分）完整保留。
- **实体法替换**：配置路径从 `claude-for-legal` 改为 `claude-for-legal-cn`；事项类型清单换为中国个保插件语境（PIIA、委托处理协议审查、个人权利请求、监管问询、数据出境路径审查、数据安全事件）；覆盖示例换为中国法语境（境内存储、约定适用外国法冲突）；术语「事项/委托业务」代替「matter」，「利益冲突检查」代替「conflicts check」。
