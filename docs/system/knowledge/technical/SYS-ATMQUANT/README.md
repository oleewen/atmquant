# SYS-ATMQUANT：ATMQuant 交易系统

本系统为基于 vnpy 4.1 的单体桌面应用，实现多周期图表、技术指标、策略与回测、数据与配置、日志告警。

## 应用/模块索引

| 类型 | ID / 名称 | 路径 | 说明 |
|------|-----------|------|------|
| 核心包 | core | 仓库 `core/` | 图表、指标、数据、日志、策略 |
| 配置包 | config | 仓库 `config/` | 设置与告警配置 |
| vnpy 应用 | ChartWizardApp | `vnpy_chartwizard/` | K 线图表 App，集成 EnhancedChartWidget |
| vnpy 应用 | CtaStrategyApp | `vnpy_ctastrategy/` | CTA 策略运行 |
| vnpy 应用 | CtaBacktesterApp | `vnpy_ctabacktester/` | 回测 |
| vnpy 网关 | CtpGateway | `vnpy_ctp/` | CTP 期货接口 |
| 数据源插件 | vnpy_tushare / vnpy_akshare | 见 requirements | 历史与行情数据 |

## 实现与业务映射

| 限界上下文 (business) | 实现位置 (technical) |
|----------------------|----------------------|
| BC-CHART-VIEW        | core/charts、vnpy_chartwizard |
| BC-INDICATOR-MGR     | core/indicators |
| BC-STRATEGY-RUN      | core/strategies、vnpy_ctastrategy、vnpy_ctabacktester |
| BC-DATA-CONFIG       | core/data、config |
| BC-LOG-ALERT         | core/logging、config/alert_config.py |

## 参考

- [系统架构总览](../SYSTEM-ARCHITECTURE.md)
- [业务视角 README](../business/README.md)
