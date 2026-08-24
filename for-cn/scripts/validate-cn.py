#!/usr/bin/env python3
"""claude-for-legal-cn 校验：
1. marketplace.json + 每个插件 plugin.json 合法性（JSON 可解析 + 必需字段）
2. 各插件目录结构完整性（CLAUDE.md / hooks.json / .gitignore 存在）
3. 英美法残留扫描：在中文版内检测不应出现在实体法层的英美法概念
4. frontmatter 完整性：每个 SKILL.md 有 name + description
"""
import json, glob, os, re, sys, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
CN = os.path.join(ROOT, "..")

# 第三类：只在"跨法域提示"语境下允许出现；出现在正文（法条引用/流程）视为残留。
US_TERMS = [
    "at-will", "FMLA", "CFRA", "PFL", "ADA ", "GDPR", "CCPA", "HIPAA",
    "Westlaw", "Delaware", "FRE 408", "FRCP", "Fed.R.Evid",
    "uncapped", "SOC 2", "SEC ", "DOJ", "FTC", "FDA", "HLT",
    "state test", "Bar exam", "bar exam", "SCC", "adequacy",
    "attorney work product", "PRIVILEGED & CONFIDENTIAL", "common law",
    "motion to dismiss", "summary judgment", "discovery",
]
EXEMPT_SECTION = ["跨法域", "Cross-border", "cross-border"]

errors = []

# 1. marketplace
mp = json.load(open(os.path.join(CN, ".claude-plugin/marketplace.json")))
names = [p["name"] for p in mp["plugins"]]
if len(names) != len(set(names)):
    errors.append("marketplace: 插件名重复")
for p in mp["plugins"]:
    src = p.get("source", "")
    if src and not src.startswith("./"):
        errors.append(f"marketplace: {p['name']} source 不是相对路径: {src}")
    d = os.path.join(CN, src[2:]) if src.startswith("./") else None
    if d and not os.path.exists(os.path.join(d, ".claude-plugin/plugin.json")):
        errors.append(f"marketplace: {p['name']} 缺少 .claude-plugin/plugin.json")
    for f in ("name", "description", "author"):
        if not p.get(f):
            errors.append(f"marketplace: {p['name']} 缺 {f}")
    if not re.match(r"^[a-z0-9][a-z0-9-]{1,63}$", p["name"]):
        errors.append(f"marketplace: {p['name']} 不符合 I11 命名")

# 2. 每个插件目录
for d in sorted(glob.glob(os.path.join(CN, "*-cn"))):
    base = os.path.basename(d)
    pj = os.path.join(d, ".claude-plugin/plugin.json")
    if not os.path.exists(pj):
        errors.append(f"{base}: 缺 plugin.json")
        continue
    p = json.load(open(pj))
    if not re.match(r"^[a-z0-9][a-z0-9-]{1,63}$", p.get("name", "")):
        errors.append(f"{base}: plugin.json name 不符合 I11")
    if p.get("name") != base:
        errors.append(f"{base}: plugin.json name 与目录名不一致 ({p.get('name')})")
    in_mp = any(x["name"] == p.get("name") for x in mp["plugins"])
    if not in_mp:
        errors.append(f"{base}: 未在 marketplace 中登记")
    for req in ("CLAUDE.md", "hooks/hooks.json", ".gitignore"):
        if not os.path.exists(os.path.join(d, req)):
            errors.append(f"{base}: 缺 {req}")
    # hooks.json 必须是合法 JSON 对象
    try:
        h = json.load(open(os.path.join(d, "hooks/hooks.json")))
        if not isinstance(h, dict):
            errors.append(f"{base}: hooks.json 不是对象")
    except Exception as e:
        errors.append(f"{base}: hooks.json 解析失败 {e}")

# 3. SKILL.md frontmatter + 英美法残留
all_skills = glob.glob(os.path.join(CN, "*-cn/skills/*/SKILL.md"))
for s in sorted(all_skills):
    rel = os.path.relpath(s, CN)
    txt = open(s, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        errors.append(f"{rel}: 缺 frontmatter")
        continue
    fm = m.group(1)
    if "name:" not in fm or "description:" not in fm:
        errors.append(f"{rel}: frontmatter 缺 name/description")
    # 探头扫描：剔除豁免段落后查英美法残留
    # 豁免章节：明确标注为跨法域/映射说明/转换决策/自检的段落
    body = txt
    for ex in ("## 跨法域", "## Cross-border", "跨法域提示", "本 skill 不做的事",
               "## 转换决策", "## 转换说明", "**分级：**", "**主要变化：**",
               "## 本 skill 不做", "## 转换自检", "## 自检",
               "跨法域识别", "转换决策记录"):
        body = body.split(ex)[0] if ex in body else body
    # 逐行扫描：跳过明显的映射行（含 → 或 -> 且左右都是术语对照）
    body_lines = []
    for line in body.split("\n"):
        # 映射行豁免：含 → 或 -> 且行首缩进项目符号（列表/表格内的对照）
        if ("→" in line or " -> " in line) and re.search(r"^\s*[-*|]|\|", line):
            continue
        # 跨法域说明豁免：句中含「中国无美国」「英美法的」「美国...概念」等对照句式
        if re.search(r"中国无(美国|英美)|英美法的|美国意义上的|中国法下不存在|中国法下(没|无)", line):
            continue
        body_lines.append(line)
    body_filtered = "\n".join(body_lines)
    for term in US_TERMS:
        if term in body_filtered:
            errors.append(f"{rel}: 残留英美法概念「{term.strip()}」")

# 4. 报告
if errors:
    print(f"✘ {len(errors)} 个问题：")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"✔ 全部通过（{len(mp['plugins'])} 个插件，{len(all_skills)} 个技能）")
