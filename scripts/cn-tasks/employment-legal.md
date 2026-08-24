你的任务：把源插件 `employment-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/employment-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../employment-legal/`（一次性读全部技能的 SKILL.md，技能清单：cold-start-interview, customize, expansion-kickoff, expansion-update, handbook-updates, hiring-review, internal-investigation, international-expansion, investigation-add, investigation-memo, investigation-open, investigation-query, investigation-summary, leave-tracker, log-leave, matter-workspace, policy-drafting, termination-review, wage-hour-qa, worker-classification）

你要产出（全部写入 for-cn/employment-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/employment-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/employment-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/employment-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：劳动用工（劳动合同法、劳动争议调解仲裁法、社保法、竞业限制、女职工保护））：
额外要求：
1. **核心差异**：中国无at-will雇佣——解除必须有法定理由：39条（过错解除）、40条（无过错/医疗期满、不能胜任、客观情况重大变化）、41条（经济性裁员）；41条必须提前30日或额外1个月工资（N+1）；违法解除赔偿金2N（87条）。
2. **经济补偿**：46/47条N（每满一年1个月）；月工资高于当地社平3倍的按3倍封顶、最高12年。
3. **试用期**：19条——3个月以上不满1年：不超过1个月；1年以上不满3年：不超过2个月；3年以上/无固定：不超过6个月；同一单位只能约定一次试用期；试用期工资不低于80%。
4. **竞业限制**：24条——主体（高管/高技/保密义务人）、期限≤2年、必须经济补偿；补偿标准各地不同（多数30%，无约定可主张）。涉及员工竞业限制的**劳动**竞业 vs 交易相对方**商业**竞业（民法典+反垄断法）区分。
5. **劳动关系认定**：劳社部发〔2005〕12号（三要素：主体资格、从属性、业务组成部分）；外卖/网约车等新业态用工——关系认定从宽，注意最高法指导案例。
6. **劳动争议前置**：仲裁前置——仲裁（劳动争议调解仲裁法，一般45天审限）→诉讼（不服仲裁15日内起诉）；仲裁时效1年。
7. **女职工保护**：产假（158天，各地不同：浙江/西藏更长）、哺乳、三期不得解除（42条）、生育津贴。
8. **病假/医疗期**：医疗期（3-24个月，按工龄），病假工资各地规定（不低于最低工资80%等）。
9. **社保**：社会保险法——未缴社保是高频争议点，解除可主张补偿。
10. **涉外用工**：外国人来华工作许可、实习备案；香港/澳门/台湾员工。
11. **新业态**：灵活用工、外包 vs 派遣（劳务派遣暂行规定：临时性/辅助性/替代性，10%比例红线）、平台用工。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。