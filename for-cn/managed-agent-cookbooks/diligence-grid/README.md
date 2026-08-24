# 尽调网格（Diligence Grid）—— 托管 Agent 模板

## 概览

对虚拟数据室（VDR）做批量文档审查。两种模式：

- **watch（监控）** —— 监控 VDR 自截止日以来的新上传，对照部署团队的尽调请求清单类目分类，标记高优先级类目（重大合同、诉讼、知识产权）的上传。
- **grid（网格）** —— 对一个文件夹的文档按列 schema 做表格审查。一份文档一行，一个数据点一列，每个单元格都溯源到逐字引用。M&A 尽调的主力工具。

与 `corporate-legal-cn` 插件同源 —— 本目录是 `POST /v1/agents` 的托管 Agent cookbook。网格模式就是 `tabular-review` 技能，以 headless 方式在一队 extractor worker 上运行。

## ⚠️ 部署前注意

- **每个单元格都是线索，不是结论。** 在律师读过底层文档之前，尽调网格不是陈述与保证、不是披露清单、也不是尽调备忘录。每个单元格里的逐字引用是让复核者快速核验用的 —— 用它。
- **重要性过滤和列分类用的是启发式，不是法律判断。** schema 认为不重要的合同，可能正是压垮交易的那份。extractor 读错条款时，标为「answered」的单元格仍然是错的。复核工时随 `unclear` + `needs_review` + `answered` 增长 —— 不只是被标记的那些。
- **监控模式分类的是元数据和预览，不是完整文档。** 分类器标「低优先级」的新上传，可能是改变交易的补充协议。把监控报告当队列，不当过滤器。
- **相对方上传的文档对工具链也是不可信输入。** grid-writer 的 CSV 公式注入防御是强制的，不是可选的 —— 见下方安全章节。

## 部署

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export VDR_MCP_URL=...              # 数据室（腾讯文档/飞书云盘/坚果云/自建 VDR）
export GDRIVE_MCP_URL=...
export IMANAGE_MCP_URL=...          # 可选；使用时把 toolset default 设为 enabled
../../scripts/deploy-managed-agent.sh diligence-grid
```

## Steering 事件

见 [`steering-examples.json`](./steering-examples.json)。

## 安全与交接

VDR 文档 —— 合同、董事会记录、补充协议、相对方上传 —— 都是**不可信输入**。相对方上传的合同可能含有意图操纵复核者或下游工具链的字符串。四层隔离让 Write 手和 MCP 手都远离文档：

| 层级 | 接触不可信文档？ | 工具 | 连接器 |
|---|---|---|---|
| **`doc-reader`** | **是**（只读） | `Read`, `Grep` | VDR、Google Drive、iManage（只读） |
| **`extractor`** | **是**（只读） | `Read`, `Grep` | 无 |
| `normalizer` / Orchestrator | 否 | `Read`, `Grep`, `Glob`, `Agent` | 无 |
| **`grid-writer`**（管 Write） | 否 | `Read`, `Write` | 无 |

`doc-reader` 和 `extractor` 返回长度受限、符合 schema 的 JSON。Orchestrator 和 `normalizer` 只看到结构化数据。`grid-writer` 产出 `./out/diligence-grid-<日期>.csv`、`./out/diligence-grid-<日期>_sources.csv` 和 `./out/diligence-grid-<日期>-summary.md`。

**CSV 公式注入。** `grid-writer` 写入的每个单元格 —— 值、逐字引用、位置、文档名、列标签 —— 都先做首字符检查（`=`、`+`、`-`、`@`、制表符、回车）。命中的单元格在落入 CSV 前加一个单引号前缀。相对方上传的合同经常含有 Excel/表格会当作公式执行的字符串（`=HYPERLINK(...)` 外泄、老版 Excel 的 `=cmd|...` DDE），交易团队一打开文件就触发。sources CSV 暴露面更大 —— 逐字引用是攻击者可控的表面。

**Xlsx 是部署侧的事。** 本 cookbook 只产出 CSV。部署团队用 `tabular-review` 技能里的 excel 输出规范把它转成 `.xlsx`（隐藏 `_source` 列、悬停显示引用的单元格批注、按状态填色、每列 `Verified` 下拉、`_schema` 和 `_summary` 工作表）。该转换在部署团队自己的 Excel 环境完成。

**不保证：** 本 agent 产出的每个单元格都是**需要核验的线索**，不是结论。复核者读原文、核对引用、勾 `Verified` 列。律师决定什么进入陈述保证、披露清单或备忘录。

## 适配清单

- **VDR URL。** 把 `VDR_MCP_URL` / `GDRIVE_MCP_URL` / `IMANAGE_MCP_URL` 指向你们的数据室。
- **列 schema。** M&A 尽调标准列集是默认。按交易类型定制 —— 技术/IP、医疗健康、房地产、涉外投资、金融监管。中国尽调特有列建议加入：注册资本实缴、对外担保（公司法 15 条）、股权代持/对赌、外商投资准入、反垄断申报、涉诉（裁判文书网）、社保欠缴、环评。
- **输出去向。** 落在 `./out/`，经部署流水线接到交易文件夹。不要给 `grid-writer` 上传用的 MCP；交接给上传步骤更干净，保持 Write 层隔离。
- **请求清单类目。** 监控模式对照部署团队 corporate-legal-cn 的 `CLAUDE.md` 配置分类。接入实盘交易前先在那里重跑 `/corporate-legal-cn:cold-start-interview`。
- **作品文档头。** `grid-writer` 前置部署团队 `## 输出` 配置里的文档头。部署前与法务确认（律师 vs 非律师头不同）。
- **推送路由。** 本 agent 从不直接推送。报告是文件；`handoff_request` 告诉 orchestrator 路由到哪个渠道。
