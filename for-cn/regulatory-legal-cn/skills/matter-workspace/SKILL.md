---
name: matter-workspace
description: >
  管理事项工作区 —— 新建 / 列表 / 切换 / 关闭 / 从当前事项分离（回到执业级）。
  触发场景：跨多个客户或事项工作、需要把一个案件 / 项目 / 立法跟踪与另一个隔离开、
  或某个实质技能需要知道当前处于哪个事项内。中国语境下「事项」= 案件 / 交易 / 立法跟踪 /
  监管应对项目。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

法务与律师日常同时跟进多个客户 / 项目。事项工作区把一个客户或项目的上下文与其他项目分开保存。本技能管理这些工作区。

## 子命令

- `/regulatory-legal-cn:matter-workspace new <slug>` —— 新建一个事项工作区，做一段简短的立项访谈，写入 `matter.md`
- `/regulatory-legal-cn:matter-workspace list` —— 列出所有事项、状态、以及当前活动事项
- `/regulatory-legal-cn:matter-workspace switch <slug>` —— 切换活动事项
- `/regulatory-legal-cn:matter-workspace close <slug>` —— 归档某个事项（移动到 `~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/matters/_archived/`，不删除）
- `/regulatory-legal-cn:matter-workspace none` —— 从当前事项分离，回到执业级上下文

## 执行逻辑

1. 读取 `~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/CLAUDE.md` —— 确认 `## 事项工作区` 一节已配置。若 `启用` 为 `✗`，告诉用户：「事项工作区未启用 —— 你在冷启动时选择的是公司法务，只有一家『客户』（本公司），插件默认使用执业级上下文。若你实际在多家客户 / 多个立法跟踪项目间切换（如律所或行业协会法务），运行 `/regulatory-legal-cn:cold-start-interview --redo` 并选择律所或多客户设置。否则本命令用不上。」不要报错 —— 「未启用」是公司法务用户的**预期状态**。
2. 使用下文的文件管理逻辑。
3. 按 `$ARGUMENTS` 首个 token 分发：
   - `new` → 运行立项访谈，写入 `~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/matters/<slug>/matter.md`，同时创建 `history.md`、`notes.md`。
   - `list` → 遍历 `~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/matters/*/matter.md`，输出表格，标注当前活动事项。
   - `switch` → 更新执业级 CLAUDE.md 中 `Active matter:` 一行。
   - `close` → 把 `matters/<slug>/` 移到 `matters/_archived/<slug>/`，在 `history.md` 追加关闭日期。
   - `none` → 把 `Active matter:` 设为 `none —— 仅执业级上下文`。
4. 展示改动内容，写档前先确认。

## 注意

- 除非执业级 CLAUDE.md 中 `跨事项上下文` 为 `on`，本技能**从不**读取其他事项的文件。
- 归档 ≠ 删除。已关闭事项保留可读，用于档案保存与利益冲突排查。
- slug 用小写 + 短横线。若同一 slug 在归档区和活动区都出现过，已归档者保留在 `_archived/<slug>/`。

---

多客户 / 多事项工作方式（律所、独立执业、行业协会法务）下会同时跟进多个事项。一个事项的上下文**不得**渗入另一个。本技能是让这一点为真的薄薄一层文件管理。

**默认关闭。** 公司法务不见此层 —— 他们只在执业级运行。冷启动为律所 / 多客户模式的用户开启事项工作区，或者通过编辑执业级 CLAUDE.md 的 `## 事项工作区` 一节手工开启。若 `启用` 为 `✗`，本技能不做实事 —— 只是解释状态，并建议 `--redo` 给真正需要事项隔离的用户。

## 存储布局

所有事项数据存放于：

```
~/.claude/plugins/config/claude-for-legal-cn/regulatory-legal-cn/
├── CLAUDE.md                       # 执业级档案
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、对方、事项类型、关键事实、事项级偏差
    │   ├── history.md              # 按日期的事件、决策、稿件、审查日志
    │   ├── notes.md                # 工作笔记
    │   └── outputs/                # 本事项的技能输出（可选子目录）
    └── _archived/
        └── <slug>/                 # 已关闭事项 —— 可读，非活动
```

slug 全小写 + 短横线。例如：`sino-datacomply-2026`、`abc-supplier-audit`、`draft-comment-on-cac-rule`。

## 「活动事项」写在执业级 CLAUDE.md 中

执业级 CLAUDE.md 里 `## 事项工作区` 一节下 `Active matter:` 那一行是**唯一权威**。切换事项就是编辑这一行。不额外开状态文件。

## 各子命令逻辑

### `new <slug>`

