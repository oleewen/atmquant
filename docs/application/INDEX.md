# ATMQuant 工程文档索引

**类型：** 单体应用（Desktop/量化交易）  
**主要语言：** Python 3.10+  
**架构：** 事件驱动 + 插件化（vnpy 4.1）  
**更新日期：** 2026-03-17

## 项目概览

ATMQuant 是基于 vnpy 4.1 的开源 AI 量化交易框架，侧重图表可视化与策略研发，提供多周期图表、技术指标库、策略开发与回测、轻量配置与日志告警。

## 快速参考

- **技术栈：** Python 3.10+、PySide6、pyqtgraph、vnpy 4.1、numpy/pandas、TA-Lib、loguru、SQLAlchemy
- **入口：** `main.py`
- **架构模式：** 事件驱动 + 插件化（MainEngine + App）
- **数据库：** 默认 SQLite，可选 MySQL
- **配置：** `.env` + `config/settings.py`

## 生成的文档

### 核心文档

- [项目概览](./project-overview.md) - 执行摘要、技术栈、核心能力与文档地图
- [源码树分析](./source-tree-analysis.md) - 带注释的目录树与关键目录说明
- [技术架构](./architecture.md) - 架构模式、数据架构、组件与集成
- [组件与指标清单](./component-inventory.md) - 图表组件、技术指标、策略、配置与 vnpy 插件
- [开发指南](./development-guide.md) - 环境、运行、测试与常用开发任务
- [数据模型](./data-models.md) - TradeData 及交易相关模型与接口

### 已有文档（仓库内）

- [项目 README](../README.md) - 项目说明与快速开始
- [文档中心](./README.md) - 文档中心与知识库结构
- [AGENTS.md](../AGENTS.md) - Agent 与开发规范

## 入门步骤

1. **环境：** Python 3.10+，`pip install -r requirements.txt`，`cp .env.example .env` 并编辑。
2. **运行：** `python main.py`。
3. **测试：** `pytest` 或 `pytest tests/unit -v`。

## 面向 AI 辅助开发

- **仅改图表/指标：** 参考 `architecture.md`、`component-inventory.md` 与 `core/charts`、`core/indicators`。
- **改策略/回测：** 参考 `architecture.md`、`component-inventory.md` 与 `core/strategies`、vnpy_ctastrategy、vnpy_ctabacktester。
- **改配置/数据/日志：** 参考 `config/`、`core/logging`、`core/data`、`data-models.md`。
- **全栈理解：** 从 `index.md` → `project-overview.md` → `architecture.md` → `source-tree-analysis.md` 与各专项文档。

---

_由 BMAD Method document-project 工作流生成_
