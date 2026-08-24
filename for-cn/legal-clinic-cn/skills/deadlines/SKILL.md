---
name: deadlines
description: >
  跟踪案件期限 —— 加、跨案汇总、更新、完结、关闭。在可配置阈值预警（默认 14/7/3/1 日）；
  过期项直到解决前一直标记。这是诊所工作量的作业记录。特别关注**诉讼时效 3 年**（民法典第 188 条）与
  **劳动仲裁时效 1 年**（劳动争议调解仲裁法第 27 条），以及**劳动争议仲裁前置**。
  触发场景：加期限、看这周到期、要期限报告、更新案件期限。
argument-hint: "[--add | --report（默认）| --update [id] | --complete [id] | --close [id] | --horizon=N]"
---

# /deadlines

1. 读 `~/.claude/plugins/config/claude-for-legal-cn/legal-clinic-cn/CLAUDE.md` → 办案地、纠纷类型、预警节奏。
2. 按下方工作流。
3. 按 flag 路由：
   - `--add`：收集案件、类型、说明、到期日、来源、责任人。写入 `~/.claude/plugins/config/claude-for-legal-cn/legal-clinic-cn/deadlines.yaml`。先查重复。
   - `--report`（默认）：跨案汇总 —— 已过期、未来 3 日、未来 7 日、未来 14 日；按责任人；按纠纷类型；未分配标记。
   - `--update [id]`：改字段；日志追加一条带日期的注。
   - `--complete [id]`：标已完成；与学生确认活确实提交 / 送达。
   - `--close [id]`：不完成关闭；理由写入 notes。
4. 任何写入前确认。

---

# 期限

## 目的

诊所最大的作业风险是漏一个期限。学生同时办多个案件，兼顾学业，每学期换一批。只存在个别学生脑子里的期限，交接时会掉、期末周会忘、
学生突然退课时会没人管。本 skill 是**中央作业记录**。

指导老师承担期限漏掉的责任。本 skill 按这个 stakes 校准：预警提前触发、过期项在显式解决前一直可见、交接（`/semester-handoff`）把期限清单转给下一位学生。

## 加载上下文

- `~/.claude/plugins/config/claude-for-legal-cn/legal-clinic-cn/CLAUDE.md` → 办案地、纠纷类型、预警天数（默认 14/7/3/1）、指导老师
- `~/.claude/plugins/config/claude-for-legal-cn/legal-clinic-cn/deadlines.yaml` —— 台账

**办案地假设。** 期限计算与预警阈值按 CLAUDE.md 里设定的办案地。中国民事诉讼答辩期、举证期限、上诉期、送达期，以及劳动仲裁的立案、举证、开庭窗口，在不同法院/仲裁委的实际操作可能有微差。若跨省或涉及专门法院（如互联网法院、金融法院），与老师核对适用规则再依赖。

## 模式

flag：`--add | --report | --update | --complete | --close`（默认：report）

### `--add` —— 记一条新期限

**输入：**
- 案件 ID + 名（哪个案件）
- 纠纷类型
- 类型（`filing` 提交 / `hearing` 开庭 / `statute-of-limitations` 诉讼时效 / `arbitration-limitation` 仲裁时效 / `answer` 答辩 / `evidence` 举证 / `appeal` 上诉 / `service` 送达 / `notice` 通知 / `enforcement` 执行申请 / `other`）
- 说明 —— 一行到期什么
- 到期日（含时间与时区，若有）
- 来源 —— 期限来自哪（法院传票、仲裁委立案通知、律师函、法条例如「劳动争议调解仲裁法第 27 条」）
- 责任学生

skill 自动生成 `id`：`[案件]-[短说明]-[YYYY-MM]`。

**从其它 skill 提取：** `/client-intake` `/draft` `/status` 输出中出现期限时，应带预填字段送到本 skill。学生确认后加入。

**加入前重复检查：** 已存在同 case_id + 类型 + 到期日的条目，标疑似重复，先问再加。

