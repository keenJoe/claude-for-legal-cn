---
name: matter-workspace
description: >
  为多委托方/多案件执业管理案件工作区 —— 新建、列表、切换、结案、脱离
  当前活跃案件。触发场景：用户要新建案件工作区、切换活跃案件、列案件、
  归档已结案、或只在执业级上下文工作。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

律师和法务在多个委托方和案件间切换。**案件工作区**（中国实务通常叫「案件卷宗」或「事项文件夹」）把一个委托方或一个案件的上下文与其他案件隔离。本命令管理这些工作区。

## 子命令

- `/litigation-legal-cn:matter-workspace new <slug>` —— 新建案件工作区，跑简短立案，写 `matter.md`
- `/litigation-legal-cn:matter-workspace list` —— 列出案件，显示状态和活跃标记
- `/litigation-legal-cn:matter-workspace switch <slug>` —— 设活跃案件
- `/litigation-legal-cn:matter-workspace close <slug>` —— 归档案件（移至 `matters/_archived/`，不删除）
- `/litigation-legal-cn:matter-workspace none` —— 脱离活跃案件，仅执业级上下文

注：`/litigation-legal-cn:matter-briefing [slug]`（不带子命令）是独立命令，生成单案简报 —— 用于组合视角。案件工作区管理在这里。

## 指令

1. 读 `CLAUDE.md` —— 确认 `## 事项工作区（案件文件夹）` 章节已配置。若 `Enabled` 为 `✗`，告诉用户：「案件工作区未启用 —— 你的配置是只服务单一委托方的公司法务，插件自动使用执业级上下文。若你实际在多委托方间工作，重跑 `/litigation-legal-cn:cold-start-interview --redo` 选律所/独立执业。否则不用 `/matter-workspace`。」不报错 —— 禁用状态对公司法务是预期的。
2. 按下方工作流。
3. 分派 `$ARGUMENTS` 首个 token：
   - `new` → 跑立案短访谈，写 `matters/<slug>/matter.md`，种入 `history.md`、`notes.md`。
   - `list` → 枚举 `matters/*/matter.md`，读前几行提取状态，输出表，标活跃案件。
   - `switch` → 更新执业级 CLAUDE.md 的 `Active matter:` 行。
   - `close` → 把 `matters/<slug>/` 移至 `matters/_archived/<slug>/`，在 `history.md` 记结案日。
   - `none` → 设 `Active matter:` 为 `无 —— 仅执业级上下文`。
4. 写入前展示改动，让用户确认。

## 说明

- 本 skill 绝不跨案件读取，除非执业级 CLAUDE.md 中 `Cross-matter context` 为 `on`。
- 归档不是删除 —— 已结案件保留可读，用于留档、利益冲突查询、经验参照。
- slug 用小写+连字符。若归档与活跃 slug 重名，归档者置于 `_archived/<slug>/`。

---

# 案件工作区

律所律师、独立执业律师在多案件间切换。一个案件的上下文不得泄漏到另一个。本 skill 是让这一点成立的薄文件管理层。

**默认状态：关闭。** 公司法务通常一家公司多个案件都在同一组合里，直接用执业级；律所/独立执业则每个委托方/案件独立。冷启动访谈时会根据「执业角色」自动配置。

## 存储布局

案件数据统一在：

```
~/.claude/plugins/config/claude-for-legal-cn/litigation-legal-cn/
├── CLAUDE.md                          # 执业级档案
└── matters/
    ├── _log.yaml                      # 全部案件结构化台账
    ├── <slug>/
    │   ├── matter.md                  # 委托方、对方、案由、关键事实、覆盖项
    │   ├── history.md                 # 事件流水
    │   ├── notes.md                   # 自由笔记
    │   ├── chronology.md              # chronology 技能产出
    │   ├── evidence/                  # 证据材料
    │   ├── pleadings/                 # 起诉状/答辩状/代理词
    │   └── outputs/                   # 其他技能产出
    └── _archived/
        └── <slug>/                    # 已结案 —— 可读但不活跃
```

slug 小写+连字符。示例：`acme-mai-2026`（对某某公司买卖合同案）、`zhang-wu-laodong-2026`、`ip-shangbiao-yq-2026`。

## 活跃案件在执业级 CLAUDE.md 里

执业级 CLAUDE.md 的 `## 事项工作区（案件文件夹）` 章节里 `Active matter:` 是单一真相源。切换即编辑该行。无独立状态文件。

## 子命令逻辑

### `new <slug>`

1. 确认 slug 不在 `matters/<slug>/` 或 `matters/_archived/<slug>/`。冲突就让用户改一个。
2. 立案短访谈：
   - **委托方**（我们代理的一方，或公司内业务方）
   - **对方当事人**（可能多个）
   - **案件类型**（合同 / 劳动 / 公司股权 / IP / 涉外 / 侵权 / 婚姻家事 / 刑事附带民事 / 其他）
   - **诉讼阶段**（诉前评估 / 诉前保全 / 立案 / 一审 / 二审 / 再审 / 执行 / 仲裁 / 调解）
   - **保密等级**（标准 / 加强 / 隔离小组 —— 加强或隔离时后续跨案件读取需额外注意）
   - **关键事实**（2–5 句：案件说的是什么、涉及谁、争议焦点、与默认 playbook 有何不同）
   - **本案覆盖执业级 playbook 的项**（例如「本案立场为原告方（覆盖默认被告方）」「本案适用香港法（覆盖内地法框架）」）
   - **关联案件**（关联案件 slug）
