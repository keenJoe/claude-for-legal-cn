你的任务：把源插件 `privacy-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/privacy-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../privacy-legal/`（一次性读全部技能的 SKILL.md，技能清单：cold-start-interview, customize, dpa-review, dsar-response, matter-workspace, pia-generation, policy-monitor, reg-gap-analysis, use-case-triage）

你要产出（全部写入 for-cn/privacy-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/privacy-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/privacy-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/privacy-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：个人信息保护（个保法/数安法/网安法、数据出境四路径））：
额外要求：
1. **PIA/DPIA中国版**：中国法下是「个人信息保护影响评估（PIIA）」——个保法55/56条。触发情形：处理敏感个人信息、利用个人信息进行自动化决策、委托处理/对外提供/公开、向境外提供、其他对个人权益有重大影响。三性审查：合法正当必要、对个人权益影响及风险、保护措施有效性。
2. **数据出境（核心新增）**：四条路径——安全评估申报（CIIO/重要数据/100万人/1万人敏感）、保护认证、标准合同备案（10个工作日省网信办）、豁免（2024《促进和规范数据跨境流动规定》七情形）。阈值按「人数」计，当年1月1日起算。
3. **委托处理**：个保法21条，受托人义务、转委托书面同意、期满返还删除、监督权。
4. **个人权利**：34-45条——知情权、决定权、更正补充、删除、复制、撤回同意、可携带、解释说明；响应时限做法条明确。
5. **敏感信息**：28-29条，生物识别、宗教、特定身份、医疗健康、金融账户、行踪轨迹、不满14岁未成年人；单独同意。
6. **DPA（数据处理协议）**：中国语境下是「委托处理协议」或「个人信息保护协议」，必备条款按21条。
7. **DSAR**：中国版「个人权利请求」响应流程：验证请求→定位数据→评估→回复；注意保存期限、删除请求与法定义务冲突。
8. **跨境员工HR**：境外总部访问中国员工数据=出境，需判断是否需要单独同意（劳动合同履行豁免：13条2/3项）。
9. **监管**：网信办、工信部、公安（等保）、市监（App违规）、个保合规审计制度（54/64条）。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。