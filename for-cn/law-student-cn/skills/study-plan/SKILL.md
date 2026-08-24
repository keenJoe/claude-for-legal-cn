---
name: study-plan
description: >
  制定或更新长期法考（或期末考）学习计划 —— 分阶段、按弱项加权科目、每日训练排期，
  按 study-plan.yaml 的 session_history 自适应。触发场景：用户说「做学习计划」
  「排一下法考备考」「安排我的学习」「[某考试] 该怎么准备」。
argument-hint: "[--build | --update | --status | --cram]"
---

# /study-plan

1. 读取 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/CLAUDE.md` → 法考目标、考试类型、考试日期、弱项科目、每日目标学时、使用的培训机构。
2. 读取 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/study-plan.yaml`（若存在）。
3. 应用下面的框架。
4. 按 flag 路由：
   - `--build`（无计划时默认）：走输入闸门（考试、科目、每周学时、休息日、方法）。建阶段结构 + 前两周日排期。写入 `study-plan.yaml`。
   - `--update`（有计划时默认）：重读 `session_history`，调整科目优先级和每周学时，填充后续日排期。
   - `--status`：今天 / 本周排了什么、成绩趋势、正在掉队的科目、每科下一次排期。
   - `--cram`：强制冲刺模式 —— 80/20 高频优先、每日客观题量、最后 2-3 天减量。
5. 写入前：用文字总结计划，与学生确认。按他回答调整。
6. 每周学时始终与学生自陈的生活约束做一次现实性核验。过于野心的计划会失败。

---

## 目的

坐下学习却不知道要学什么，是几周悄然消失的方式。这个技能建计划 —— 距考试几周、每天几场训练、每周哪些科目、什么类型 —— 然后随学生真的去做而适应。这是活的计划，不是日程表导出。

它也给下游技能（bar-prep、flashcards、drill、irac）一份共享排期，让学生每次开会话都不必被问「今天想学什么」。

## 可信度纪律

计划是意见，不是教义。技能明确标出什么是估计：

- **每知识点耗时估计** 是一般指导（基于典型培训机构权重）。标为估计 —— 学生真实的节奏会不同。
- **科目权重** 从学生自陈的弱项和 `session_history` 派生。可信。
- **冲刺模式的高频知识点排序** 基于多年法考科目频率。任何「这个肯定考」的表述都要标 `[UNCERTAIN —— 过去频率不是命题预测]`。

## 加载上下文

`~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/CLAUDE.md`：
- 法考目标、卷别（客观题 / 主观题）、考试日期
- 当前课程（用于非法考场景）
- 弱项科目（客观题、主观题）
- 使用的培训机构（如瑞达 / 厚大 / 众合 / 深蓝等）
- 每日目标学时

`~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/study-plan.yaml`（若存在） —— 延续，不要覆盖。

## 流程

### 第 1 步：为什么建计划

> 我们建的是什么计划？
>
> 1. **法考**（你有一个法考目标日期）
> 2. **某门具体的期末考或一组期末**
> 3. **学期日常学习节奏**（跨科目的读书、大纲、训练）

若 (1) 法考：从档案读考试日期，确认。若未记，问客观题（通常 9 月）和主观题（通常 10 月）的准确日期，以司法部当年公告为准 `[待核验 —— 以当年公告为准]`。
若 (2) 期末考：问哪门课、什么日期、什么形式。
若 (3) 学期：问学期结束日期作为锚点。

### 第 2 步：输入 —— 一次一个，等回答

**问了就等。** 不要把全部问题堆在一个提示里再自己往前走。

- **考试日期：** 确认了？（若法考：如果档案未记，也要问准确报考公告日期。）
- **要覆盖的科目：** 法考按当年《国家统一法律职业资格考试大纲》（卷一 + 卷二 + 主观题）；期末按教学大纲。与学生确认 ——「有要加或去掉的科目吗？」
- **强项科目：** 优先级最低。仍复习，不重练。
- **弱项科目：** 优先级最高。多排训练。
- **每周可用学时：** 现实的，不是理想的。「我一周能学 30 小时」和「我可以连续 12 周每周 30 小时」是两回事。问他能实际维持多少。
- **生活现实性核验 —— 强制走。** 学生给了数字后问（一次一个，别跳过）：

  > 你说每周 [N] 小时。在我建计划之前，告诉我你这周还有什么 —— 工作（每周几小时）、家庭（子女 / 照护）、通勤、运动、社团、实习、诊所、其他。计划要贴你的生活，不是让你贴计划。做不到的计划比更轻但能做到的更糟。

  等回答。然后对照他报的负荷核对小时数：

  > 那就是 [N] 天里每天 [X] 小时，还得加上 [工作 + 家庭 + 通勤 + 其他]。按我经验这是 [现实 / 紧张 / 不可持续]。要不要在我建之前把每周目标学时调低，或者保留看看第 1 周实际怎么样？

  即使档案里已记过目标学时也别跳。档案记的是学生说的，现实性核验记的是能不能维持。若核验产出更低的数字，用更低的数字建计划，并在 `confidence_flags` 里注明调整。

  若学生拒绝分享生活情况（「就照原样建」），尊重 —— 但加一条 `confidence_flags`：「生活现实性核验被拒；计划假设每周 [N] 小时可维持。第 2 周末若坚持率低于 [X]% 再谈。」
