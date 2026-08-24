# 并购尽调 — 标准列集

买方目标合同审查的默认 schema。从这里开始，再按交易增删列。这是起点，不是清单——收购协议的陈述和尽调清单决定实际重要的是什么。

```yaml
schema:
  name: "并购尽调 — 标准"
  columns:
    - id: counterparty
      label: "相对方"
      type: verbatim
      prompt: "除目标公司外的合同方名称，逐字引用。"

    - id: agreement_type
      label: "协议类型"
      type: classify
      options: [主协议, 采购订单, 许可入, 许可出, 租赁, 服务, 供应, 分销, 保密, 合资, 借款, 担保, 劳动, 其他]
      prompt: "这是什么类型的协议？"

    - id: effective_date
      label: "生效日"
      type: date
      prompt: "本协议何时生效？"

    - id: term
      label: "期限"
      type: duration
      prompt: "初始期限是多长？"

    - id: auto_renewal
      label: "自动续约"
      type: classify
      options: [无, 年度, 固定期, 永续]
      prompt: "协议自动续约吗？周期是什么？"

    - id: termination_for_convenience
      label: "任意解除"
      type: classify
      options: [无, 双方均可, 仅目标, 仅相对方]
      prompt: "任一方可无因终止吗？谁？"

    - id: termination_notice
      label: "终止通知期"
      type: duration
      prompt: "终止需要多长通知期？"

    - id: change_of_control
      label: "控制权变更"
      type: classify
      options: [未约定, 需同意, 不得无理拒绝的同意, 自动终止, 仅通知, 相对方享有终止权]
      prompt: "协议是否处理目标的控制权变更？触发什么、发生什么？"

    - id: assignment
      label: "转让"
      type: classify
      options: [未约定, 需同意, 不得无理拒绝的同意, 可自由转让, 可向关联方转让, 不得转让]
      prompt: "目标能转让本协议吗？有什么限制？（注：中国法下未约定时，权利转让原则上需通知债务人，义务转让原则上需债权人同意——民法典合同编，条文号待核验）"

    - id: exclusivity
      label: "排他 / 竞业限制"
      type: classify
      options: [无, 独家供应, 独家客户, 竞业限制, 禁止招揽, 地域限制, 最惠国]
      prompt: "协议是否限制任一方与其他方竞争或签约？"

    - id: liability_cap
      label: "责任限额"
      type: currency
      prompt: "有责任上限吗？金额或倍数是多少？"

    - id: indemnification
      label: "赔偿"
      type: classify
      options: [无, 相互, 目标赔偿, 相对方赔偿, 仅 IP, 仅第三人索赔]
      prompt: "谁赔偿谁，为什么？"

    - id: governing_law
      label: "适用法律"
      type: verbatim
      prompt: "适用什么法律？"

    - id: dispute_resolution
      label: "争议解决"
      type: classify
      options: [诉讼, 仲裁, 先调解后诉讼, 先调解后仲裁, 未约定]
      prompt: "争议如何解决？（若约定仲裁，具体机构必须明确，否则仲裁条款可能因约定不明而无效——仲裁法第 16、18 条）"

    - id: arbitration_institution
      label: "仲裁机构"
      type: verbatim
      prompt: "如约定仲裁，具体机构名称是什么？（如 CIETAC 中国国际经济贸易仲裁委员会、北京仲裁委员会等——必须写机构全称）"

    - id: most_favored_nation
      label: "最惠国 / 价格保护"
      type: classify
      options: [无, 最惠国价格, 价格匹配, 对标权]
      prompt: "有最惠国或价格保护条款吗？"

    - id: minimum_commitments
      label: "最低采购 / 数量承诺"
      type: currency
      prompt: "有最低采购、数量或支出承诺吗？"

    - id: ip_ownership
      label: "IP 权属"
      type: classify
      options: [各自拥有, 目标拥有工作成果, 相对方拥有工作成果, 共有, 仅许可, 未约定]
      prompt: "协议下产生或使用的知识产权归谁？（注意区分职务发明——专利法：单位提供物质技术条件的属于职务发明，权属归单位）"

    - id: confidentiality_term
      label: "保密存续期"
      type: duration
      prompt: "终止后保密义务存续多久？（商业秘密建议约定至不再构成商业秘密时止，而非固定年限——反不正当竞争法第 9 条）"

    - id: guarantee_or_security
      label: "担保 / 抵押"
      type: classify
      options: [无, 保证担保, 抵押, 质押, 独立保函, 母公司保证]
      prompt: "协议是否含担保或抵押安排？（对目标提供的对外担保，尽调重点——公司法第 15 条：为他人担保须经董事会或股东会决议）"

    - id: personal_information_involved
      label: "涉及个人信息处理"
      type: classify
      options: [无, 目标作为处理者, 目标作为受托方, 共同处理者, 涉数据出境]
      prompt: "协议是否涉及个人信息处理或数据出境？（个保法第 21 条委托处理必备条款，第 38-43 条出境规则；控制权变更后可能触发数据出境重新评估）"

    - id: audit_rights
      label: "审计权"
      type: classify
      options: [无, 相对方可审计目标, 目标可审计相对方, 相互]
      prompt: "任一方有审计权吗？"

    - id: notices
      label: "通知条款"
      type: verbatim
      prompt: "目标的通知地址和方式是什么？"
```

## 按交易类型的常见增列

- **科技 / IP 密集目标：** 源代码托管、开源限制、数据权利、模型训练权利、API 访问、软件著作权登记情况
- **医疗 / 生命科学：** 医疗器械/药品注册、GCP 合规、临床试验义务、监管申报义务
- **政府/军工承包商：** 变更主体的同意要求、涉密文件流转、保密资格
- **不动产：** 续约选择权、租金递增、物业费、承租人变更需出租人同意（合同法/民法典默认规则）
- **金融业务：** 监管审批条件、资本要求、金融监管申报触发点
- **上市公司/拟上市公司：** 关联交易审议程序、同业竞争、对赌回购条款

## 快速首轮的常见削减

时间紧迫的初次筛查，这 6 列回答 80% 早期交易问题：counterparty、effective_date、term、change_of_control、assignment、termination_for_convenience。先跑这些，交易团队排优先级后再扩 schema。

## 质量自检

本次转换决策：A 级直转，加中国实务补充列。列类型系统与结构保留。选项翻译为中文并对齐中国合同实务用语。补充 4 个中国语境专属列：**arbitration_institution**（仲裁机构必须明确——仲裁法第 16、18 条）、**guarantee_or_security**（担保/抵押）、**personal_information_involved**（个人信息处理与数据出境）。IP 权属列补充职务发明提示（专利法）。保密存续期补充商业秘密建议条款（反不正当竞争法第 9 条）。转让列补充民法典合同编默认规则提示（`[待核验条文号]`）。按交易类型的增列改为中国常见语境（软件著作权登记、监管审批、上市公司关联交易与同业竞争）。
