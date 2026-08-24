---
name: review
description: >
  按你的 playbook 审查供应商协议、保密协议或 SaaS 订阅合同。从标题识别合同结构，
  路由到正确的审查技能（vendor-agreement-review、nda-review、saas-msa-review），
  并把输出整合成一份备忘录。触发场景：用户说「审一下这份合同」「看看这份服务合同」
  「这个 NDA 行不行」「看看这份 SaaS 协议」，或附上进向合同。
argument-hint: '[文件路径 | 云盘链接 | 合同管理系统编号 | 粘贴文本]'
---

# /review

对照 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md` 的 playbook 审查一份进向合同。从标题识别合同结构，选择合适的技能，并在 confirm_routing 开启时先与用户确认再进行。

## 说明

1. **加载 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md`。** 若有占位符，停下并提示：「先运行 `/commercial-legal-cn:cold-start-interview` —— 我需要先学你们的 playbook 才能对照审查。」

   同时读 `## 审查偏好` → `confirm_routing`。字段缺失时按 `true` 处理。

2. **获取合同：** 从文件路径、云盘链接、合同管理系统编号或粘贴文本。都没有就问。

3. **读文档结构 —— 先看标题。**

   读正文前先提取：
   - 主协议标题（如《技术服务合同》《保密协议》《软件服务合同》）
   - 所有附件、附录、附表、补充协议标题（如「附件一 —— 数据处理条款」「附表 1 —— 订单」「附件三 —— 服务水平协议」）

   这是路由信号。不要只靠正文关键词 —— 一份 40 页、通篇「保密」的技术服务合同不是 NDA。

4. **按文档结构选技能。**

   把每个识别出的文档或章节映射到技能：

   | 文档 / 章节标题含 | 技能 |
   |---|---|
   | 保密协议、NDA、保密合同（作为**主**协议） | **nda-review** |
   | 技术服务合同、技术开发合同、服务合同、外包合同、咨询/顾问合同、采购/购销合同 | **vendor-agreement-review** |
   | 软件服务合同、SaaS 订阅、云服务协议、含自动续约的订单、按期收费的软件服务 | **saas-msa-review**（叠加在 vendor-agreement-review 之上） |
   | 数据处理条款、委托处理协议、个人信息处理条款（作为附件或独立文件） | 记给 **vendor-agreement-review** → 个人信息与数据小节 |
   | 服务水平协议、SLA（作为附件） | 记给 **saas-msa-review** → SLA 小节 |

   可能多个技能同时适用。常见组合：
   - 技术服务合同 + 数据处理附件 → vendor-agreement-review，数据条款一并记
   - SaaS 订阅 + 订单 + SLA 附件 → saas-msa-review（覆盖三者）
   - 服务合同 + 含自动续约的订单 → vendor-agreement-review + saas-msa-review 叠加

   读完标题结构仍真正含糊时（如标题只写「协议」、无附件列表），读正文前两页再定 —— 定完就停下路由。

   *软件许可 vs 软件服务的区分要点：* 一次性买断/本地部署许可走 vendor-agreement-review；年度续费、云端访问的订阅走 saas-msa-review。

5. **开启时确认路由。**

   若 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md` 中 `confirm_routing` 为 `true`（或字段缺失）：

   ```
   我打算把它作为以下类型审查：[合同类型]。

   识别到的文档：
   - [主协议标题] → [技能]
   - [附件一标题] → [如何处理]
   - [附件二标题] → [如何处理]

   对吗？（是 / 否 —— 或告诉我哪里错了）
   ```

   等确认再进行。用户纠正路由的，按其指示进行。

   若 `confirm_routing` 为 `false`：静默进行。在审查备忘录顶部记录路由决策，让用户能看到套用了什么。

6. **运行技能。** 完整走每个技能的工作流。多个技能适用时按序运行，把输出整合成一份备忘录 —— 不要出多份。

7. **检查升级：** 若任何问题超出审查人授权（按档案矩阵），调用 **escalation-flagger** 路由并起草升级请求。

8. **提供后续：**
   - 给业务负责人的业务方版本
   - 带修订标记的 docx
   - 合同管理系统建档（若已连接）
   - 加入续约登记（若发现自动续约）

## 配置 confirm_routing

加到 `~/.claude/plugins/config/claude-for-legal-cn/commercial-legal-cn/CLAUDE.md` → `## 审查偏好`：

```markdown
## 审查偏好

confirm_routing: true   # 设为 false 可跳过路由确认，自动进行
```

冷启动访谈应问这个偏好。默认 `true` —— 确认开启。随着信任建立，用户可设为 `false`。

## 示例

```
/commercial-legal-cn:review 技术服务合同.pdf
```

```
/commercial-legal-cn:review https://云盘链接/文件/ABC123
```

```
/commercial-legal-cn:review
[粘贴合同文本]
```

## 输出

按技能格式的完整审查备忘录。路由决策记在顶部。逐条偏差、具体修订措辞、点名审批人。存到档案 `## 输出` / 房屋风格指定的工作产物去处。

## 质量自检（本技能转换说明）

- **A 级直转：** 路由器结构、confirm_routing 逻辑、按标题识别、多技能整合、后续提供 —— 方法论层原样保留。
- **B 级大改：** 路由映射表的合同类型全换为中国合同实务类型（技术服务、技术开发、软件服务/SaaS、采购/购销、保密协议）；新增软件许可 vs 软件服务的识别提示（中国语境关键区分）。
- **C 级删除：** 无英美法特有概念残留。
- **D 级新增：** 无。
