---
name: session
description: >
  跑一次针对某科目、固定 N 题的专项训练 —— 客观题、主观题或闪卡。追踪成绩并
  更新学习计划。触发场景：用户说「练 10 道 [科目]」「[科目] 来一套」「练 5 张 [科目] 卡」
  「/law-student-cn:session 民法 10」，或想做定题量训练并让计划自适应。
argument-hint: "<科目> <n> [--objective | --subjective | --flashcards]"
---

# /session

1. 解析 `$ARGUMENTS` —— 科目和 N。若缺失，问：
   > 什么科目，多少题？（如「民法 10」或「刑法 5 --subjective」。）
2. 读取 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/CLAUDE.md` → 考试目标、备考阶段、弱项科目。
3. 读取 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/study-plan.yaml`（若存在）。读该科目的 `session_history`，把权重向学生曾经薄弱的子知识点倾斜。
4. 按方法参数路由：
   - `--objective`（法考科目默认）：加载 `bar-prep-questions` 技能，跑 N 道客观题（单选 / 多选 / 不定项）。触及有新旧法差异的规则时，按该技能的 `## 法条时效与新旧法处理` 显式标出。给每题标卷别（`[卷一]` / `[卷二]`）。
   - `--subjective`：加载 `bar-prep-questions`，跑 N 道主观题（案例分析 + 论述）。按主观题批改标准评分（争议焦点、法律依据、说理、结论、「答：」开头）。
   - `--flashcards`：加载 `flashcards` 技能，跑 N 张 `--drill` 模式的卡。
5. 逐题呈现。每题作答后讲清对 / 错原因，规则涉及新旧修订时显式标出现行有效版本。
6. 结束时写入结果：
   - 若 `study-plan.yaml` 存在：按 `study-plan` 技能的 schema 追加到 `session_history`。
   - 若不存在：写入 `~/.claude/plugins/config/claude-for-legal-cn/law-student-cn/session-history.yaml`。
7. 报告：
   - 得分：X/N（百分比）
   - 错题：附子知识点标签
   - 本次薄弱子知识点
   - 与该科目往次对比（若历史有 2 次以上）
   - 计划下一步建议

---

## 转换说明（质量自检）

- **分级：A 级直接转化。** 保留原 session 技能的整套路由逻辑（三种 flag、写入 study-plan.yaml、fallback 到 session-history.yaml、逐题呈现 + 反馈、报告结构）。
- **实体法层调整：**
  - `--mbe` → `--objective`（法考客观题）
  - `--essay` → `--subjective`（法考主观题）
  - `--flashcards` 保留
  - 州法分歧 handling（jurisdiction_mode: ube / state-specific）→ 新旧法处理（现行有效版本 / 修订对比），按 `bar-prep-questions` 的对应规则
- **卷别标签：** 新增 `[卷一]` / `[卷二]` 标签，对应法考客观题两卷。
- **命令前缀：** 全部本地化为 `claude-for-legal-cn/law-student-cn`。
