---
name: investigation-summary
description: >
  从保密调查备忘录起草面向对象的摘要——HR 版、管理层版或外部律师版。
  触发场景：调查备忘录需要传达给不该看到完整保密工作成果的对象。
argument-hint: "[事项名] [对象：hr / leadership / outside-counsel]"
---

# /investigation-summary

从保密调查备忘录起草一份精简的、面向具体对象的摘要。HR 摘要不含保密分析。管理层摘要为高层级。外部律师简报含完整背景。

## 说明

1. 加载 `internal-investigation` 参考技能并跑模式 5（面向对象摘要）。
2. 若还没有备忘录，提供先起草备忘录。
3. HR 摘要不得包含律师内心判断、可信度方法或法律风险分析。

## 示例

```
/employment-legal-cn:investigation-summary [事项名] hr
```

```
/employment-legal-cn:investigation-summary [事项名] leadership
```

```
/employment-legal-cn:investigation-summary [事项名] outside-counsel
```

> 详细的对象裁剪规则和摘要模板在 `internal-investigation` 参考技能里——做实质工作前先加载它。