**合理区间快检。** 学生输入到期日后**不计算、不核验**，但对该类型的典型区间做粗略合理检查。日期严重超出区间时提请学生复核。这是抓算错，不是替算。

**区间按办案地键入。** 从 `references/plausibility-bands/{省份代码}.md` 加载本诊所办案地的区间文件（联邦规则等价物：`cn-national.md` 始终并行加载，对应中国国家层级法律）。本插件出厂附 `references/plausibility-bands/cn-national.md`（全国通用规则，已填充）与 `references/plausibility-bands/local-template.md`（占位结构）作为起点。

**若办案地无区间文件，冷启动硬停止。** `references/plausibility-bands/{省份代码}.md` 对本诊所办案地不存在，**不**默默无区间跑。冷启动时告知老师：

> 「我没有 [省份] 的期限合理区间 —— 你诊所办案地的区间文件不在出厂附带的参考文件里。我仍可加、报、改、完结、关闭期限，但**不能对典型区间做合理检查**。做区间文件的方法：把 `references/plausibility-bands/local-template.md` 复制一份，为你诊所常见的期限类型各填一行（典型区间、触发事件处理、计算规则、简短引用），保存为 `references/plausibility-bands/{省份代码}.md`，重跑 `/legal-clinic-cn:deadlines`。在此之前，我接受的每条期限都带 `warnings: no-plausibility-band`，你审阅时应把日期视为未检。」

不要对不同省份回退到 cn-national 里的地方性内容。悄悄把上海的区间套到深圳诊所 —— 这个失败点就是本 fix 的对象。

**合理检查逻辑：**
1. 加载办案地区间（+ `cn-national.md`）。
2. 学生输入 `due:` 后，对该 `type:` 用触发事件日 + 典型区间比。
3. 在区间内 → 写入，什么都不说 —— 区间是抓错的，不是给对了鼓掌的。
4. 超出实质余量 → 写入前停下：
   > 你输入的日期落在 [办案地] [type] 的典型区间之外。[类型] 从 [触发事件] 起通常约 [区间]。你输入 [日期]，距 [触发事件] [N] 日。请对照 [区间文件引用的规则] 与计算规则复核。若你的计算正确（本地特殊规则、非典型触发事件、时效中止/延展、当事人放弃），确认后我按现值加入。否则重算再 `/deadlines --add`。
5. 该 `type:` 无已知区间（非常规、非标准期限）→ 不做合理检查，写入，在 `warnings:` 记「无合理区间」。
6. 办案地区间文件整体缺失 → 冷启动硬停止如上；稳态下（老师承认缺口继续），每条写入带 `warnings: no-plausibility-band`。

**skill 不计算。** 学生因还没算把 `[待核]` 填入 `due:`，写入 `due: [待核]` —— 合理区间仅在学生给出具体日期时生效。计算留给学生与老师。

### `--report`（默认）—— 跨案汇总

读 `~/.claude/plugins/config/claude-for-legal-cn/legal-clinic-cn/deadlines.yaml`。产出：

```markdown
# 期限报告 —— [今天]

**活跃期限：** [N]
**过期：** [N] ⚠️
**本周（未来 7 日）：** [N]

---

## ⚠️ 过期（需立即处理）

| ID | 案件 | 类型 | 到期 | 责任人 | 过期天数 |
|---|---|---|---|---|---|

## 🔴 今日/未来 3 日

| ID | 案件 | 类型 | 到期 | 责任人 |
|---|---|---|---|---|

## 🟡 未来 4-7 日

| ID | 案件 | 类型 | 到期 | 责任人 |
|---|---|---|---|---|

## 🟢 未来 8-14 日

[列表]

## 14 日以外

[仅计数 —— 用 `/deadlines --report --horizon=30` 展开]

---

## 按学生（工作量分布）

| 学生 | 过期 | 未来 7 日 | 未来 14 日 | 活跃总数 |
|---|---|---|---|---|

## 按纠纷类型

[同表，按类型分组]

## 未分配期限

[任何活跃期限无 owner_student 的标出]
```

