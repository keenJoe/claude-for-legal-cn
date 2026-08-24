你的任务：把源插件 `product-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/product-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../product-legal/`（一次性读全部技能的 SKILL.md，技能清单：cold-start-interview, customize, feature-risk-assessment, is-this-a-problem, launch-review, marketing-claims-review, matter-workspace）

你要产出（全部写入 for-cn/product-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/product-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/product-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/product-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：产品发布与营销合规（广告法、消费者权益保护法、反不正当竞争法））：
额外要求：
1. **广告法**：绝对化用语（广告法9条，「国家级」「最高级」「最佳」等）、虚假广告（4/28条）、广告代言（16条医疗、38条不得代言的）、比较广告合规（反法11/13条）。
2. **消费者权益保护法**：知情权、格式条款、七天无理由退货（网络购物25条）、个人信息条款。
3. **产品责任**：民法典1202-1207条（产品缺陷责任）、产品质量法。
4. **发布审查**：中国语境下「上线审查」= 产品功能合规 + 文案合规 + 隐私政策 + 算法合规（如果涉及）。风险分级：红（违法拟发布）、黄（需修改）、绿（可发）。
5. **定价合规**：价格法、明码标价、价格欺诈（市监总局规定）、促销：反不正当竞争法（有奖销售、虚假宣传）。
6. **未成年人**：未成年人保护法、防沉迷、幼教资质。
7. **许可证**：ICP备案/许可证（工信部）、EDI、游戏版号、出版资质——按产品类型检查前置审批。
8. **广告审查**：医疗广告（卫健委审查）、金融广告（银保监/证监会）、教育培训广告（双减）。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。