# 📘 AI文档库精要索引指南
> 生成时间：2026-03-18  |  执行模式：Mode 3（精读抽样 + 覆盖声明）  |  索引覆盖率：已精读/抽样约 40+ 关键文件；其余路径见 §6「未索引区域声明」

本索引面向 **AI Agent / RAG 检索**：强调 **路径精确、标签受控、依赖方向、数据流与配置入口**。  
硬性约束：只索引已读取文件；未读取的路径均标注为 `[未索引]`。

---

## 1. 全局元信息

- **项目名称**：ATMQuant
- **核心定位（≤30字）**：基于 vnpy 的桌面量化交易与图表策略框架
- **项目形态**：Python 单体桌面应用（PySide6 GUI）+ 内置文档/知识库体系（AI-SDD）
- **技术栈**
  - **语言**：Python 3.10+
  - **框架**：vnpy 4.1
  - **GUI/图表**：PySide6、pyqtgraph、vnpy.chart
  - **数据/指标**：numpy、pandas、TA-Lib
  - **数据库**：SQLAlchemy、PyMySQL（可选 `vnpy_mysql`）
  - **日志/告警**：loguru；飞书/钉钉机器人（webhook）
  - **测试**：pytest、pytest-cov
- **关键外部依赖（3–8）**
  - `vnpy` / `vnpy_ctp` / `vnpy_ctastrategy` / `vnpy_ctabacktester` / `vnpy_chartwizard`
  - `PySide6`
  - `pyqtgraph`
  - `sqlalchemy`
  - `loguru`
  - `python-dotenv`（仓库内采用自读 `.env` 的方式）
- **入口**
  - **应用入口**：`./main.py`
  - **配置注入**：`./config/settings.py` 的 `apply_settings()`
  - **核心图表组件**：`./core/charts/enhanced_chart_widget.py`
  - **策略基类**：`./core/strategies/base_strategy.py`
- **构建/启动命令**
  - **安装依赖**：`pip install -r requirements.txt`
  - **启动**：`python main.py`
  - **测试**：`pytest`（更多见 `./tests/README.md`）
- **文档入口**
  - **应用文档（ATMQuant）**：`./docs/application/INDEX.md`
  - **系统文档（知识库/SDD）**：`./docs/system/INDEX.md`
  - **根 README**：`./README.md`
  - **注意**：`./docs/README.md` 当前不存在（已搜索未找到）

---

## 2. 架构拓扑

### 2.1 目录树（带语义注释）

> 仅包含已读取/已确认的关键路径；其余见 §6。