### `--update` —— 改一条期限

常见更新：到期日变化（法院/仲裁委延期）、责任人变（重新分配）、加注。

每次更新在条目内联写一条带日期的注；条目里能看到历史。

### `--complete` —— 标已完成

- 状态 → `completed`，completed_date → 今天
- 与学生确认实际工作已完成并提交/送达
- 从活跃报告移除但仍留在 yaml 中

### `--close` —— 不完成关闭

期限不再适用（和解、撤回、受援人退出、案件转介后由外部律师承办）。要求 `notes:` 写理由。

## 预警节奏

按 CLAUDE.md 预警天数。默认 14、7、3、1。

预警不自动弹出 —— 本插件无定时 / agent 行为。但每次 `/deadlines`（或 `/status` 走本 skill 检查期限）都会把打到预警阈值的项拉到前面。

期限过到期日仍未标完成的，转为 `status: overdue`，在每份报告里一直保留到显式解决。过期期限**不**自动关闭。

## 集成

- **`/client-intake`：** 接待中冒出时效紧迫（劳动仲裁时效将届、诉讼时效将届、开庭日期已定），提议 `/deadlines --add`，字段预填。
- **`/draft`：** 起草提交材料涉及期限（答辩期、上诉期）时提议加入。
- **`/status`：** status skill 读 `deadlines.yaml` 中相关案件的期限并纳入输出。
- **`/semester-handoff`：** 读 deadlines.yaml 找出离校学生名下的活跃期限；每份交接备忘把期限带到下一学生。
- **`/supervisor-review-queue`（若启用正式队列）：** 临近截止的期限在审核队列中优先。

## 本 skill 不做的事

- **不从触发事件计算期限。** 若诉状于今日送达，答辩期是 15 日（民事诉讼法第 128 条 `[待核验条文号]`），skill 不做这个算术 —— 学生依规则算完把结果日期录入。（自动算会带来 skill 不该承担的责任；规则随办案地、诉讼类型而异；劳动仲裁另有一套。）
- **不提交或送达任何材料。** skill 跟日期；提交/送达在插件外。
- **不自动通知。** 无定时通知。报告在调用时显示预警；不推送。老师可选允许后未来加。
- **不覆盖办案地规则。** 学生录了与办案地规则冲突的到期日，skill 不抓 —— 又一条理由：任何非常规期限用 `[核实：与办案地规则比对]` 标注。
- **不判断诉讼时效是否已过。** 时效起算点（民法典第 188 条从「知道或应当知道」起算；未定期限的从主张之日起算等）由学生与老师定；skill 只登记结论。

---

## 转换决策自检

- **A 级直转：** 5 种模式（--add/--report/--update/--complete/--close）、报告结构（过期/3天/7天/14天/按人/按类型）、预警节奏 14/7/3/1、合理区间机制（含硬停止逻辑）、集成清单。
- **B 级大改：** 期限类型词汇（filing/hearing/statute-of-limitations/discovery/cure-period → filing/hearing/statute-of-limitations/**arbitration-limitation**/answer/**evidence**/appeal/service/notice/enforcement）；区间文件路径从 `{state}.md` → `{省份代码}.md`；出厂文件从 `CA.md` + `IL.md` → `cn-national.md`（已填）+ `local-template.md`（占位）。
- **C 级重写：** 「Federal always loads」→ `cn-national.md` 承担全国统一规则（民法典时效、民诉法答辩期上诉期、劳动争议调解仲裁法时效）—— 因为中国国家统一立法多、地方差异集中在地方性法规与法院实操；不要复用 `CA.md` 的假设「地方是省份补充版」逻辑。
- **D 级新增：** 类型词汇加入 `arbitration-limitation`（劳动仲裁时效 1 年）、`enforcement`（申请执行期间 2 年）、`evidence`（举证期限）；「不判断诉讼时效是否已过」显式列入不做事项，把中国时效起算点专属复杂性向老师暴露。
