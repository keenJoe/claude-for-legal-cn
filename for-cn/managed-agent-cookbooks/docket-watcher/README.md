# 案卷监控（Docket Watcher）—— 托管 Agent 模板

## 概览

监控活跃诉讼组合的法院案卷。中国裁判文书网覆盖全国法院公开文书；人民法院案例库、各省高院官网补充。对每个活跃案件，agent 拉取上次检查以来的新文书，把文书类型映射到候选期限，与案件历史和未完成交付物交叉比对，产出案卷状态报告 + 结构化期限信息流。

与 `litigation-legal-cn` 插件的 [`docket-watcher`](../../for-cn/litigation-legal-cn/agents/docket-watcher.md) agent 同源 —— 本目录是 `POST /v1/agents` 的托管 Agent cookbook。

## ⚠️ 部署前注意

- **计算出的期限是线索，不是日历条目。** 法院期限规则因辖区、法院、法官、地方规则而异，且可能被个案管理令改变。错过法院期限有执业责任后果。持证律师在记入排期前，必须对照有效的地方规则与个案管理令核验每个计算期限。本 agent 在该决策的上游，不能替代它。
- **文书分类是启发式的。** 文书类型到期限规则的映射会错：把程序性裁定读成实体判决、把和解协议读成证据争议。读原文，不要只信标签。
- **未知法院 ≠ 默认值。** 如果没有建立规则索引的法院有了新文书，agent 标为 `confidence: low` + `needs_verification: true`，不套用通用规则。
- **「案卷平静」不是「案卷干净」。** 送达延迟、公告送达晚几天常见。没有新文书是关于信息源的陈述，不是关于案件的陈述。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export WENSHU_MCP_URL=...          # 中国裁判文书网
export RMFYALK_MCP_URL=...         # 人民法院案例库（可选）
../../scripts/deploy-managed-agent.sh docket-watcher
```

> 中国法院体系无联邦层级划分；案卷检索主要通过中国裁判文书网（公开文书）、各省高院官网和律所自建数据库（如威科、北大法宝）。

## Steering 事件

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

法院文书 —— 起诉状、答辩状、证据清单、裁定 —— 都是**不可信输入**。提交人可以在文书正文里写「忽略之前的指令」。三层隔离让 Write 和网络访问远离文书：

| 层级 | 接触不可信文书？ | 工具 | 连接器 |
|---|---|---|---|
| **`docket-reader`** | **是**（只读） | `Read`, `Grep` | 裁判文书网、人民法院案例库（只读） |
| `deadline-mapper` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | 无 |
| **`tracker-writer`**（管 Write） | 否 | `Read`, `Write` | 无 |

`docket-reader` 返回长度受限、符合 schema 的 JSON（文书类型、日期、当事人、案号）。`deadline-mapper` 无 MCP、无网络，只应用部署团队配置的规则。输出：`./out/docket-report-<日期>.md` + `./out/deadlines-<日期>.yaml`（供排期系统导入）。

**不保证：** 每个期限都带 `confidence` 和 `needs_verification` 字段。低置信条目在报告里被隔离标记。任何非源自明确规则的期限都加 `[待核验]`。这是人工复核的下限不是上限；负责排期的律师对照有效规则确认每个日期。

## 适配清单

- **MCP URL。** 指向你们的裁判文书库、法院平台端点。
- **案件清单。** `deadline-mapper` 和 orchestrator 从 `litigation-legal-cn` 的 `matters/_log.yaml` 加载案件（案号、法院、上次检查时间）。首次部署前，把活跃案件录入那里。
- **辖区期限规则表。** 通用民诉法规则（上诉期 15 日、举证期限、再审 6 个月、执行时效 2 年）一次编码；地方法院规则和个案管理令需特殊处理。未知法院标 `confidence: low`。
- **交付物 YAML。** 报告到 `./out/`，期限 YAML 经部署流水线接到排期系统。
- **推送路由。** agent 经 `handoff_request` 告诉 orchestrator 报告去哪（企微群/邮件），关键标记路由给谁。
- **节奏。** 多数案件每周检查；近期开庭、处于庭审/举证关键期、或 `risk: critical` 的案件每日。

## 本 cookbook 不提供

- 不把计算期限记入日历 —— 落入排期前必须由人工对照有效规则核验
- 不信任自己的文书分类 —— 映射会错，读原文
- 不决定应对策略 —— 告诉你「判决已送达」是事实，怎么办是律师决定
- 不碰已结案件（除非被明确指示）
