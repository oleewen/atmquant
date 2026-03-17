# ATMQuant - 组件与指标清单

**日期：** 2026-03-17

## 图表组件（core/charts）

| 组件 | 文件 | 说明 |
|------|------|------|
| EnhancedChartWidget | enhanced_chart_widget.py | 增强版 K 线图表：主图/副图指标、复选框显隐、参数配置、扩展指标动态加载、X 轴延伸、专注模式 |
| DualChartWidget | dual_chart_widget.py | 双图并排视图，时间轴同步 |
| QuadChartWidget | quad_chart_widget.py | 四图 2×2 视图，时间轴同步 |
| CursorManager | components/cursor_manager.py | 光标与十字线管理 |
| ExtendableViewBox | components/extendable_viewbox.py | 可扩展 ViewBox（拖拽/键盘延伸 X 轴） |

## 技术指标（core/indicators）

### 主图指标（K 线同层）

| 指标 | 类名 | 文件 | 说明 |
|------|------|------|------|
| 布林带 | BollItem | boll_item.py | 可配置 |
| 多均线 SMA | MultiSmaItem | multi_sma_item.py | 可配置 |
| 多均线 EMA | MultiEmaItem | multi_ema_item.py | 可配置 |
| 斐波那契入场带 | FibonacciEntryBandsItem | （扩展） | 动态加载 |
| 聪明钱通道 | SmartMoneyChannelsItem | （扩展） | 动态加载 |
| ZLEMA | ZlemaItem | （扩展） | 动态加载 |
| SuperTrend | SupertrendItem | （扩展） | 动态加载 |

### 副图指标

| 指标 | 类名 | 文件 | 说明 |
|------|------|------|------|
| 成交量 | VolumeItem / EnhancedVolumeItem | （vnpy / enhanced_volume_item） | 可选增强版 |
| MACD | Macd3Item | macd_item.py | 可配置 |
| RSI | RsiItem | rsi_item.py | 可配置 |
| DMI | DmiItem | dmi_item.py | 可配置 |
| Adaptive MACD Deluxe | AdaptiveMacdDeluxeItem | （扩展） | 动态加载 |
| Squeeze Momentum | SqueezeMomentumItem | （扩展） | 动态加载 |
| Supertrended RSI | SupertrendedRsiItem | （扩展） | 动态加载 |
| WaveTrend | WaveTrendItem | （扩展） | 动态加载 |

### 基础与工具

| 名称 | 文件 | 说明 |
|------|------|------|
| ConfigurableIndicator | indicator_base.py | 可配置指标混入类（配置对话框、应用/获取配置） |
| DynaArrayManager | dyna_array_manager.py | 动态数组管理，供策略等使用 |

## 策略（core/strategies）

| 组件 | 文件 | 说明 |
|------|------|------|
| BaseCtaStrategy | base_strategy.py | 基础 CTA 策略：交易时段识别、日志、告警 |
| TripleMaStrategy | triple_ma_strategy.py | 3MA 示例策略 |

## 数据与日志（core）

| 组件 | 文件 | 说明 |
|------|------|------|
| LoggerManager | logging/logger_manager.py | 统一日志管理 |
| AlertManager | logging/alert_manager.py | 告警（飞书/钉钉） |
| FuturesDataDownloader | data/downloader.py | 期货数据下载与合约管理 |

## 配置（config）

| 文件 | 说明 |
|------|------|
| settings.py | .env 加载并写入 vnpy SETTINGS |
| alert_config.py | 告警机器人等配置 |
| plugin_settings.py | 插件相关配置 |
| futures_config.py | 期货合约配置 |
| trading_sessions_config.py | 交易时段配置 |

## vnpy 插件（入口与职责）

| 插件 | 目录 | 说明 |
|------|------|------|
| CTP | vnpy_ctp | 交易网关 |
| CTA 策略 | vnpy_ctastrategy | 策略引擎与 UI |
| CTA 回测 | vnpy_ctabacktester | 回测引擎与界面 |
| ChartWizard | vnpy_chartwizard | K 线图表 App（使用 EnhancedChartWidget） |
| 数据管理 | vnpy_datamanager | 数据管理 App |
| MySQL | vnpy_mysql | MySQL 数据库 |
| 数据源 | vnpy_tushare / vnpy_akshare / vnpy_tqsdk | 历史/实时数据 |
| 价差交易 | vnpy_spreadtrading | 价差交易模块 |

---

_由 BMAD document-project 工作流生成_