```text
./
├── README.md                              # 项目介绍、快速开始、模块概览、系列文章索引
├── AGENTS.md                              # Agent 行为约束、关键路径、命令、规范指引
├── requirements.txt                       # Python 依赖清单（含 GUI/指标/数据库/测试）
├── .env.example                           # 环境变量示例：数据库/数据源/邮件/告警
├── main.py                                # 启动入口：apply_settings → EventEngine/MainEngine → add_gateway/add_app → MainWindow
├── config/
│   ├── settings.py                        # 读取 .env 并写入 vnpy SETTINGS（email/datafeed/database/log/font）
│   ├── alert_config.py                    # 告警渠道配置（飞书/钉钉）+ 告警级别/静音规则
│   ├── plugin_settings.py                 # CTP 连接配置（CTP_*；默认 SimNow 地址）
│   ├── futures_config.py                  # 期货品种参数字典 FUTURES_INFO（合约乘数/保证金/手续费等）
│   └── trading_sessions_config.py         # 全球市场交易时段（小时/半小时/日线结束时间）+ 品种识别
├── core/
│   ├── charts/
│   │   ├── enhanced_chart_widget.py       # EnhancedChartWidget：主/副图指标、扩展指标动态加载、光标/视图组件
│   │   └── components/                    # CursorManager、ExtendableViewBox（见 README.md/源码树分析）
│   ├── indicators/
│   │   └── indicator_base.py              # ConfigurableIndicator：通用配置对话框/应用配置协议
│   ├── strategies/
│   │   └── base_strategy.py               # BaseCtaStrategy：交易时段识别、日志、告警封装
│   ├── logging/
│   │   └── logger_manager.py              # loguru 初始化、文件轮转、bind(symbol) 输出
│   ├── data/
│   │   └── downloader.py                  # FuturesDataDownloader：tqsdk 拉取 → vnpy database 写入
│   └── models/
│       └── trade_models.py                # SQLAlchemy TradeData + 查询/保存函数（兼容 vnpy_mysql）
├── tests/
│   └── README.md                          # pytest/脚本运行说明与注意事项
└── docs/
    ├── application/
    │   ├── INDEX.md                       # 应用文档索引入口
    │   ├── README.md                      # 应用知识库（联邦单元）说明（偏 AI-SDD 模板）
    │   ├── project-overview.md            # ATMQuant 项目概览（BMAD 生成）
    │   ├── architecture.md                # ATMQuant 技术架构（BMAD 生成）
    │   ├── source-tree-analysis.md         # ATMQuant 源码树分析（BMAD 生成）
    │   ├── development-guide.md           # 开发/测试/配置说明（BMAD 生成）
    │   ├── component-inventory.md         # 指标/组件清单（BMAD 生成）
    │   └── data-models.md                 # 数据模型说明（BMAD 生成）
    ├── documents/
    │   ├── README.md                      # documents 区域说明（已读）
    │   └── INDEX.md                       # documents 区域索引（已读）
    └── system/
        ├── INDEX.md                       # 系统级知识库/solutions/analysis/requirements/specs 索引
        ├── README.md                      # system 文档根说明
        ├── DESIGN.md                      # 知识库设计方案摘录（SSOT/联邦治理/四视角）
        ├── CONTRIBUTING.md                # 知识库贡献与引用规则
        └── knowledge/
            ├── README.md                  # knowledge 总说明（视角入口、引用与追溯）
            ├── constitution/              # 宪法层：术语表/命名/ADR/原则（抽样精读）
            ├── business/                  # 业务视角：BD/BSD/BC/AGG（抽样精读）
            ├── product/                   # 产品视角：PL/PM/FT/UC（抽样精读）
            ├── technical/                 # 技术视角：SYS/APP/MS（抽样精读）
            └── data/                      # 数据视角：DS/ENT（抽样精读）
```

### 2.2 模块依赖方向图（A → B）

#### ATMQuant 应用（运行时依赖）

- `./main.py` → `./config/settings.py`（配置注入）
- `./main.py` → `vnpy.event.EventEngine` → `vnpy.trader.engine.MainEngine`
- `./main.py` → `vnpy_ctp.CtpGateway`
- `./main.py` → `vnpy_ctastrategy.CtaStrategyApp`
- `./main.py` → `vnpy_ctabacktester.CtaBacktesterApp`
- `./main.py` → `vnpy_chartwizard.ChartWizardApp`
- `./core/charts/enhanced_chart_widget.py` → `./core/indicators/*`（基础指标 + 扩展指标动态导入）
- `./core/strategies/base_strategy.py` → `./config/trading_sessions_config.py`（交易时段）
- `./core/strategies/base_strategy.py` → `./core/logging/logger_manager.py`（日志）
- `./core/strategies/base_strategy.py` → `./core/logging/alert_manager.py`（告警，文件未读：见 §6）
- `./core/data/downloader.py` → `vnpy.trader.database.get_database` → DB（写入 BarData）
- `./core/models/trade_models.py` → `vnpy_mysql.mysql_database`（可选）否则 → `sqlalchemy.create_engine(mysql+pymysql://...)`

#### 文档/知识库体系（依赖关系）

- `./docs/system/INDEX.md` → `./docs/system/DESIGN.md`、`./docs/system/CONTRIBUTING.md`、`./docs/system/knowledge/**`
- `./docs/system/knowledge/constitution/adr/*` 定义全局治理决策 → 约束 `knowledge` 各视角目录结构
- `./.ai/workflows.yaml` + `./.ai/agents.yaml` + `./.ai/context/project-context.yaml` → 定义 AI-SDD 流程与上下文加载策略

