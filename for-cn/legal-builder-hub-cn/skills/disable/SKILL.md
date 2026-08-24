---
name: disable
description: >
  停用通过 hub 安装的社区技能但不删除其文件。触发场景：用户想临时静默某个社区技能
  （「停用 [技能]」）、在保留配置的情况下停止其 hook 触发，或重新启用之前停用的技能。
argument-hint: "[技能名]"
---

# /disable

对指定的技能运行 skill-manager 参考技能中的 disable 工作流。

disable 做什么：

- 将技能的 `SKILL.md` 重命名为 `SKILL.md.disabled`，使 Claude 不再把它当作活动技能发现。文件、references、模板与配置原样保留。
- 如果技能自带 `hooks/hooks.json`，同样重命名为 `hooks.json.disabled`，使技能停用期间没有任何自动触发。
- 将操作记录到 `~/.claude/plugins/config/claude-for-legal-cn/legal-builder-hub-cn/install-log.yaml`。

安全规则：

1. **只停用通过本 hub 安装的社区技能。** 与 uninstall 相同的检查 —— 查阅安装日志与 CLAUDE.md 的已安装清单。
2. **绝不停用第一方插件的技能。** 禁区。
3. **重命名前先确认。** 展示将改动的路径，获得明确的 `yes`。

再次运行同一命令并输入相同技能名即可重新启用 —— skill-manager 工作流会识别已停用的技能并翻转重命名。

> 详细的卸载、停用与重新启用工作流在 `skill-manager` 参考技能中 —— 做实质工作前先加载它。

## 转换说明（质量自检）

- **A 级直转**：停用/重命名/记录逻辑、安全规则（只动 hub 安装的社区技能、不动第一方插件）原样保留。
- **B 级大改**：路径改为 `claude-for-legal-cn/legal-builder-hub-cn`；命令改为 `/legal-builder-hub-cn:disable`。
- **D 级新增**：无。
- **明确不做**：不涉及实体法内容；安全机制保留。
