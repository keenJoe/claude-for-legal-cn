> **这份地图是给谁看的**：法务、合规、律师 —— 不需要任何编程基础。
> 读完它，你知道这是什么、能帮你做什么、怎么开始用。

# claude-for-legal-cn 使用地图

## 一、整体介绍：这是什么？

**一句话：这是一盒"会干活的法务助理"，每个助理专精一个领域，按你们团队的规矩干活，产出永远是"给你审的草稿"，不是结论。**

想象你团队里多了十几个助理：

- 有的专门审合同（NDA、供应商协议、SaaS 订阅）
- 有的专门盯期限（续约、商标续展、诉讼时效、假期期限）
- 有的专门做合规判断（数据出境走哪条路、发布文案能不能发、AI 能不能用）
- 有的专门盯监管（法规出了什么新规、跟我们的制度差在哪）

每个助理入职时都先问你 10–20 分钟问题（**冷启动访谈**），把你团队的规矩记下来 —— 标准立场、可接受的退让、绝不接受的红线、谁审批什么。之后它干活就照这个规矩来，而不是照通用模板。

### 它由三部分组成

| 部分 | 是什么 | 类比 |
|---|---|---|
| **插件（Plugin）** | 一个领域一套完整能力，按需安装 | 一个"助理包"：招一个合同助理就装合同包 |
| **技能（Skill）** | 插件里的一个个具体工作流，说人话调用 | 助理的"作业流程手册" |
| **执业档案（CLAUDE.md）** | 记录你们团队规矩的文件，助理干活前先读 | 助理的"入职培训记录" |

### 三个关键事实（先消除最大误解）

1. **不需要写代码。** 全程对话式：你把文件给它、说你要干什么，它干活。像跟助理说话一样。
2. **它不替你决定。** 每份输出顶部都写着"本文件由 AI 辅助生成，是待律师审核的工作草稿，不构成法律意见"。签不签、发不发，永远你说了算。
3. **它不编法条。** 引用法律时会标注来源等级：`[国家法律法规数据库]`（真查过）／`[模型知识 — 待核验]`（凭记忆，需要你核）／`[待核验条文号]`（记得有这规定但不确定条文号）。没有标注来源的引用，你该警惕。

---

## 二、每一个插件的作用

按"你日常在做什么"分组，12 个插件如下。每个插件都含一个**冷启动访谈**（配置它自己）和 **customize**（随时调整它），表里不再重复。

### 事务与咨询类（公司日常高频）

| 插件 | 管什么 | 具体包含（技能） |
|---|---|---|
| **commercial-legal-cn**<br>商务合同 | 供应商协议、NDA、SaaS 订阅、续约、升级 | `review`（合同审查入口）· `vendor-agreement-review`（供应商协议）· `nda-review`（NDA 三级分流：绿/黄/红）· `saas-msa-review`（SaaS/MSA）· `amendment-history`（修订单追踪）· `renewal-tracker`（续约期限）· `escalation-flagger`(升级路由) · `stakeholder-summary`（业务方版本）· `review-proposals`（playbook 更新评审） |
| **corporate-legal-cn**<br>公司法务 | 并购尽调、公司治理、披露 | `tabular-review`（尽调表格审查，每格带出处）· `diligence-issue-extraction`（问题提取）· `material-contract-schedule`（重大合同清单）· `closing-checklist`（交割清单）· `written-consent`（股东会/董事会决议）· `board-minutes`（会议记录）· `entity-compliance`（实体合规期限）· `integration-management`（并购后整合）· `deal-team-summary`（交易简报）· `ai-tool-handoff`（AI 尽调工具结果交接） |
| **privacy-legal-cn**<br>个人信息保护 | 隐私合规全流程 | `use-case-triage`（处理活动分流：可进行/需 PIIA/法定必做）· `pia-generation`（个人信息保护影响评估 PIIA）· `dpa-review`（委托处理协议）· `dsar-response`（个人权利请求答复）· `reg-gap-analysis`(新规对照) · `policy-monitor`（制度漂移监控） |
| **product-legal-cn**<br>产品法务 | 发布、文案、快速问答 | `launch-review`（发布审查）· `marketing-claims-review`（营销文案：绝对化用语、虚假宣传）· `is-this-a-problem`（"这有问题吗"快速问答）· `feature-risk-assessment`（功能深挖） |
| **employment-legal-cn**<br>劳动用工 | 雇佣全周期（技能最多） | `hiring-review`（录用审查）· `termination-review`（解除审查：N/N+1/2N）· `worker-classification`（劳动关系 vs 劳务/外包认定）· `wage-hour-qa`（工时加班问答）· `leave-tracker`/`log-leave`（假期期限）· `policy-drafting`（制度起草+民主程序）· `handbook-updates`（手册修订）· `internal-investigation`（内部调查，7 个子技能）· `international-expansion`（跨境用工） |
| **ai-governance-legal-cn**<br>AI 治理 | 生成式 AI、算法备案 | `use-case-triage`（AI 用例分流）· `aia-generation`（AI 影响评估）· `vendor-ai-review`（AI 供应商条款）· `ai-inventory`（AI 系统台账）· `reg-gap-analysis`（新规对照）· `policy-starter`（AI 制度起草）· `policy-monitor`（制度漂移） |
| **regulatory-legal-cn**<br>监管监控 | 法规变化、制度缺口 | `reg-feed-watcher`（监管源巡检）· `policy-diff`（新规 vs 制度差异）· `gap-surfacer`（缺口追踪）· `policy-redraft`（制度修订建议）· `comments`（征求意见稿期限） |
| **ip-legal-cn**<br>知识产权 | 商标、专利、著作权、商业秘密 | `clearance`（商标先查）· `fto-triage`（自由实施分析）· `invention-intake`（发明披露筛查）· `infringement-triage`（侵权分流）· `cease-desist`（警告函/律师函）· `takedown`(删除通知) · `ip-clause-review`（IP 条款）· `oss-review`（开源合规）· `portfolio`（组合期限：续展、年费） |

