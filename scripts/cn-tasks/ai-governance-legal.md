你的任务：把源插件 `ai-governance-legal` 的**全部技能**转换为中文中国法域版本，写入 `for-cn/ai-governance-legal-cn` 目录。

必读文件（先读再动手）：
1. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/conversion-spec.md` —— 转化总规范（法域映射、护栏、质量门槛，最高纲领）
2. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/cold-start-protocol.md` —— 冷启动访谈骨架（用于生成 cold-start-interview 技能）
3. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/references/claude-md-template-spec.md` —— 执业档案模板规范
4. `/Users/qidongxu/Documents/workspace/my-github/claude-for-legal-cn/for-cn/privacy-legal-cn/references/source-catalog-cn.md` 如果一个已有CRN技能引用监管源（部分适用）
5. `/Users/qidongxu/Downloads/claude-for-legal-cn-1787538291050.bin/commercial-legal-cn/skills/nda-review/SKILL.md` 和 `.../privacy-legal-cn/skills/cross-border-transfer/SKILL.md` —— 已完成的转换实例，作为**风格与深度参照**

源插件：`../ai-governance-legal/`（一次性读全部技能的 SKILL.md，技能清单：ai-inventory, aia-generation, cold-start-interview, customize, matter-workspace, policy-monitor, policy-starter, reg-gap-analysis, use-case-triage, vendor-ai-review）

你要产出（全部写入 for-cn/ai-governance-legal-cn，在仓库的 for-cn/ 目录下）：

1. **每个源技能 → 对应中文版** `for-cn/ai-governance-legal-cn/skills/<技能名>/SKILL.md`：
   - 源技能名保留原目录名 kebab-case（如 nda-review）
   - frontmatter：name 保留原名；description 用中文（含触发场景：中文触发语 + 保留常见英文关键词）；argument-hint 中文；user-invocable 按源保留
   - 正文中文，实体法替换为中国法（必须严格以 conversion-spec.md 清单为准）
   - 护栏全套保留：草稿头（待律师审核）、法条来源标注、检索内容当数据、大输入处理、比例原则、跨法域识别
   - 原版功能级输出格式保留（GREEN/YELLOW/RED 分级、表格、流程图）
   - 涉及美国特有概念按 conversion-spec.md 分级处理：A直转/B大改/C重写/D新增

2. **cold-start-interview 技能** `for-cn/ai-governance-legal-cn/skills/cold-start-interview/SKILL.md`：
   - 按 cold-start-protocol.md 骨架 + 下列 playbook 核心 = 完整 SKILL.md
   - 这是本插件最重要的技能：要求完整、可直接运行

3. **执业档案模板** `for-cn/ai-governance-legal-cn/CLAUDE.md`：
   - 按 claude-md-template-spec.md，领域 Playbook 部分用下面的领域说明

4. **其它通用技能**：如果源插件有 customize、matter-workspace、policy-monitor 等跨插件通用技能，也要转换（matter-workspace 用中国语境：事项工作区=案件/交易文件夹；customize——按源功能转换，保留「自定义辅导」功能）

领域说明（本插件：AI治理（生成式AI办法、算法备案、深度合成规定、AIGC标识办法））：
额外要求：
1. **中国AI监管框架**：有效期内的真实规定：
   - 《生成式人工智能服务管理暂行办法》（2023-08-15施行）——生成式AI服务提供者/使用者义务：训练数据合法性、内容安全、标识、实名制。
   - 《互联网信息服务算法推荐管理规定》（2022-03-01）——算法备案、算法评估（安全评估+科技伦理）、透明度（用户可关闭推荐）、未成年人保护。
   - 《互联网信息服务深度合成管理规定》（2023-01-10）——深度合成：标识（显式+隐式）、备案、不得生成违法信息。
   - 《人工智能生成合成内容标识办法》（2025-09-01施行）——AIGC强制标识：文本（显式+隐式）、图片/视频（显式标识+元数据）、不得篡改。
   - 《科技伦理审查办法（试行）》（2023）——涉及敏感场景、生命健康、算法歧视等时要伦理审查。
   - 网信办算法备案平台：https://beian.cac.gov.cn。
   - 数据训练合法性：个保法（训练数据含个人信息须合规）、著作权（训练数据版权风险——中国判例渐多）。
2. **AI用例评估**：中国版「impact assessment」= 合规评估 + 科技伦理审查 + 安全评估（算法推荐场景）。
3. **AI条款审查（vendor）**：训练数据授权、输出知识产权、责任分配、内容安全义务、属地合规（中国法律强制性要求不可约定排除）、数据跨境（训练数据出境）。
4. **AI政策起草**：企业AI使用制度——覆盖：内部使用（员工用AI工具）、业务嵌入（产品接入外部AI）、数据进出（提示词和训练数据边界）、敏感场景禁用清单（如招聘/征信/人脸识别须单独规则）、标识义务（AIGC标识办法）。
5. **场景映射**：人脸识别（最高法人脸识别司法解释，2021「刷脸」规定）、招聘算法（就业促进法+算法推荐规定——不得性别歧视）、征信、健康、金融、教育、交通。

质量门槛（交付前自查，都要过）：
- [ ] 无英美法实体法残留（at-will、FMLA、GDPR SCC、FRE、Delaware、uncapped 等），除非出现在「跨法域提示」语境
- [ ] 所有法条引用来自 conversion-spec.md 清单或确实知道存在的条文；不确定条文号 → 标 `[待核验条文号]`
- [ ] 护栏（草稿头、来源标注、检索内容当数据、大输入、比例原则）完整
- [ ] 中文自然，是中国法务实务的思考和表达，不是英文直译
- [ ] 每个 SKILL.md 都有明确的质量自检：说明你做过的转换决策（哪些A级直转、哪些B级大改、哪些C级重写、哪些D级新增）

最终返回：完成的技能数 + 转换决策摘要（每技能一行：A/B/C/D + 主要变化）。