- **偏好的学习方法：** 多选。客观题 / 主观题 / 闪卡 / 大纲 / 苏格拉底对练 / 重读。向他说会真的做的方法加权。
- **每周休息日：** 休息日重要。全周 7/7 排的计划第 3 周就崩。

### 第 2.5 步：补充 vs 替代（培训机构学员）

若 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/CLAUDE.md` → `培训机构` 名下写的是具体机构（如瑞达 / 厚大 / 众合 / 深蓝等，而非「自学」或「无」），学生已经有一份机构日历。本技能的计划必须在两种角色里挑一种 —— 它不能与机构完整课程并跑不烧学生。

问，一次一个：

> 你档案里说在跟 [机构名]。他们发布日日课程与任务表。这个计划的两种做法 —— 选一个：
>
> 1. **补充。** 机构课程是你的主线。这个计划补漏：弱项科目额外刷题、专项主观题练习、你漏掉话题的闪卡回环。我不重建机构日历；我叠加。
> 2. **替代。** 你不按机构日历走（可能是节奏不适合你的生活）。我建整份计划 —— 科目、学时、阶段、排期 —— 你不再看机构日历。
>
> 别都选。两份完整课程互相打架就是学员第 4 周崩盘的原因。

等回答。在 yaml 里记为 `prep_course_mode: supplement | replace`。

若**补充**：日排期更轻 —— 只加弱项训练和专项练习，不重复机构覆盖。在 `confidence_flags` 里标：「补充模式 —— 假设主线跟着 [机构] 走。若机构跟不上，告诉我，我们重排。」

若**替代**：按下述完整建。

若培训机构是「自学」或「无」，跳过这一步。

### 第 3 步：建排期

从今天算周数到考试。然后：

**正常模式（4 周以上）：**
- 阶段：
  - **学习阶段**（前 ~60%）：每 ~3-5 天一门科目，混合大纲 / 读法条 + 闪卡 + 少量新学内容的客观题 / 主观题。
  - **训练阶段**（次 ~30%）：客观题量增大、主观题量增大、模拟条件、全科目轮换。
  - **复习阶段**（最后 ~10%）：聚焦 `session_history` 里最薄弱的子知识点、整套模拟考、强项做轻复习。
- 按弱项加权：弱科目拿到强科目 ~2 倍的学时。
- 日日排：什么科目、什么方法、多长。给学生实际生活留松。

**冲刺模式（不到 4 周）：**
- 标出来：「距考试不到四周。冲刺模式 —— 计划把高频考点优先于全面覆盖。会留缺口。此时的取舍就这样。」
- 80/20 优先：法考里历年出题最多的科目（民法、刑法、民诉、刑诉、行政法与行政诉讼、商经法）占大头。窄科目做最小可用覆盖。
- 日排：每天客观题块（此时题量最重要）、隔天主观题练习、每周一次整套模拟。
- 最后 2-3 天减量、睡眠。别在考前一天排硬训练。真的 —— 熬夜刷到考试当天分数更低。

### 第 4 步：写出来

写入 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/study-plan.yaml`：

```yaml
plan_type: bar-exam  # or course-final or semester
exam_date: 2026-09-20  # 客观题
subjective_exam_date: 2026-10-18  # 主观题（若适用）
exam_format: 客观题+主观题  # or 客观题 / 主观题 / course-final
created: 2026-05-08
last_updated: 2026-05-08
weeks_to_exam: 20
hours_per_week: 25
days_per_week: 6
mode: normal  # or cram
prep_course: 瑞达  # or 厚大 / 众合 / 深蓝 / 自学 / 无
prep_course_mode: supplement  # or replace / N/A
phases:
  - name: 学习阶段
    start: 2026-05-08
    end: 2026-07-31
    focus: 大纲、闪卡、新学章节客观题
  - name: 训练阶段
    start: 2026-08-01
    end: 2026-09-10
    focus: 客观题量、主观题练习、模拟条件
  - name: 复习阶段
    start: 2026-09-11
    end: 2026-09-19
    focus: 薄弱子知识点复习、整套模拟
subjects:
  刑法:
    priority: high  # 弱项
    weekly_hours: 5
    methods: [objective, flashcards, subjective]
  民法:
    priority: high
    weekly_hours: 5
    methods: [objective, flashcards, subjective]
  行政法与行政诉讼法:
    priority: medium
    weekly_hours: 3
    methods: [objective, outline-review]
  # 其余科目
schedule:
  - date: 2026-05-08
    day: Thursday
    sessions:
      - subject: 刑法
        method: outline-review
        duration_min: 90
      - subject: 刑法
        method: objective
        duration_min: 60
        n_questions: 25
  - date: 2026-05-09
    day: Friday
    sessions:
      - subject: 民法
        method: flashcards
        duration_min: 45
      - subject: 民法
        method: subjective
        duration_min: 60
  # 其余
session_history: []  # 由 bar-prep / flashcards / drill / irac 完成训练时追加
```

