你的任务：把源插件 `ip-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/ip-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../ip-legal/`（一次性读全部技能的 SKILL.md，技能清单：cease-desist, clearance, cold-start-interview, customize, fto-triage, infringement-triage, invention-intake, ip-clause-review, matter-workspace, oss-review, portfolio, takedown）

你要产出（全部写入 for-cn/ip-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/ip-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/ip-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/ip-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：知识产权（商标法、专利法、著作权法、商业秘密、开源合规））：
额外要求：
1. **商标法**：57条（侵权情形）、13条（驰名——按需认定）、14条（驰名证据）、45条（无效宣告：5年、恶意注册不受限）、49条（撤三：3年不使用）、续展（40条：期满前12个月，宽展期6个月——逾期失效）、异议（33条公告期3个月）。审查：类似商品/近似商标判断、混淆可能性、在先权利。
2. **专利法**：22条（三性：新颖性/创造性/实用性）、25条（不授予——科学发现、智力活动规则、疾病诊断治疗、动物植物品种、原子核变换等）、24条（宽限期）、30条（优先权）、Bolar例外（69条5项）。发明/实用新型/外观设计区别；专利申请文件（权利要求书、说明书）。职务发明（专利法第6条）权属。
3. **著作权法**：24条（合理使用13种情形——2020修订后）、10条（权利内容）、53条（侵权）、网络信息传播权保护条例（24条）、软著登记。AI生成内容著作权（中国判例：北京互联网法院——AI生成图片「具备独创性」案，如「春风十里」案）。
4. **商业秘密**：反法9条（2019修订——三种侵权行为+恶意第三人）、保密义务+竞业限制搭配、密点管理（保密措施：分级、控制访问、水印）、侵犯商业秘密罪（刑法219条）。
5. **FTO**：中国专利检索（国家知识产权局、CNIPA）、FTO分析框架——权利要求拆解+对比+结论（不构成侵权意见书一般由专利代理师/律所出具）。
6. **C&D**：中国版「警告函」——律师函：注意反法/广告法虚吓（最高法关于滥用权利——商标权滥用）、函件发送对象、时间点（诉前）。
7. **开源**：GPL/AGPL/LGPL/BSD/MIT/Apache——中国判例（如「数字天堂」案，GPL效力承认与边界）、合规建议：开源清单、许可证审查、DCO。
8. **登记续展**：商标续展期限10年；专利年费（第1-3年900元等，逾期有滞纳金+恢复期）；软著登记周期。
9. **跨境IP/涉外**：PCT申请、马德里商标、巴黎公约优先权。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。