---

## 3. 详细索引字典

### 3.0 全局标签词表（≤30）

**应用侧（ATMQuant）**
- `entrypoint`（启动入口）
- `config`（配置注入/.env）
- `vnpy`（vnpy 主引擎/事件）
- `gateway-ctp`（CTP 网关）
- `app-chartwizard`（K线图表 App）
- `app-cta`（CTA 策略 App）
- `app-backtest`（回测 App）
- `chart-widget`（增强图表组件）
- `indicator`（技术指标）
- `indicator-config`（指标可配置对话框）
- `strategy`（策略基类/示例）
- `trading-session`（交易时段/日线收盘时间）
- `data-download`（数据下载/写库）
- `db`（数据库/ORM）
- `logging`（日志）
- `alert`（告警）
- `tests`（测试）

**文档/知识库侧（AI-SDD）**
- `docs-index`（文档索引入口）
- `knowledge`（知识库）
- `constitution`（宪法/治理）
- `adr`（架构决策记录）
- `naming`（ID命名规范）
- `glossary`（术语表）
- `business-view`（业务视角）
- `product-view`（产品视角）
- `technical-view`（技术视角）
- `data-view`（数据视角）
- `mapping`（跨视角映射字段）
- `workflow-sdd`（AI-SDD 工作流）

### 3.1 模块：ATMQuant 应用代码

| 文件路径 | 功能精要 | 检索标签 | 上游依赖 | 下游被依赖 | 重要度 |
|---|---|---|---|---|---|
| `./main.py` | 启动引擎与注册网关/插件 | `entrypoint`,`vnpy` | `./config/settings.py` | GUI 全链路 | ⭐⭐⭐ |
| `./requirements.txt` | 依赖版本边界与可选数据源 | `config` | - | 环境搭建 | ⭐⭐ |
| `./.env.example` | 环境变量清单与敏感项提示 | `config` | - | `config/*` | ⭐⭐ |
| `./config/settings.py` | `.env` → vnpy `SETTINGS` 写入 | `config` | `.env` | `main.py` | ⭐⭐⭐ |
| `./config/plugin_settings.py` | CTP_* 读取与 SimNow 默认 | `gateway-ctp`,`config` | `.env` | CTP 配置消费方[未索引] | ⭐⭐ |
| `./config/alert_config.py` | 告警渠道/级别/静音策略 | `alert`,`config` | `.env` | `alert_manager`[未索引] | ⭐⭐ |
| `./config/trading_sessions_config.py` | 市场时段定义与品种识别 | `trading-session` | - | `BaseCtaStrategy` | ⭐⭐⭐ |
| `./config/futures_config.py` | 期货品种参数字典 | `config` | - | `FuturesDataDownloader` | ⭐⭐ |
| `./core/charts/enhanced_chart_widget.py` | 指标体系+扩展动态加载+交互组件 | `chart-widget`,`indicator` | `core/indicators/*` | ChartWizard UI[未索引] | ⭐⭐⭐ |
| `./core/indicators/indicator_base.py` | 指标配置对话框通用实现 | `indicator-config` | vnpy Qt | `core/indicators/*` | ⭐⭐ |
| `./core/strategies/base_strategy.py` | 策略基类：时段/日志/告警 | `strategy`,`trading-session` | vnpy CTA | 策略实现[未索引] | ⭐⭐⭐ |
| `./core/logging/logger_manager.py` | loguru 初始化与轮转 | `logging` | loguru | `BaseCtaStrategy` | ⭐⭐ |
| `./core/data/downloader.py` | tqsdk 拉取K线写入 vnpy DB | `data-download`,`db` | `config/futures_config.py` | 数据准备脚本[未索引] | ⭐⭐ |
| `./core/models/trade_models.py` | 成交持久化模型与查询 | `db` | SQLAlchemy/vnpy_mysql | 统计/回测[未索引] | ⭐⭐ |
| `./tests/README.md` | 测试运行方式与注意事项 | `tests` | - | 开发验证 | ⭐ |

