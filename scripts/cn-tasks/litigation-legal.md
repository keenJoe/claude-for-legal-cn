你的任务：把源插件 `litigation-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/litigation-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../litigation-legal/`（一次性读全部技能的 SKILL.md，技能清单：brief-section-drafter, chronology, claim-chart, cold-start-interview, customize, demand-draft, demand-intake, demand-received, deposition-prep, legal-hold, matter-briefing, matter-close, matter-intake, matter-update, matter-workspace, oc-status, portfolio-status, privilege-log-review, subpoena-triage）

你要产出（全部写入 for-cn/litigation-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/litigation-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/litigation-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/litigation-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：民事诉讼（民诉法2023修正、证据规定、诉讼时效、保全、律师函））：
额外要求：
1. **中国民诉法（2023修正）关键点**：
   - 起诉条件（122条）、管辖（级别管辖+协议管辖35条+专属管辖+网络合同管辖）
   - 诉讼时效：一般3年（民法典188条）、普通案件上诉期15日、判决给付期限、申请再审6个月（民诉法212条）、执行时效2年
   - 保全：103-104条（诉前/诉中保全、担保）、行为保全（知识产权案件常见，反法/商标法行为保全司法解释）
   - 举证：谁主张谁举证、举证期限（证据规定）、逾期举证后果、自认、电子数据真实性（证据规定14条+电子数据规则——哈希、时间戳、公证）
   - 证人出庭、专家辅助人（证据规定）
   - 一审普通程序6个月、简易3个月、二审3个月
2. **中国律师函/起诉状格式**：起诉状：当事人信息→诉讼请求→事实与理由→证据清单→落款；答辩状、代理词、质证意见、证据目录。用中国法院官方文书格式（最高法规范格式）。
3. **案件管理**：中国语境——案件台账（Excel/企业微信）、开庭日期、举证期限、执行申请期限、上诉期限。
4. **FRE 408对应**：中国无直接对应「和解邀约不可采」证据规则，但民诉法/证据规定（自认规则、调解中的让步不得作为不利证据——最高法民诉法解释第107条「调解协议、和解协议的让步不得作为对其不利的证据」）。写知识点，引用条文要标[待核验条文号]，因为我不完全确定107条条款号准确性。用[调解/和解中的让步不得作为不利证据]这个知识点表述更稳妥，条文号标[待核验]。
5. **诉讼请求设计**：中国实务——违约金调整抗辩、律师费承担（合同约定/最高法支持范围）、利息（LPR）、迟延履行加倍利息（民诉法第264条？不确定条款号——标[待核验条文号]，知识点：加倍支付迟延履行期间债务利息）。
6. **仲裁 vs 诉讼**：涉外合同常选仲裁（CIETAC/北仲/上仲）；仲裁一裁终局、保全（仲裁法28条）、裁决执行（仲裁法62条+民诉法执行）。
7. **证据固定**：中国实务——电子证据公证（公证处）、区块链存证（法院认可，最高法区块链存证司法解释）、时间戳、哈希校验。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。