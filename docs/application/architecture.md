# ATMQuant - 技术架构

**日期：** 2026-03-17

## 架构概览

ATMQuant 是基于 vnpy 4.1 的桌面量化交易应用，采用**事件驱动 + 插件化**架构：EventEngine 负责事件分发，MainEngine 管理网关与 App，各功能以 App（如 CtaStrategyApp、CtaBacktesterApp、ChartWizardApp）形式挂载。

## 技术栈与版本

| 类别 | 技术 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 类型注解、现代语法 |
| GUI | PySide6 6.8.2.1 | Qt6 绑定 |
| 图表 | pyqtgraph ≥0.13.7 | K 线、指标绘图 |
| 框架 | vnpy 4.1 | 事件引擎、主引擎、交易、图表基类 |
| 数值 | numpy, pandas ≥2.2.3 | 数据处理与指标计算 |
| 指标库 | TA-Lib ≥0.6.4 | 部分指标底层计算 |
| 配置 | python-dotenv ≥1.0.0 | .env 加载 |
| 日志 | loguru ≥0.7.3 | 异步日志、按品种/策略 |
| 数据库 | SQLAlchemy ≥2.0.0 | 默认 SQLite，可选 MySQL（vnpy_mysql） |
| 数据源 | vnpy_tushare / vnpy_akshare / vnpy_tqsdk | 与 .env DATAFEED_NAME 对应 |
| 测试 | pytest, pytest-cov | 单元/集成/回测测试 |

## 架构模式

- **事件驱动：** 各模块通过 EventEngine 发布/订阅事件（如 `EVENT_CHART_HISTORY`），解耦数据生产与消费。
- **插件化：** 交易（CtpGateway）、策略（CtaStrategyApp）、回测（CtaBacktesterApp）、图表（ChartWizardApp）等以引擎/App 形式注册到 MainEngine。
- **分层：** 界面层（MainWindow、各 App UI）→ 引擎层（MainEngine、各 App Engine）→ 网关/数据源/数据库。

## 数据架构

- **配置：** `.env` → `config/settings.py` 的 `apply_settings()` 写入 vnpy `SETTINGS`（数据库、数据源、日志、邮件等）。
- **K 线：** 历史数据由 datafeed 或 database 提供，ChartWizardEngine 查询后通过事件推送；实时由 CTP 等网关 tick 驱动。
- **交易记录：** `core/models/trade_models.py` 定义 `TradeData`（SQLAlchemy），支持实盘与回测记录，可持久化到 MySQL。

## 组件与集成

- **图表：** `core/charts/EnhancedChartWidget` 继承 vnpy `ChartWidget`，集成主图/副图指标、扩展指标配置、ExtendableViewBox、CursorManager；ChartWizard 在运行时使用该组件并接收历史数据事件。
- **策略：** `core/strategies/BaseCtaStrategy` 继承 vnpy `CtaTemplate`，统一交易时段识别、日志与告警；具体策略（如 TripleMaStrategy）继承 BaseCtaStrategy。
- **指标：** `core/indicators` 下各 `*_item.py` 实现 vnpy `ChartItem` 与 `ConfigurableIndicator`，在 EnhancedChartWidget 中注册；扩展指标通过 `EXTENDED_INDICATORS_CONFIG` 动态加载。

## 源码结构（关键路径）

- **入口：** `main.py`
- **核心：** `core/`（charts、indicators、data、logging、strategies、models）
- **配置：** `config/`
- **插件：** `vnpy_*`（ctp、ctastrategy、ctabacktester、chartwizard、datamanager、mysql、数据源、spreadtrading）
- **框架：** `vnpy/`（event、trader、chart）

## 开发与运行

- 环境：Python 3.10+，`pip install -r requirements.txt`，复制并编辑 `.env`。
- 启动：`python main.py`（自动加载 .env）。
- 测试：`pytest` / `pytest tests/unit -v` / `pytest tests/ --cov=core --cov-report=term-missing`。

## 部署与扩展

- 当前以本地桌面运行为主；无独立 REST API，无容器化配置在仓库内。
- 扩展方式：新增 vnpy App、在 `main.py` 中 `add_app`；新增指标在 `core/indicators` 并（可选）加入 `EXTENDED_INDICATORS_CONFIG`；新增策略继承 `BaseCtaStrategy`。

---

_由 BMAD document-project 工作流生成_