### 3.2 模块：应用文档（ATMQuant）

| 文件路径 | 功能精要 | 检索标签 | 上游依赖 | 下游被依赖 | 重要度 |
|---|---|---|---|---|---|
| `./docs/application/INDEX.md` | 应用文档总入口与导航 | `docs-index` | - | Agent 入口 | ⭐⭐ |
| `./docs/application/project-overview.md` | 技术栈与能力摘要 | `docs-index` | - | Onboarding | ⭐⭐ |
| `./docs/application/architecture.md` | 事件驱动+插件化架构说明 | `docs-index` | - | 架构理解 | ⭐⭐ |
| `./docs/application/source-tree-analysis.md` | 目录树与关键文件指路 | `docs-index` | - | 代码导航 | ⭐⭐ |
| `./docs/application/development-guide.md` | 环境/测试/常见任务 | `docs-index` | - | 开发流程 | ⭐⭐ |
| `./docs/application/component-inventory.md` | 图表/指标/插件清单 | `docs-index`,`indicator` | - | 选型/查找 | ⭐⭐ |
| `./docs/application/data-models.md` | TradeData 表与字段说明 | `db` | `core/models/trade_models.py` | 数据理解 | ⭐ |
| `./docs/application/README.md` | 应用知识库“联邦单元”说明 | `docs-index`,`workflow-sdd` | `docs/system/*` | 模板体系 | ⭐ |

### 3.3 模块：系统文档与知识库（AI-SDD）

| 文件路径 | 功能精要 | 检索标签 | 上游依赖 | 下游被依赖 | 重要度 |
|---|---|---|---|---|---|
| `./docs/system/INDEX.md` | knowledge/solutions/analysis/requirements/specs 总索引 | `docs-index` | `DESIGN.md` | 全体系入口 | ⭐⭐⭐ |
| `./docs/system/DESIGN.md` | SSOT/联邦治理/四视角元模型 | `constitution`,`mapping` | - | 全库结构约束 | ⭐⭐⭐ |
| `./docs/system/CONTRIBUTING.md` | ID 引用规则与贡献流程 | `constitution` | - | 修改规则 | ⭐⭐ |
| `./docs/system/knowledge/README.md` | knowledge 总说明与入口 | `knowledge` | `docs/system/INDEX.md` | 视角导航 | ⭐⭐ |
| `./docs/system/knowledge/constitution/GLOSSARY.md` | 术语表 + 常用映射字段速查 | `glossary`,`mapping` | - | 统一语言 | ⭐⭐ |
| `./docs/system/knowledge/constitution/standards/naming-conventions.md` | 实体 ID 前缀与文件命名规则 | `naming` | - | 全库校验 | ⭐⭐ |
| `./docs/system/knowledge/constitution/adr/ADR-001-knowledge-repo-structure.md` | 知识库结构治理决策 | `adr` | - | 结构依据 | ⭐⭐ |
| `./docs/system/knowledge/constitution/adr/ADR-002-atmquant-docs-and-knowledge.md` | docs 根与 knowledge 位置决策 | `adr` | - | 路径权威 | ⭐⭐ |
| `./docs/system/knowledge/business/BD-ORDER/.../BC-ORDER-MGMT/_meta.yaml` | BC→APP 映射示例 | `business-view`,`mapping` | - | 追溯实现 | ⭐ |
| `./docs/system/knowledge/business/BD-ORDER/.../AGG-ORDER.yaml` | AGG→ENT 映射示例 | `business-view`,`mapping` | - | 数据追溯 | ⭐ |
| `./docs/system/knowledge/product/PL-ECOMMERCE/.../FT-ADD-TO-CART.yaml` | FT→API/UC 映射示例 | `product-view`,`mapping` | - | 功能追溯 | ⭐ |
| `./docs/system/knowledge/technical/SYSTEM-ARCHITECTURE.md` | 系统/子系统职责与依赖 | `technical-view` | - | 宏观架构 | ⭐⭐ |
| `./docs/system/knowledge/technical/SYS-ECOMMERCE-BACKEND/APPLICATION-ARCHITECTURE.md` | 微服务分层/交互/横切关注点 | `technical-view` | - | 设计参考 | ⭐ |
| `./docs/system/knowledge/technical/.../APP-ORDER-SERVICE.yaml` | APP 注册信息样例 | `technical-view`,`mapping` | - | 联邦治理 | ⭐ |
| `./docs/system/knowledge/data/DATA-ARCHITECTURE.md` | 数据存储全景+缓存/备份策略 | `data-view` | - | 数据治理 | ⭐ |
| `./docs/system/knowledge/data/.../ENT-T_ORDER.yaml` | ENT→AGG 映射示例 | `data-view`,`mapping` | - | 数据追溯 | ⭐ |
| `./.ai/CONVENTIONS.md` | `.ai/rules` 索引与关键摘要 | `workflow-sdd` | `.ai/rules/**` | 规范入口 | ⭐⭐ |
| `./.ai/workflows.yaml` | AI-SDD 主流程与阶段门禁 | `workflow-sdd` | - | 过程编排 | ⭐⭐ |
| `./.ai/agents.yaml` | Agent 角色与输入输出产物 | `workflow-sdd` | - | Agent 路由 | ⭐ |
| `./.ai/context/project-context.yaml` | 全局/阶段/按需上下文装载策略 | `workflow-sdd` | - | RAG 策略 | ⭐⭐ |