3. 用下方模板写 `matters/<slug>/matter.md`。
4. 种入 `matters/<slug>/history.md` 单条「立案」条目。
5. 建空 `matters/<slug>/notes.md`。
6. **不自动切换**。问：「切换到 `<slug>`？（`/litigation-legal-cn:matter-workspace switch <slug>`）」

### `list`

枚举 `matters/*/matter.md`。读前几行提取状态。输出表：

| Slug | 委托方 | 案件类型 | 状态 | 立案日 | 活跃 |
|---|---|---|---|---|---|

用 `*` 标记当前活跃案件。归档案件放在单独的「已归档」标题下（如有）。

### `switch <slug>`

1. 确认 `matters/<slug>/matter.md` 存在。若无，提示 `/litigation-legal-cn:matter-workspace new <slug>`。
2. 编辑执业级 CLAUDE.md 中的 `Active matter:` 行为 `Active matter: <slug>`。
3. 展示 matter.md 概要，让用户确认在正确案件上。

### `close <slug>`

1. 确认 `matters/<slug>/` 存在。
2. 追加「结案」条目到 `history.md`。
3. 移动 `matters/<slug>/` → `matters/_archived/<slug>/`。
4. 若结案案件正是活跃案件，设 `Active matter:` 为 `无 —— 仅执业级上下文`。

*注意：这里的「归档」是工作区层面的移动。案件正式结案的实体动作（写入 outcome、更新 `_log.yaml` status: 已结案）走 `/litigation-legal-cn:matter-close`。两个动作可先后进行。*

### `none`

设 `Active matter:` 为 `无 —— 仅执业级上下文`。用户确认。

## `matter.md` 模板

```markdown
本文件由 AI 辅助生成，是待律师审核的工作草稿，不构成法律意见。
审查人：[姓名]  日期：[立案日]  已读范围：[本次访谈捕捉]

# 案件：[委托方] —— [简述]

**Slug：** [slug]
**立案日：** [YYYY-MM-DD]
**状态：** 活跃
**保密等级：** [标准 / 加强 / 隔离小组]

---

## 当事人

**委托方：** [名称]
**对方：** [名称 —— 可多个]
**对方代理律师：** [律所+律师，若已知]

## 案件类型与阶段

[合同 / 劳动 / 公司股权 / IP / 涉外 / 侵权 —— 附一句案由说明]
[诉前 / 立案 / 一审 / 二审 / 执行]

## 关键事实

[2–5 句。案件是什么。谁是相关方。争议焦点。与默认 playbook 有何不同。]

## 本案覆盖项

*偏离执业级 playbook 的、仅适用于本案的项。*

- [例如：「本案立场：原告方（执业级默认为被告方）」]
- [例如：「适用法律：香港法（执业级默认为内地法）」]
- [例如：「保全立场：不申请（对方是长期合作商户，保全影响关系）」]

## 关联案件

- [slug —— 一行说明为何关联]

## 保密说明

[若加强或隔离，说明为何。谁可看案件文件。跨案件上下文即便全局开启，本案是否仍不可跨。]
```

## `history.md` 种子

```markdown
# 历史：[委托方] —— [简述]

追加式事件日志。最新在上。

---

## [YYYY-MM-DD] —— 案件立案

立案访谈完成。Slug：`[slug]`。状态：活跃。
[任何值得留存但 matter.md 未捕捉的初始上下文 —— 例如「因对方于 2026-03-15 送达律师函而立案」。]
```

## 跨案件上下文

执业级 CLAUDE.md 有 `Cross-matter context:` 开关。为 `off`（默认）时，在案件 A 中工作的 skill **绝不读取** 任何其他 `matters/B/` 中的文件。这是本设置存在的保密保障。

为 `on` 时，skill 只在用户明确要求时跨案件读取（例如「对比过去五个买卖合同违约案的举证策略」）。即便 `on`，默认也只加载活跃案件，除非用户请求跨案件视图。

## 转换决策

- 分级：**A 直接转化**。原版结构（存储布局、子命令、跨案件保密）保留；实体层：案件类型换为中国常见争议类型（合同/劳动/公司股权/IP/涉外/侵权/婚姻/刑附民）；诉讼阶段术语替换为中国审级；引用「clean team」保留（涉外/大型案件仍会用到，但常用中文替代表述为「隔离小组」）；律师保密引用改为律师法第 38 条。

## 这个 skill 不做的事

- **跑利益冲突检查。** 利益冲突是律所/律师自身职责；立案访谈捕捉用户申报。
- **执行保留期。** 结案归档，不删除。保留策略超出范围。
- **自动路由输出。** 具体 skill 决定写哪里；本 skill 只告诉它*哪个文件夹*活跃，不决定放什么。
- **决定跨案件是否合适。** 只读开关并遵守。
