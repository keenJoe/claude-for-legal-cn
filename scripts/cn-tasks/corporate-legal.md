你的任务：把源插件 `corporate-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/corporate-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../corporate-legal/`（一次性读全部技能的 SKILL.md，技能清单：ai-tool-handoff, board-minutes, closing-checklist, cold-start-interview, customize, deal-team-summary, diligence-issue-extraction, entity-compliance, integration-management, material-contract-schedule, matter-workspace, tabular-review, written-consent）

你要产出（全部写入 for-cn/corporate-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/corporate-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/corporate-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/corporate-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：公司事务（公司法2023修订、外商投资法、反垄断申报、ODI））：
额外要求：
1. **公司法2023修订**（2024-07-01施行）：有限公司注册资本5年实缴（公司法47条）；股份公司授权资本制；审计委员会替代监事会；法定代表人制度（公司法定代表人由代表公司执行公司事务的董事或者经理担任）；股东失权制度；横向人格否认（民法典83条/公司法23条）。
2. **公司治理文书**：董事会决议/股东会决议（须核对召集程序、表决权、回避、章程约定）；会议记录；章程修订。
3. **M&A尽调**：中国语境审查重点：股权结构（代持、对赌）、注册资本实缴/抽逃、对外担保（公司法15条）、《外商投资法》负面清单、反垄断申报（经营者集中，国监委标准：营业额超4亿+20亿）、外汇管理（ODI/37号文）、劳动（经济补偿）、环保（环评）、知识产权（职务发明）、涉诉（裁判文书网）。
4. **交易文件**：股权转让协议（优先购买权公司法84条）、增资协议、股东协议（对赌回购——九民纪要：与公司对赌条款效力，须履行减资程序/上市审核限制）、业绩承诺。
5. **合资企业**：外商投资法（2019）与负面清单；VIE架构提示。
6. **上市**：注册制（证券法）、IPO审核要点、信息披露（交易所规则）、股权激励（上市公司股权激励管理办法）。
7. **法律意见书**：中国语境下律师出具法律意见书、尽职调查报告。输出是工作文件不是正式意见书。
8. **期限管理**：年报（工商年报3月-6月30日）、税务申报、实缴期限、章程约定日期。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。