1. 确认 `matters/<slug>/` 或 `matters/_archived/<slug>/` 中都没有同名 slug。若已存在，请用户换一个 slug。
2. 立项访谈：
   - **客户**（我方代理的一方，或公司法务下的内部业务单元）
   - **对方**（相对方 —— 可以多个）
   - **事项类型**（对本插件而言的典型类别：立法跟踪 | 征求意见回应 | 监管缺口整改 | 监管问询应对 | 执法应对 | 长期专项跟踪 | 其他）
   - **保密等级**（标准 / 加严 / 净室 —— 加严意味着在跨事项设置下要更小心）
   - **关键事实**（2-5 句：事项主题、利益相关方、事关什么、与默认 playbook 的差异）
   - **事项级偏差**（对执业级 playbook 的偏离项，例如「本事项客户要求 24 个月责任限额上限」「对方是战略合作伙伴，语气偏向维系关系」）
   - **关联事项**（关联事项的 slug）
3. 用下文模板写 `matters/<slug>/matter.md`。
4. 在 `matters/<slug>/history.md` 写一条「已立项」入口。
5. 建空 `matters/<slug>/notes.md`。
6. **不**自动切换到新事项。问：「要切换到 `<slug>` 吗？（`/regulatory-legal-cn:matter-workspace switch <slug>`）」

### `list`

遍历 `matters/*/matter.md`，读取每份文件的前几行提取状态。输出表：

| slug | 客户 | 事项类型 | 状态 | 立项日 | 活动 |
|---|---|---|---|---|---|

活动事项在「活动」列标 `*`。若有 `_archived/*`，单独在「已归档」标题下列出。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。若不存在，提示 `/regulatory-legal-cn:matter-workspace new <slug>`。
2. 编辑执业级 CLAUDE.md 中 `Active matter:` 为 `Active matter: <slug>`。
3. 展示该 matter.md 的摘要，供用户确认切到了正确的事项。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 向 `matters/<slug>/history.md` 追加一条「已关闭」入口，日期为今日。
3. 移动 `matters/<slug>/` → `matters/_archived/<slug>/`。
4. 若被关闭者恰为当前活动事项，将 `Active matter:` 设为 `none —— 仅执业级上下文`。

### `none`

把执业级 CLAUDE.md 中 `Active matter:` 设为 `none —— 仅执业级上下文`。写档前先向用户确认。

## `matter.md` 模板

```markdown
[输出头部 —— 见执业级 CLAUDE.md ## 输出 一节；因角色不同而不同，参见执业级 CLAUDE.md 中 `## 谁在用`]

# 事项：[客户] —— [简短描述]

**slug：** [slug]
**立项日：** [YYYY-MM-DD]
**状态：** 活动
**保密等级：** [标准 / 加严 / 净室]

---

## 参与方

**客户：** [名称]
**对方：** [名称（可多个）]

## 事项类型

[立法跟踪 | 征求意见回应 | 监管缺口整改 | 监管问询应对 | 执法应对 | 长期专项跟踪 | 其他 —— 附一句理由]

## 关键事实

[2-5 句。本事项是关于什么。利益相关方是谁。事关什么。与默认 playbook 的差异。]

## 事项级偏差

*本事项相对执业级 playbook 的偏离项，仅本事项适用。*

- [例：「责任限额上限：本客户要求 24 个月，非本所标准 12 个月」]
- [例：「语气：维系关系 —— 对方是战略合作伙伴」]
- [例：「适用法律：必须约定英国法，非中国法」]

## 关联事项

- [slug —— 一行说明为何关联]

## 保密说明

[若为加严 / 净室，说明原因。谁可以看事项文件。即便跨事项上下文全局为 on 时，本事项的跨事项访问是否允许。]
```

## `history.md` 初始化

```markdown
# 历史：[客户] —— [简短描述]

只追加式事件日志。最新在上。

---

## [YYYY-MM-DD] —— 事项已立项

立项完成。slug：`[slug]`。状态：活动。
[matter.md 之外值得保留的初始上下文 —— 例如「因对方发来 MSA 草案而立项」。]
```

## 跨事项上下文

执业级 CLAUDE.md 中有一项 `跨事项上下文:` 开关。默认 `off`：某事项 A 内工作的技能**绝不读**任何其他事项 B 的文件。这是这个设置存在的保密价值。

开关 `on` 时：技能只在用户明确要求跨事项时才跨（例如「盘点过去五个供应商合同里我们的责任限额立场」）。即便 `on`，默认仍是只读活动事项 —— 用户明确请求跨事项才跨。

## 本技能不做的事

- **不做利益冲突排查。** 利益冲突是执业者 / 律所的义务；立项只记录用户声明的信息。
- **不执行归档 / 销毁保存期。** 关闭 = 归档，不删除。保存期政策不在范围内。
- **不代替实质技能决定输出位置。** 是本技能告诉实质技能「当前活动事项在哪里」；具体写什么由实质技能决定。
- **不判断跨事项访问是否合适。** 只读开关，遵守开关。

## 转换决策自检

- **分级：** A 直接转化 —— 完整保留事项工作区的架构（子命令、存储布局、活动事项标识、跨事项开关）。
- **主要变化：** 事项类型改为中国监管实务的典型分类（立法跟踪 / 征求意见回应 / 监管缺口整改 / 监管问询应对 / 执法应对 / 长期专项跟踪）；示例 slug 改为中国典型场景；「in-house」直译为「公司法务」，说明该角色下默认关闭事项工作区的语义与英美一致。
