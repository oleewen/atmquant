# ATMQuant - 源码树与目录分析

**日期：** 2026-03-17

## 带注释的目录树

```
atmquant/                          # 项目根目录
├── main.py                         # 主入口：加载配置、创建事件引擎与主引擎、注册网关与 App、启动 MainWindow
├── requirements.txt               # Python 依赖
├── .env.example                   # 环境变量示例（复制为 .env 使用）
├── core/                           # 核心业务模块（ATMQuant 自有）
│   ├── charts/                    # 图表组件
│   │   ├── components/            # 图表子组件
│   │   │   ├── cursor_manager.py  # 光标管理器
│   │   │   └── extendable_viewbox.py # 可扩展 ViewBox（X 轴延伸等）
│   │   ├── enhanced_chart_widget.py # 增强版 K 线图表（主图/副图指标、配置、扩展指标）
│   │   ├── dual_chart_widget.py   # 双图视图
│   │   └── quad_chart_widget.py   # 四图视图
│   ├── indicators/                # 技术指标实现
│   │   ├── indicator_base.py      # ConfigurableIndicator 基类
│   │   ├── boll_item.py           # 布林带
│   │   ├── multi_sma_item.py      # 多均线 SMA
│   │   ├── multi_ema_item.py      # 多均线 EMA
│   │   ├── macd_item.py           # MACD
│   │   ├── rsi_item.py            # RSI
│   │   ├── dmi_item.py            # DMI
│   │   ├── dyna_array_manager.py  # 动态数组管理（策略用）
│   │   └── （扩展指标按需动态加载）
│   ├── data/                      # 数据处理
│   │   └── downloader.py           # 期货数据下载与合约管理
│   ├── logging/                   # 日志与告警
│   │   ├── logger_manager.py      # 日志管理器
│   │   └── alert_manager.py        # 告警管理器（飞书/钉钉）
│   ├── strategies/                # 策略
│   │   ├── base_strategy.py       # BaseCtaStrategy（交易时段、日志、告警）
│   │   └── triple_ma_strategy.py  # 3MA 示例策略
│   └── models/                    # 数据模型
│       └── trade_models.py        # 交易记录模型（TradeData 等）
├── config/                        # 统一配置
│   ├── settings.py                # 轻量配置：.env → vnpy SETTINGS
│   ├── alert_config.py             # 告警配置
│   ├── plugin_settings.py          # 插件配置
│   ├── futures_config.py           # 期货合约配置
│   └── trading_sessions_config.py # 交易时段配置
├── vnpy_chartwizard/               # K 线图表 App（集成 EnhancedChartWidget、实时 tick）
├── vnpy_spreadtrading/             # 价差交易模块
├── vnpy_tqsdk/                    # 天勤数据源
├── vnpy_akshare/                  # AkShare 数据源
├── vnpy_tushare/                  # Tushare 数据源（requirements 中）
├── vnpy_ctp/                      # CTP 交易网关
├── vnpy_ctastrategy/              # CTA 策略引擎
├── vnpy_ctabacktester/            # CTA 回测引擎与界面
├── vnpy_datamanager/              # 数据管理
├── vnpy_mysql/                    # MySQL 数据库
├── vnpy/                          # VeighNa 框架核心
├── scripts/                        # 脚本（回测、下载数据、更新合约等）
├── backtests/                     # 回测相关
├── utils/                         # 工具模块
├── tests/                         # 测试
│   ├── unit/
│   ├── integration/
│   └── backtest/
├── docs/                          # 文档
│   ├── README.md                  # 文档中心
│   ├── index.md                   # 工程文档索引
│   ├── project-overview.md        # 项目概览（及 architecture、development-guide 等）
│   └── knowledge/                 # 知识库（四视角）
└── examples/                      # 使用示例
```

## 关键目录说明

| 目录/文件 | 用途 |
|-----------|------|
| `main.py` | 应用入口；加载 config、创建 EventEngine/MainEngine、注册 CTP/CTA/回测/ChartWizard、显示主窗口 |
| `core/charts` | 增强 K 线、双图/四图、光标与 ViewBox 扩展 |
| `core/indicators` | 所有技术指标（主图/副图、可配置、扩展指标动态加载） |
| `core/strategies` | 策略基类与示例策略 |
| `core/data` | 数据下载与合约管理 |
| `core/logging` | 统一日志与告警 |
| `core/models` | 交易等业务数据模型 |
| `config` | 全局与插件配置、交易时段 |
| `vnpy_*` | vnpy 插件：交易、策略、回测、图表、数据源、数据库 |
| `vnpy` | vnpy 框架核心（event、trader、chart 等） |

## 入口与集成点

- **应用入口：** `main.py` → `main()`。
- **图表数据流：** ChartWizardEngine 使用 datafeed/database 查询历史 → 发送 `EVENT_CHART_HISTORY` → 图表与策略消费。
- **配置注入：** `config.settings.apply_settings()` 在 `main.py` 启动时调用，将 `.env` 写入 vnpy `SETTINGS`。

---

_由 BMAD document-project 工作流生成_
