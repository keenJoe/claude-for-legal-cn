---
name: registry-browser
description: >
  在被监控的技能仓库中搜索社区法务技能，展示匹配结果及描述，安装前可先查看完整 SKILL.md。
  触发场景：用户说「浏览」「找技能」「找找有没有 [X] 的技能」「社区里都有什么」，
  或想往监控清单里加一个新仓库。
argument-hint: "[搜索词]"
---

# /registry-browser

1. 读取 `~/.claude/plugins/config/claude-for-legal-cn/legal-builder-hub-cn/CLAUDE.md` → 被监控的仓库。
2. 按下方工作流执行。
3. 搜索每个仓库。展示带描述的匹配结果。
4. 对任一匹配，可提供查看完整 SKILL.md。

---

## 目的

在被监控的仓库中找到技能。搜索、预览、决定。

## 加载上下文

`~/.claude/plugins/config/claude-for-legal-cn/legal-builder-hub-cn/CLAUDE.md` → 被监控仓库清单。

## 工作流

### 第 1 步：抓取仓库索引

对每个被监控仓库：

- GitHub 仓库（含 gitee 镜像）：抓取 `skills/` 目录清单与每个 `SKILL.md` 的 frontmatter（name + description）。
- 市场式仓库：抓取索引。

将索引缓存到本地（`references/registry-cache.json`）以便快速浏览。缓存超过 7 天或用户要求时刷新。

### 第 2 步：搜索

用查询词匹配技能名称与描述。简单的关键词匹配即可 —— 量小，模糊搜索是多余的。

如果仓库按类别组织，也支持按类别浏览。

### 第 3 步：展示匹配结果

```markdown
## 搜索：「[查询词]」

**在 [M] 个仓库中找到 [N] 个技能：**

### [技能名]
**来自：** [仓库名]
**描述：** [来自 frontmatter]
[查看完整 SKILL.md] [安装]

### [技能名]
[...]
```

### 第 4 步：预览

「查看完整 SKILL.md」：抓取并展示整个文件。用户在决定安装前先读一遍。没有惊喜。

### 第 5 步：添加仓库

如果用户有不在监控清单中的仓库 URL：

1. 抓取它，验证确实是技能仓库（有 `skills/` 或 `.claude-plugin/`）
2. 展示里面有什么
3. 确认后加入 `~/.claude/plugins/config/claude-for-legal-cn/legal-builder-hub-cn/CLAUDE.md` → 被监控仓库

## 默认仓库

- **lpm-skills**（github.com/legalopsconsulting/lpm-skills）—— 法律项目管理技能（mirror 见 gitee 镜像），领域无关，良好起点。
- 其余在生态成长过程中添加。国内技能仓库（GitHub 中国镜像 / gitee / 国内技能市场）经用户确认后加入白名单。

## 本技能不做的事

- 不安装任何东西。只浏览，由 skill-installer 负责安装。
- 不评分或评审技能。展示 SKILL.md，由用户判断。
- 不搜索整个互联网。只搜被监控的仓库。

## 转换说明（质量自检）

- **A 级直转**：浏览/缓存/搜索/预览/添加仓库的工作流原样保留；「只看被监控仓库、不搜全网」的边界保留。
- **B 级大改**：路径改为 `claude-for-legal-cn/legal-builder-hub-cn`；命令改为 `/legal-builder-hub-cn:registry-browser`；默认仓库说明补充中国镜像（gitee / 国内技能市场），白名单默认制。
- **D 级新增**：无。
- **明确不做**：不涉及实体法内容；安装与安全机制不在此技能，保持纯净浏览职责。
