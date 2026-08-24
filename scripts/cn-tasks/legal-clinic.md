你的任务：把源插件 `legal-clinic` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/legal-clinic-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../legal-clinic/`（一次性读全部技能的 SKILL.md，技能清单：build-guide, client-comms-log, client-intake, client-letter, cold-start-interview, customize, deadlines, draft, form-generation, memo, plain-language-letters, ramp, research-start, semester-handoff, status, supervisor-review-queue）

你要产出（全部写入 for-cn/legal-clinic-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/legal-clinic-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/legal-clinic-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/legal-clinic-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：法律援助诊所（法律援助法、高校诊所））：
额外要求：
1. **中国高校法律援助诊所**：法律援助法（2022-01-01施行）背景——法律援助机构、值班律师、高校诊所（实践中以「法律援助工作站/中心」名义，受司法行政机关指导）；学生非律师，不能以律师身份执业——只能在教师指导下做辅助工作。注意：**高校诊所学生不能出庭代理，只能做材料准备、咨询、普法、调解协助**（不同地区有限度试点——标注需要按当地规定核实[a待核验]）。
2. **接待**：法律援助接待要点——身份核对、案情记录、纠纷类型（劳动/婚姻家事/民间借贷/消费/物业/人身损害/赡养抚养）、经济困难审查（法律援助法41条——申请条件，各地标准）。
3. **期限管理**：诉讼时效提示（3年，民法典188条）、劳动仲裁时效（1年）、证据保存。
4. **文书**：法律咨询意见书、起诉状、答辩状、仲裁申请书（劳动者见多）、调解申请书——用中国法院/仲裁格式。
5. **案件交接**：学期结束交接（诊所学生毕业实习）——案卷清单、进度、未决事项。
6. **ABA 512对应**：美国ABA意见书→中国对应「教师监督+学生行为底线」（学生不能承诺结果、不能收费、不能以律师名义）。格式：行为规范=「诊所行为准则」，标注依据是法律援助法+高校实践规范[a待核验]。
7. **常见案件类型知识**：劳动（拖欠工资、未缴社保、辞退赔偿——最典型）、婚姻家事（离婚、抚养、财产）、交通事故（人身损害、保险理赔）、民间借贷（利率上限LPR4倍——最高法民间借贷司法解释，2020修正）、房屋租赁、物业、消费者维权、行政/刑事了（刑事辩护援助——值班律师：认罪认罚从宽，刑诉法36/48条）。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。