---

## 4. 核心数据流（Mode 3）

### DF-ATM-BOOT：应用启动与插件挂载

- **路径**：`./main.py` → `./config/settings.py::apply_settings()` → `vnpy.event.EventEngine` → `vnpy.trader.engine.MainEngine` → `add_gateway(CtpGateway)` → `add_app(CtaStrategyApp/CtaBacktesterApp/ChartWizardApp)` → `MainWindow.showMaximized()` → `qapp.exec()`
- **要点**：配置注入在引擎创建前完成；App 以 vnpy 插件方式挂载。

### DF-ATM-CONFIG：.env → SETTINGS 注入

- **路径**：`./config/settings.py::load_env_file()` 读取项目根 `.env` → `get_atmquant_settings()` 构造字典 → `apply_settings()` 更新 `vnpy.trader.setting.SETTINGS`
- **要点**：此处决定 datafeed/database/email/log 等运行参数；属于启动链路的“全局开关”。

### DF-ATM-CHART：K线图表渲染与指标装载

- **路径**：ChartWizardApp（vnpy 插件）→ 使用 `./core/charts/enhanced_chart_widget.py::EnhancedChartWidget`
  - `EnhancedChartWidget` → 注册基础指标（BOLL/SMA/EMA/Volume/MACD/RSI/DMI）
  - `EXTENDED_INDICATORS_CONFIG` → `__import__(core.indicators.<module>)` 动态装载扩展指标类（缺失时静默跳过）
- **要点**：扩展指标“可选装”，不应让缺失模块阻塞应用启动。

### DF-ATM-STRATEGY：策略运行中的时段识别 + 日志/告警

- **路径**：`./core/strategies/base_strategy.py::BaseCtaStrategy.__init__()`  
  `vt_symbol` → `./config/trading_sessions_config.py::get_trading_session_by_symbol()` → `TradingSession`  
  同时 `get_logger(symbol=...)` 绑定日志；`send_alert()` 调用 `alert_manager`（实现未索引，见 §6）
- **要点**：交易时段直接影响小时/半小时聚合与日线结束时间（`daily_end` 设计为最后一分钟K线时间戳）。

### DF-ATM-DATA：期货历史数据下载入库

- **路径**：`./core/data/downloader.py::FuturesDataDownloader`  
  `vnpy.trader.database.get_database()` → `tqsdk.TqApi` 拉取K线 → 转换为 `vnpy.trader.object.BarData` → 写入 DB
- **要点**：支持游客/鉴权模式；免费版限制有兼容分支（专业版时间范围 → 免费版 data_length）。

