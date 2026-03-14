# 源码目录结构 (Source Tree)

## 核心业务 (Core)

- **core/charts/**: 图表系统核心
  - **components/**: 图表子组件（光标管理器、扩展视图）
  - **enhanced_chart_widget.py**: 增强型K线图表
  - **dual_chart_widget.py**: 双图视图组件
  - **quad_chart_widget.py**: 四图视图组件
- **core/indicators/**: 技术指标实现（BOLL, MACD, RSI, DMI, SMA, EMA 等）
- **core/data/**: 数据处理模块
  - **future_data/**: 期货数据处理
  - **processors/**: 数据处理器
  - **downloader.py**: 数据下载逻辑
- **core/logging/**: 日志与告警系统
  - **logger_manager.py**: 日志管理器
  - **alert_manager.py**: 告警管理器
- **core/models/**: 交易模型与算法
- **core/strategies/**: 策略基类与实现
  - **base_strategy.py**: 策略基类（必须继承）
  - **triple_ma_strategy.py**: 示例策略

## 配置管理 (Config)

- **config/settings.py**: 全局配置加载
- **config/alert_config.py**: 告警配置
- **config/futures_config.py**: 期货合约配置
- **config/trading_sessions_config.py**: 交易时段配置

## 本地框架修改 (Local VNPY)

- **vnpy/**: VeighNa 框架核心修改版
  - **trader/**: 交易核心引擎
  - **chart/**: 图表基础组件
  - **event/**: 事件引擎
  - **rpc/**: RPC 通信

## 扩展模块 (Extensions)

- **vnpy_akshare/**: AkShare 数据源适配器
- **vnpy_chartwizard/**: K线图表向导模块
- **vnpy_ctabacktester/**: CTA 回测模块
- **vnpy_ctastrategy/**: CTA 策略模块
- **vnpy_ctp/**: CTP 接口封装

## 脚本与工具 (Scripts & Utils)

- **scripts/**: 运维脚本（下载数据、回测、重启等）
- **utils/**: 通用工具函数
- **tests/**: 测试代码
  - **unit/**: 单元测试
  - **integration/**: 集成测试
  - **backtest/**: 回测测试

## 文档 (Documents)

- **documents/**: 项目生成文档（本目录）
- **docs/**: 原始开发文档与指南

## 根目录文件

- **main.py**: 程序入口
- **requirements.txt**: 依赖列表
- **pytest.ini**: 测试配置
- **AGENTS.md**: AI Agent 全局规则