### 诉讼类

| 插件 | 管什么 | 具体包含（技能） |
|---|---|---|
| **litigation-legal-cn**<br>民事诉讼 | 案件管理 + 诉讼文书 | 案件侧：`matter-intake`（立案）· `matter-briefing`（案件简报）· `matter-update`· `matter-close`· `portfolio-status`（组合视图）· `oc-status`（外派律师跟进）· `legal-hold`（证据保存）· `chronology`（时间线）· `subpoena-triage`（调查取证分流）· `privilege-log-review`（保密筛查）．文书侧：`claim-chart`（构成要件表）· `demand-draft/intake/received`（律师函起草/信息收集/收到函分流）· `deposition-prep`（证人出庭准备）· `brief-section-drafter`（法律文书段落） |

### 学习与实践类

| 插件 | 管什么 | 具体包含（技能） |
|---|---|---|
| **law-student-cn**<br>法学生 | 学习辅助（只引导不代答） | `socratic-drill`（苏格拉底提问）· `case-brief`（案例研读）· `outline-builder`（大纲）· `irac-practice`（案例分析批改）· `bar-prep-questions`（法考题目）· `flashcards`（记忆卡）· `cold-call-prep`（课堂提问预习）· `exam-forecast`（考点预测）· `study-plan`/`session`（学习计划）· `legal-writing`（写作点评） |
| **legal-clinic-cn**<br>法律援助诊所 | 高校法援工作 | `ramp`（学生上岗）· `client-intake`(接待) · `client-comms-log`（沟通日志）· `research-start`（检索路线）· `memo`（备忘录）· `draft`/`form-generation`（文书/表格）· `client-letter`/`plain-language-letters`（给当事人的信）· `deadlines`（期限——注意诉讼时效）· `status`（案件状态）· `semester-handoff`（学期交接）· `supervisor-review-queue`（老师审阅队列） |

### 生态类

| 插件 | 管什么 | 具体包含（技能） |
|---|---|---|
| **legal-builder-hub-cn**<br>技能集市 | 安装社区技能（带安全审查） | `registry-browser`（浏览技能仓库）· `skill-installer`（安装+信任检查）· `skills-qa`（技能质量评审）· `auto-updater`（更新检查）· `skill-manager`/`disable`/`uninstall`（管理）· `related-skills-surfacer`（按你的活动推荐） |

### 后台定时任务（不需要你触发，自动跑）

各插件还带 10 个**定时 agent**：续约监控、成交复盘、playbook 监控（商务）· 数据室监控（公司）· 假期期限（劳动）· 案卷监控（诉讼）· IP 续展（知产）· 发布雷达（产品）· 监管摘要（监管）· 仓库同步（集市）。它们按你设定的节奏干活，报告推到你配置的地方（企业微信/钉钉/Slack）。

---

## 三、如何使用

### 第 0 步：确认环境

你需要在 **Claude Code**（终端工具）或 **Claude Cowork**（桌面版）里操作。手机版不支持安装插件。