### DF-ATM-TRADE：成交数据持久化与查询

- **路径**：`./core/models/trade_models.py`
  - 优先：`vnpy_mysql.mysql_database` 提供 `Base/engine/session`
  - 否则：从 `vnpy.trader.setting.SETTINGS` 拼接 `mysql+pymysql://...` 建 engine
  - `save_trade_data()` / `get_last_trade()` / `get_unclosed_trades()` 等对 `TradeData` 读写
- **要点**：无 `vnpy_mysql` 时默认走 MySQL URL（并非 SQLite）；该行为对本地体验影响大，需在实现侧留意。

---

## 5. 配置与环境变量索引（Mode 3）

> 只列出已读到的配置与变量；默认值以代码/示例为准。**敏感项**：凭据、密码、webhook、密钥。

### 5.1 `.env` 变量（示例来源：`./.env.example`）

| 配置项 | 所在文件 | 语义 | 默认值 | 敏感性 |
|---|---|---|---|---|
| `DATABASE_TYPE` | `./.env.example` / `./config/settings.py` | vnpy `database.name` 类型 | `sqlite` | 否 |
| `DATABASE_NAME` | 同上 | SQLite 文件名或 DB 名 | `atmquant.db` | 否 |
| `DATABASE_HOST` | 同上 | MySQL 主机 | `localhost` | 否 |
| `DATABASE_PORT` | 同上 | MySQL 端口 | `3306` | 否 |
| `DATABASE_USER` | 同上 | MySQL 用户 | `root` | 中 |
| `DATABASE_PASSWORD` | 同上 | MySQL 密码 | `your_password` | **高** |
| `DATAFEED_NAME` | 同上 | datafeed 名称（vnpy） | 空 | 中 |
| `DATAFEED_USERNAME` | 同上 | 数据源账号 | 空 | **高** |
| `DATAFEED_PASSWORD` | 同上 | 数据源密码 | 空 | **高** |
| `EMAIL_SERVER` | 同上 | SMTP 地址 | `smtp.qq.com` | 否 |
| `EMAIL_PORT` | 同上 | SMTP 端口 | `465` | 否 |
| `EMAIL_USERNAME` | 同上 | 邮箱账号 | - | 中 |
| `EMAIL_PASSWORD` | 同上 | 邮箱授权码 | - | **高** |
| `FEISHU_DEFAULT_WEBHOOK` | `./config/alert_config.py` | 飞书 webhook | 示例URL | **高** |
| `FEISHU_DEFAULT_SECRET` | 同上 | 飞书签名密钥 | - | **高** |
| `DINGTALK_DEFAULT_WEBHOOK` | 同上 | 钉钉 webhook | 示例URL | **高** |
| `DINGTALK_DEFAULT_SECRET` | 同上 | 钉钉签名密钥 | - | **高** |

### 5.2 CTP 连接变量（来源：`./config/plugin_settings.py`）

| 配置项 | 语义 | 默认值 | 敏感性 |
|---|---|---|---|
| `CTP_USER` | 交易用户名 | `your_simnow_account` | **高** |
| `CTP_PASSWORD` | 交易密码 | 空 | **高** |
| `CTP_BROKER` | 经纪商代码 | `9999` | 中 |
| `CTP_TD_ADDRESS` | 交易服务器 | SimNow 地址 | 中 |
| `CTP_MD_ADDRESS` | 行情服务器 | SimNow 地址 | 中 |
| `CTP_APP_ID` | 产品名称 | `simnow_client_test` | 中 |
| `CTP_AUTH_CODE` | 授权编码 | `0000...` | **高** |

### 5.3 代码级配置结构

- `./config/settings.py::get_atmquant_settings()`  
  - **输出**：写入 `vnpy.trader.setting.SETTINGS` 的字典键（如 `database.*`、`email.*`、`datafeed.*`、`log.*`、`font.*`）
- `./config/alert_config.py`  
  - **输出**：`FEISHU_CONFIG`、`DINGTALK_CONFIG`、`ALERT_CONFIG`（级别开关、静音策略、消息长度）

