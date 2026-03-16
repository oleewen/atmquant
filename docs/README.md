# ATMQuant 文档中心

本仓库以 **`docs/`** 为文档中心，采用「四视角 + 宪法层」的知识库结构，与 SDD（解决方案→需求分析→需求交付）工作流配合。

## 快速导航

| 文档 | 说明 |
|------|------|
| [**知识库全局索引**](./INDEX.md) | 各类文档入口、示例与映射速查 |
| [**业务知识**](./knowledge/README.md) | 宪法层、业务/产品/技术/数据四视角 |
| [**解决方案**](./solutions/README.md) | 解决方案文档（SOLUTION-{ID}.md） |
| [**需求分析**](./analysis/README.md) | 需求分析文档（REQUIREMENT-{ID}.md） |
| [**需求交付**](./requirements/README.md) | 按 MVP 阶段的 PRD/ADD/TDD 交付 |

## 目录结构

```text
docs/
├── knowledge/         # 知识库（四视角 + 宪法层）
│   ├── constitution/  # 宪法层：ADR、术语表、命名与架构原则
│   ├── business/      # 业务视角：BD-ATMQUANT、子域、限界上下文
│   ├── product/      # 产品视角：PL-ATMQUANT、模块与功能
│   ├── technical/    # 技术视角：SYS-ATMQUANT、模块与实现
│   └── data/         # 数据视角：数据存储与实体
├── solutions/        # 解决方案文档
├── analysis/         # 需求分析文档
├── requirements/     # 需求交付文档（按 REQUIREMENT-{ID}/）
└── INDEX.md          # 全局索引与映射速查
```

## 设计原则

- **单一事实源 (SSOT)**：每个知识点只在一处定义，其他地方通过 ID 引用。
- **可追溯性**：业务、产品、技术、数据四视角通过 ID 显式关联（如 `implemented_by_app_id`、`relies_on_context_ids`）。

## 参考

- 项目概述与启动：仓库根目录 [README.md](../README.md)
- Agent 指南：仓库根目录 [AGENTS.md](../AGENTS.md)
- 知识库索引：本目录 [INDEX.md](./INDEX.md)
