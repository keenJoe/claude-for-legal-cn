---
name: uninstall
description: >
  卸载通过 hub 安装的社区技能。删除文件前确认，拒绝触碰第一方插件技能，每一步都记录日志。
  触发场景：用户想彻底移除某个社区技能（「卸载 [技能]」「把这个技能删掉」），而不是仅仅停用。
argument-hint: "[技能名]"
---

# /uninstall

对指定的技能运行 skill-manager 参考技能中的 uninstall 工作流。

安全规则：

1. **只卸载通过本 hub 安装的社区技能。** 检查 `~/.claude/plugins/config/claude-for-legal-cn/legal-builder-hub-cn/install-log.yaml` 与 CLAUDE.md 的已安装清单。若该技能没有记录，拒绝并告知用户。
2. **绝不卸载第一方插件的技能。** claude-for-legal 自带的 12 个核心插件对本命令来说是禁区。若指定的技能解析到这些插件内的路径，拒绝。
3. **删除文件前确认。** 向用户展示将要删除的每一个路径。仅在明确 `yes` 后继续。
4. **记录卸载。** 在 `install-log.yaml` 追加 `action: uninstall` 和时间戳，保持审计轨迹完整。

如果用户想停止技能运行但保留文件（例如为了以后重新启用，或保留配置），建议改用 `/legal-builder-hub-cn:disable`。

> 详细的卸载、停用与重新启用工作流在 `skill-manager` 参考技能中 —— 做实质工作前先加载它。

## 转换说明（质量自检）

- **A 级直转**：卸载限制（仅 hub 安装的社区技能）、第一方插件禁区、确认后删除、日志记录，全部原样保留。
- **B 级大改**：路径改为 `claude-for-legal-cn/legal-builder-hub-cn`；命令改为 `/legal-builder-hub-cn:uninstall`。
- **D 级新增**：无。
- **明确不做**：不涉及实体法内容；安全机制保留。