---

## 6. 未索引区域声明

> 原因：Mode 3 仍无法通读全仓；且本次目标是“AI 可检索地图”，优先精读入口/规则/关键链路。以下路径未读取内容，禁止推断细节。

- **vnpy 插件与框架源码**：`./vnpy/`、`./vnpy_*`（如 `vnpy_chartwizard/`、`vnpy_ctastrategy/` 等）`[未索引]`
  - **原因**：体量大；当前已通过入口与调用点确认集成方式
  - **建议后续**：优先精读 `vnpy_chartwizard` 中与 EnhancedChartWidget 的绑定点
- **core/indicators 具体指标实现**：`./core/indicators/*.py`（除 `indicator_base.py` 外）`[未索引]`
  - **原因**：指标数量多；本次只确认“可配置协议 + 动态装载入口”
- **告警实现**：`./core/logging/alert_manager.py` `[未索引]`
  - **原因**：本次未读取；但被 `BaseCtaStrategy` 调用
- **脚本/工具/回测目录**：`./scripts/`、`./backtests/`、`./utils/`、`./examples/` `[未索引]`
  - **原因**：本次聚焦主运行链路与文档体系
- **docs/system/knowledge 的其余实体**：除本文 §3.3 列出的抽样文件外，其余 `_meta.yaml`、`*.yaml`、`*.md` `[未索引]`
  - **原因**：知识库是规模化体系；已抽样验证元模型与映射字段
  - **建议后续**：按“要追溯的实体类型（BD/BC/AGG/FT/APP/DS/ENT）”批量精读对应目录

---

## 7. AI 查阅指北（检索表 + Prompt 模板）

### 7.1 要了解什么 → 优先标签/路径

| 目标 | 优先标签 | 首选路径 |
|---|---|---|
| 启动流程/插件加载 | `entrypoint`,`vnpy` | `./main.py` |
| .env 配置如何注入 | `config` | `./config/settings.py` + `./.env.example` |
| 图表指标如何装载 | `chart-widget`,`indicator` | `./core/charts/enhanced_chart_widget.py` |
| 指标如何做配置UI | `indicator-config` | `./core/indicators/indicator_base.py` |
| 策略如何识别交易时段 | `strategy`,`trading-session` | `./core/strategies/base_strategy.py` + `./config/trading_sessions_config.py` |
| 历史数据如何下载入库 | `data-download`,`db` | `./core/data/downloader.py` |
| 成交记录如何落库/查询 | `db` | `./core/models/trade_models.py` |
| 测试怎么跑 | `tests` | `./tests/README.md` |
| AI-SDD 文档体系入口 | `docs-index` | `./docs/system/INDEX.md` |
| 知识库四视角/映射字段 | `knowledge`,`mapping` | `./docs/system/DESIGN.md` + `./docs/system/knowledge/README.md` |
| ID 命名与引用规范 | `naming` | `./docs/system/knowledge/constitution/standards/naming-conventions.md` |
| 工作流与上下文装载策略 | `workflow-sdd` | `./.ai/workflows.yaml` + `./.ai/context/project-context.yaml` |

### 7.2 快速检索 Prompt 模板（面向代码/文档混合仓）

**模板 A：找“入口/调用链”**

> 请从 `./main.py` 出发，梳理创建 `EventEngine`、`MainEngine`、注册 `CtpGateway` 与 `ChartWizardApp` 的调用顺序；指出每一步的失败处理与可替换点（比如不加载 DataManagerApp）。

**模板 B：找“配置项 → 生效位置”**

> 对照 `./.env.example` 与 `./config/settings.py`，列出每个环境变量最终写入的 `vnpy.trader.setting.SETTINGS` 键名，并说明缺省值与敏感性。

**模板 C：找“图表指标扩展点”**

> 在 `./core/charts/enhanced_chart_widget.py` 中，解释扩展指标 `EXTENDED_INDICATORS_CONFIG` 的动态导入机制：缺失模块时的行为、如何新增一个扩展指标并让其出现在 sub plot 中。

