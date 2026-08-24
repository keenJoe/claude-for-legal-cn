---
name: matter-workspace
description: >
  管理事项工作区 —— 新建、列出、切换、关闭或脱离到执业级。触发场景：多客户执业者
  需要新建一个事项、切换活动事项、列出事项、归档事项、脱离到执业级上下文，
  或另一技能需要知道当前工作在哪个事项。事项工作区=案件/交易文件夹。
argument-hint: "<new | list | switch | close | none> [简称]"
---

# /matter-workspace

律师在多客户、多事项间工作。一个事项工作区把一个客户或一次业务的上下文与其他事项隔开。本命令管理这些工作区。

## 子命令

- `/commercial-legal-cn:matter-workspace new <简称>` —— 新建一个事项工作区，做一轮短访谈，写入 `matter.md`
- `/commercial-legal-cn:matter-workspace list` —— 列出事项，标状态与活动标记
- `/commercial-legal-cn:matter-workspace switch <简称>` —— 设为活动事项
- `/commercial-legal-cn:matter-workspace close <简称>` —— 归档事项（移到 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/matters/_archived/`，绝不删除）
- `/commercial-legal-cn:matter-workspace none` —— 脱离活动事项，仅在执业级工作

## 说明

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 章节已配置。若 `Enabled` 为 `✗`，告诉用户：「事项工作区未开启 —— 你的档案配置为单客户公司法务，插件自动使用执业级上下文。如果你实际是跨客户执业（律所），重新运行 `/commercial-legal-cn:cold-start-interview --redo` 并选择律所设置。否则，你根本不需要 `/matter-workspace`。」不报错 —— 关闭状态对公司法务用户是正常的。
2. 使用下方子命令逻辑。
3. 按 `$ARGUMENTS` 的第一个 token 分派：
   - `new` → 跑进件访谈，写入 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/matters/<简称>/matter.md`，初始化 `history.md` 和 `notes.md`。
   - `list` → 枚举 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/matters/*/matter.md`，打印表格，标记活动事项。
   - `switch` → 更新执业级 CLAUDE.md 里的 `Active matter:` 行。
   - `close` → 把 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/matters/<简称>/` 移到 `matters/_archived/<简称>/`，在 `history.md` 记录关闭日期。
   - `none` → 把 `Active matter:` 设为 `none —— 仅执业级上下文`。
4. 展示改动并请用户确认再写入。

## 注意

- 除非执业级 CLAUDE.md 中 `Cross-matter context` 为 `on`，本技能绝不跨事项读取文件。
- 归档不是删除 —— 关闭的事项仍可读，供保留/利益冲突查询用。
- 简称用小写加连字符。若在归档与活动之间简称重复，归档的保留在 `_archived/<简称>/`。

---

多客户律师（律所 —— 单独执业、中小所、大所）跨多个事项工作。一个事项的上下文不得泄漏到另一个。本技能是那层薄薄的文件管理，保证这一点。

**默认关闭。** 公司法务用户永不看到本技能 —— 他们只在执业级运行。事项工作区在 cold-start 时对律所用户开启，或通过编辑执业级 CLAUDE.md 的 `## 事项工作区` 开启。若 `Enabled` 为 `✗`，本技能不运行；上面的工作流解释关闭态并建议律所用户运行 `--redo`。

## 存储布局

所有事项数据在：

```
~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/
├── CLAUDE.md                       # 执业级执业档案
└── matters/
    ├── <简称>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖
    │   ├── history.md              # 按日期的事件、决策、稿件、审查记录
    │   ├── notes.md                # 自由笔记
    │   └── outputs/                # 本事项的技能输出（可选子文件夹）
    └── _archived/
        └── <简称>/                 # 已关闭事项 —— 可读、非活动
```

简称用小写加连字符。例如：`acme-msa-2026`、`zenith-renewal`、`vendor-xyz-nda`。

## 活动事项在执业级 CLAUDE.md

执业级 CLAUDE.md `## 事项工作区` 里的 `Active matter:` 行是唯一真相源。切换事项就是编辑这行。没有另外的状态文件。

## 子命令逻辑

### `new <简称>`

1. 确认 `matters/<简称>/` 或 `matters/_archived/<简称>/` 不存在同名。重复就请用户换个简称。
2. 进件访谈：
   - **客户**（我们代表的一方，或公司内部业务方）
   - **相对方**（另一方 —— 可以多个）
   - **事项类型**（读插件执业档案的常用类型；商务合同用：供应商合同 | 客户合同 | 保密协议 | SaaS 订阅 | 补充协议 | 续约 | 其他）
   - **保密等级**（标准 | 增强 | 隔离小组 —— 增强触发跨事项场景下额外谨慎）
   - **关键事实**（2-5 句：事项讲什么、当事方是谁、利害何在）
   - **本事项覆盖执业档案 playbook 的地方**（如「客户要求责任上限 24 个月，而非我们标准 12 个月」「相对方是战略合作方 —— 语气须维护关系」）
   - **关联事项**（简称清单）
3. 用下方模板写 `matters/<简称>/matter.md`。
4. 初始化 `matters/<简称>/history.md`，写一条「开立」条目。
5. 建空文件 `matters/<简称>/notes.md`。
6. **不自动切换**到新事项。问：「要立刻切到 `<简称>` 吗？（`/commercial-legal-cn:matter-workspace switch <简称>`）」

### `list`

枚举 `matters/*/matter.md`。读每份文件的前几行提取状态。打印表格：

| 简称 | 客户 | 事项类型 | 状态 | 开立日 | 活动 |
|---|---|---|---|---|---|

活动事项用 `*` 标记。存在归档就单列「已归档」小节。

### `switch <简称>`

1. 确认 `matters/<简称>/matter.md` 存在。不存在就提议 `/commercial-legal-cn:matter-workspace new <简称>`。
2. 把执业级 CLAUDE.md 的 `Active matter:` 行编辑为 `Active matter: <简称>`。
3. 展示 matter.md 摘要给用户，让其确认切对了事项。

### `close <简称>`

1. 确认 `matters/<简称>/` 存在。
2. 在 `matters/<简称>/history.md` 追加一条「关闭」条目，日期为今天。
3. 移动 `matters/<简称>/` → `matters/_archived/<简称>/`。
4. 若被关闭的事项曾是活动事项，把 `Active matter:` 设为 `none —— 仅执业级上下文`。

### `none`

把执业级 CLAUDE.md 的 `Active matter:` 设为 `none —— 仅执业级上下文`。请用户确认。

## `matter.md` 模板

```markdown
[草稿头 —— 按档案 ## 输出头部]

# 事项：[客户] —— [简述]

**简称：** [简称]
**开立日：** [YYYY-MM-DD]
**状态：** active
**保密等级：** [标准 / 增强 / 隔离小组]

---

## 当事方

**客户：** [名称]
**相对方：** [名称]

## 事项类型

[供应商合同 | 客户合同 | 保密协议 | SaaS 订阅 | 补充协议 | 续约 | 其他 —— 一行理由]

## 关键事实

[2-5 句。事项讲什么。当事方是谁。利害何在。它与默认 playbook 有何不同。]

## 事项级覆盖

*任何仅对本事项适用、不同于执业级 playbook 的立场。*

- [例：「责任上限：客户要求 24 个月，而非我们标准 12 个月。」]
- [例：「语气：维护关系 —— 相对方是战略合作方。」]
- [例：「适用法律：必须约定英国法，而非我方所在地。」]

## 关联事项

- [简称 —— 一行为何关联]

## 保密说明

[若为增强或隔离小组，说明原因。谁可看事项文件。即使跨事项上下文全局开启，本事项是否允许被跨读。]
```

## `history.md` 初始

```markdown
# 历史：[客户] —— [简述]

追加型事件日志。最新在上。

---

## [YYYY-MM-DD] —— 事项开立

进件完成。简称：`[简称]`。状态：active。
[任何值得记录但不属于 matter.md 的初始上下文 —— 例如「因收到 [相对方] 的合同草稿而开立」。]
```

## 跨事项上下文

执业级 CLAUDE.md 有一个 `Cross-matter context:` 开关。默认 `off` 时，一个在事项 A 中工作的技能**绝不读**任何其他 `matters/B/` 里的文件。这就是这个设置存在的保密保证。

`on` 时，技能可跨事项文件夹读取，但仅当用户明确要求（例如「对比我们过去五个供应商合同里的责任上限立场」）。即使 `on`，默认也只加载活动事项，除非用户明确要求跨事项视图。

## 本 skill 不做的事

- **不做利益冲突检查。** 冲突是律师/律所的活；进件采集用户所声明的内容。
- **不做保留强制。** 关闭是归档，不是删除。保留策略在本技能范围之外。
- **不自动路由输出。** 实质技能决定写在哪；本技能告诉它**哪个文件夹活动**，不告诉它写什么。
- **不决定跨事项是否合适。** 它读开关，服从。

## 质量自检（本技能转换说明）

- **A 级直转：** 五个子命令逻辑（new / list / switch / close / none）、存储布局、活动事项单一真相源、matter.md 与 history.md 模板、跨事项上下文默认关闭 —— 方法论层原样保留。
- **B 级大改：** 默认关闭态的说明改为公司法务 vs 律所语境；事项类型清单换为中国合同实务（供应商合同 / 客户合同 / 保密协议 / SaaS 订阅 / 补充协议 / 续约）；配置路径换为 claude-for-legal-cn。
- **C 级删除：** privilege 头部替换为草稿头。
- **D 级新增：** 无。