### 第 5 步：与学生确认

**头部 —— 对话内呈现与任何单独的文字版计划文档都必需。** 摘要第一行（与保存在 YAML 旁的任何 `study-plan.md` 伙伴文件的第一行）必须是插件档案 `## 输出` 里的原文头：

```
学习笔记 —— 非法律意见
```

头部不放进 YAML 内（那是数据文件），但要在向学生展示的文字摘要和任何保存在 YAML 旁的可读计划文档顶部。不是事后免责 —— 是输出的身份。不省、不换措辞、不挪位置。

保存前用文字（不是原始 YAML）总结计划，头部放最上面：

> 学习笔记 —— 非法律意见
>
> 我建好了。到 [考试] 还有 [X] 周。每周 [Y] 小时，散在 [Z] 天。弱项（刑法、民法）拿到 2 倍学时。三阶段：[日期] 前学习阶段、[日期] 前训练阶段、最后 [N] 天复习阶段。前两周日日排好。之后按周分配 —— 你完成训练后我逐步填日排期，让计划贴你的实际进度。
>
> 感觉对吗？太狠？太轻？漏了科目？

按回答调整。然后写。

## 计划自适应

每场训练之后（经由 bar-prep-questions、flashcards、drill、irac），对应技能追加到 `session_history`：

```yaml
session_history:
  - date: 2026-05-08
    subject: 刑法
    type: bar-prep-objective
    n_questions: 10
    score: 6
    weak_subtopics: [共同犯罪, 正当防卫]
```

下次 `/law-student-cn:study-plan --update` 时（或任一技能检测到计划过时时）：
- 得分持续低的科目 `priority` 和 `weekly_hours` 上调。
- 科目内的薄弱子知识点标记给该科目下次排期。
- 若学生掉队（排的场次没出现在 history），调整：或压缩覆盖，或点出缺口并询问。
- 若学生超前，开放时间给弱项深化。

## 模式

`--build`（默认） —— 新计划
`--update` —— 重读 session_history、调整权重、填充后续日排期
`--status` —— 今天 / 本周排什么、成绩趋势、什么在掉队
`--cram` —— 强制冲刺模式（用户覆写）

## 集成

- `/law-student-cn:session <科目> <n>` 把结果写到本计划的 `session_history`。
- `/law-student-cn:bar-prep-questions` 读计划知今天排的科目。
- `/law-student-cn:flashcards` 可以 `--session <n>`，结果进计划。
- `/law-student-cn:socratic-drill` 和 `/law-student-cn:irac-practice` 训练完成也会追加。

## 这个技能不做的事

- **保证你过。** 计划是脚手架。功夫在你。
- **预测考试。** 冲刺模式用历年科目频率；高频 ≠ 保证考。
- **替代培训机构日历。** 若你在跟机构，本计划可补充 —— 别与机构并跑两条完整课程。用一条作主线。
- **安排你的生活。** 可用小时是你告诉我的。若你高估，第 2 周计划就崩。诚实报。

---

## 转换说明（质量自检）

- **分级：B 级大改。** 保留原 study-plan 整套方法论 —— 三阶段（学习 / 训练 / 复习）、按弱项加权、生活现实性核验闸门、supplement vs replace 培训机构选择、cram 模式的 80/20、YAML schema、session_history 自适应、`STUDY NOTES` 头部规则、四种 flag。
- **实体法层重写：**
  - Bar exam → 法考（客观题 9 月 + 主观题 10 月两阶段）
  - jurisdiction / exam_format → 卷别（客观题 / 主观题）
  - NCBE subject outline → 国家统一法律职业资格考试大纲
  - Commercial prep course（Themis/Barbri/Kaplan）→ 中国法考培训机构（瑞达 / 厚大 / 众合 / 深蓝等，仅示例，不作官方背书）
  - 高频科目替换：Civ Pro / Evidence / Con Law / Contracts → 民法 / 刑法 / 民诉 / 刑诉 / 行政法与行政诉讼法 / 商经法
- **D 级新增：客观题 + 主观题两日期。** YAML schema 加入 `subjective_exam_date`，反映法考的两阶段结构。
- **输出头部：** `STUDY NOTES — NOT LEGAL ADVICE` → `学习笔记 —— 非法律意见`。
- **护栏保留：** 可信度纪律（历年频率不是命题预测）、生活现实性核验、supplement vs replace 二选一、模式（build/update/status/cram）、集成路由。
- **命令前缀 & 配置路径：** 全部本地化。
- **法考日期：** 标 `[待核验 —— 以当年公告为准]`，因司法部每年发布考试公告可能微调日期。
