# SYS-ATMQUANT 应用架构（ATMQuant）

## 元信息

| 属性 | 值 |
|------|-----|
| 系统 ID | SYS-ATMQUANT |
| 架构风格 | 单体桌面应用（事件驱动 + 插件化） |
| 入口 | `main.py` |
| 关键文档 | `docs/INDEX.md`、`docs/application/architecture.md`、`docs/application/source-tree-analysis.md` |

## 架构概览

ATMQuant 以 **vnpy 4.1** 为核心框架：`EventEngine` 负责事件分发，`MainEngine` 作为主引擎管理网关与 App；应用以桌面 GUI 形式运行（PySide6），并通过 `MainWindow` 聚合各插件界面。

### 运行时组件

| 组件 | 作用 | 主要位置 |
|---|---|---|
| 配置注入 | `.env` → vnpy `SETTINGS` | `config/settings.py` |
| 事件引擎 | 事件发布/订阅与派发 | `vnpy.event.EventEngine`（外部依赖） |
| 主引擎 | 管理网关与 App，承载插件 | `vnpy.trader.engine.MainEngine`（外部依赖） |
| GUI 主窗口 | 聚合各 App UI | `vnpy.trader.ui.MainWindow`（外部依赖） |
| CTP 网关 | 期货交易/行情接入 | `vnpy_ctp`（外部依赖目录） |
| CTA 策略 | 策略运行与管理 | `vnpy_ctastrategy`（外部依赖目录） + `core/strategies` |
| 回测 | 回测引擎与界面 | `vnpy_ctabacktester`（外部依赖目录） |
| 图表 | K 线图表 App + 增强图表组件 | `vnpy_chartwizard`（外部依赖目录） + `core/charts` |

## 模块边界（仓库内）

| 模块 | 职责边界 | 关键文件 |
|---|---|---|
| `core/charts` | 图表容器、双图/四图、交互组件 | `core/charts/enhanced_chart_widget.py` |
| `core/indicators` | 技术指标实现与可配置能力 | `core/indicators/indicator_base.py` |
| `core/strategies` | 策略基类与示例策略 | `core/strategies/base_strategy.py` |
| `core/data` | 数据下载与写库、合约处理 | `core/data/downloader.py` |
| `core/logging` | 日志管理与告警适配 | `core/logging/logger_manager.py` |
| `core/models` | 交易/回测相关持久化模型 | `core/models/trade_models.py` |
| `config` | `.env`、告警、插件、交易时段等配置 | `config/settings.py`、`config/trading_sessions_config.py` |

## 关键调用链（摘要）

### 启动链路

`main.py` → `config/settings.py::apply_settings()` → `EventEngine` → `MainEngine` → `add_gateway(CtpGateway)` → `add_app(...)` → `MainWindow` → Qt 事件循环

### 图表与指标扩展点

`core/charts/enhanced_chart_widget.py` 内通过 `EXTENDED_INDICATORS_CONFIG` 动态导入扩展指标模块；模块缺失时按设计静默跳过，避免阻塞启动。

## 进一步阅读

- AI 索引地图：`docs/INDEX.md`
- ATMQuant 工程文档：`docs/application/INDEX.md`