### 第 1 步：安装（一次性，30 秒）

```
/plugin marketplace add <仓库路径>/for-cn
/plugin install commercial-legal-cn@claude-for-legal-cn
```

装几个按需来 —— 先装你最忙的领域，用熟了再装别的。安装完**重启**。

### 第 2 步：冷启动访谈（每插件一次，10–20 分钟）

```
/commercial-legal-cn:cold-start-interview
```

它会问你：你们公司是采购方还是供应方？合同标准条款是什么？违约金水平？谁审批什么？然后**读你给的种子文件**（几份已签合同、制度文件、审批矩阵——越多越准），最后写一份执业档案。

> **这一步最容易被跳过，也是"为什么它输出的是模板货"的唯一原因。** 跳过 = 它按通用默认干活；跑完 = 它按你的规矩干活。

### 第 3 步：直接说人话干活

配置好后，日常使用就是对话。示例开场：

| 你想干什么 | 你就说 |
|---|---|
| 审一份对方发来的 NDA | 「审一下这份保密协议」 |
| 担心数据出境 | 「外资总部要访问我们系统里的数据，合规吗？」 |
| 查续约 | 「什么合同 90 天内要续约？」 |
| 问发布 | 「这个新功能上架前要做什么？」 |
| 看休假期限 | 「有员工的医疗期快到了，查一下」 |
| 问法规动态 | 「网信办最近有什么新的？」 |

也可以显式调用命令（`/插件名:技能名`），比如 `/commercial-legal-cn:nda-review`。

### 进阶：可以改它

- **改规矩**：直接编辑执业档案文件（`~/.claude/plugins/config/claude-for-legal-cn/<插件>-cn/CLAUDE.md`），改一处=全局生效。
- **重访谈**：`/<插件>:cold-start-interview --redo`。
- **接你的系统**（可选）：连接合同管理、北大法宝、企业微信等，让它能读你的数据。不接也能用（手动粘贴文件），接了更顺手。

---

## 四、其他

### 安全与责任边界（务必读）

- **草稿头**：每份输出顶部固定「待律师审核的工作草稿，不构成法律意见」。
- **引用分级**：法条引用标注来源等级，`[模型知识 — 待核验]` 表示未经检索验证——这份引用你需要先核。
- **防"被文件骗"**：合同、法规、网页里出现的任何"指令性文字"会被当作数据而非指令处理，不会照做。
- **大文件诚实**：50 页以上的合同没读完就是没读完，它会写明读了哪几页。
- **关键动作前提示**：除非你是律师/法务，发送红字、签署、对外发函前它会停下来确认。

### 常见问题

**Q：需要学代码吗？** 不需要。命令都是 `/<插件>:<技能>` 或自然语言。

**Q：它会把我公司的数据发到外面吗？** 数据只在你的 Claude 会话和你的连接器范围内；接入外部系统（如企业微信）需要你授权。

**Q：能替换律师吗？** 不能。它是"加速审查的草稿机"，不是"做决定的"。

**Q：我不接任何系统能用吗？** 能。手动粘贴文件即可；接系统只影响效率和自动化程度。

**Q：更新怎么办？** `/plugin update`。本仓库的转换规则（`for-cn/references/conversion-spec.md`）保证上游英文版更新后能对照转换，校验脚本（`for-cn/scripts/validate-cn.py`）检测英美法概念残留。

### 想深入看结构？

```
for-cn/
  .claude-plugin/marketplace.json   # 市场清单（12 插件）
  <插件>-cn/
    .claude-plugin/plugin.json      # 插件元信息
    CLAUDE.md                       # 执业档案模板 ← 冷启动访谈复制到你的机器
    skills/<技能>/SKILL.md           # 技能正文（150 个）
    agents/                         # 定时任务
    hooks/  .mcp.json               # 连接器
  managed-agent-cookbooks/          # 无头部署模板（给工程团队用）
  references/                       # 转换规范、访谈协议、模板规范
  scripts/validate-cn.py            # 校验脚本
```

> **与技术细节**：本仓库由 `anthropics/claude-for-legal`（英文原版）转换而来 —— 保留工作流架构，替换实体法为中国法。转换分级：A 直接换法条 / B 大改 / C 重写（原版概念中国法下不存在，如"自由雇佣"→法定解除事由）/ D 新增（中国特有，如数据出境四路径）。每个 SKILL.md 末尾的「转换决策自检」记录了这些变化，你需要审查某个技能的可信度时可从那里开始。
