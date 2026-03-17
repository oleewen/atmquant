# ATMQuant - 项目概览

**日期：** 2026-03-17  
**类型：** 单体应用（Desktop/量化交易）  
**架构：** 基于 vnpy 4.1 的插件化桌面应用

## 执行摘要

ATMQuant 是基于 vnpy 4.1 的开源 AI 量化交易框架，专注于图表可视化与策略研发。采用 Python 3.10+、PySide6 构建桌面 GUI，通过事件引擎与主引擎串联 CTP 交易、CTA 策略、回测与 K 线图表等模块，支持多周期图表、技术指标库、策略开发与回测、轻量配置与日志告警。

## 项目分类

- **仓库类型：** 单体（Monolith）
- **项目类型：** 桌面/后端混合（Python + PySide6 GUI，量化交易）
- **主要语言：** Python 3.10+
- **架构模式：** 事件驱动 + 插件化（vnpy MainEngine + App）

## 技术栈摘要

| 类别     | 技术           | 版本/说明 |
|----------|----------------|-----------|
| 语言     | Python         | 3.10+     |
| GUI      | PySide6        | 6.8.2.1   |
| 图表     | pyqtgraph      | ≥0.13.7   |
| 框架     | vnpy           | 4.1       |
| 数据     | numpy, pandas   | ≥2.2.3    |
| 指标     | TA-Lib         | ≥0.6.4    |
| 配置     | python-dotenv  | ≥1.0.0    |
| 日志     | loguru         | ≥0.7.3    |
| 数据库   | SQLAlchemy     | ≥2.0.0，默认 SQLite，可选 MySQL |
| 数据源   | vnpy_tushare / akshare | 与 .env 中 DATAFEED_NAME 对应 |
| 测试     | pytest, pytest-cov | ≥7.4.0 |

## 核心能力

- **多周期图表系统**：双图/四图视图，多时间框架对比；增强版 K 线组件（主图/副图指标、可配置、X 轴延伸、专注模式）。
- **技术指标库**：BOLL、SMA、EMA、MACD、RSI、DMI、成交量等；扩展指标（斐波那契、ZLEMA、SuperTrend、Squeeze、WaveTrend 等）动态加载。
- **策略开发与回测**：基于 CtaTemplate 的 BaseCtaStrategy，支持交易时段识别、日志与告警；回测引擎与增强回测界面。
- **轻量配置与日志告警**：`.env` + `config/settings.py` 覆盖 vnpy 配置；loguru 日志、飞书/钉钉告警机器人。

## 架构要点

- **入口：** `main.py` → 加载配置 → 创建 EventEngine、MainEngine → 注册 CtpGateway、CtaStrategyApp、CtaBacktesterApp、ChartWizardApp → MainWindow。
- **核心目录：** `core/`（charts、indicators、data、logging、strategies）、`config/`、`vnpy_*` 插件（ctp、ctastrategy、ctabacktester、chartwizard、datamanager、mysql、tushare、akshare、tqsdk、spreadtrading）。
- **数据流：** 数据源/数据库 → ChartWizardEngine 查询历史 K 线 → 事件推送 → 图表与策略消费。

## 开发概览

### 环境要求

- Python 3.10+
- 虚拟环境建议：`python3 -m venv venv && source venv/bin/activate`
- 依赖：`pip install -r requirements.txt`
- 配置：复制 `.env.example` 为 `.env` 并填写（数据库、数据源、告警等）

### 常用命令

- **启动：** `python main.py`
- **测试：** `pytest` / `pytest tests/unit -v` / `pytest tests/ --cov=core --cov-report=term-missing`

### 文档地图

- [index.md](./index.md) - 文档索引
- [architecture.md](./architecture.md) - 技术架构
- [source-tree-analysis.md](./source-tree-analysis.md) - 目录结构
- [development-guide.md](./development-guide.md) - 开发与测试
- [component-inventory.md](./component-inventory.md) - 组件与指标清单
- [data-models.md](./data-models.md) - 数据模型

---

_由 BMAD document-project 工作流生成_
