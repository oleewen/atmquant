---
id: "constitution-glossary"
title: "全局术语表"
version: "0.2.0"
status: "active"
created: "2025-03-13"
updated: "2025-03-15"
tags: ["glossary", "terminology", "constitution", "atmquant"]
---

# 全局术语表（ATMQuant）

本表为 ATMQuant 项目业务与技术术语的统一定义，便于文档与代码沟通一致。AI Agent 理解本系统时以本表为准。

## 知识库与架构

| 术语 | 英文 | 定义 |
|------|------|------|
| 单一事实源 | SSOT | 每个知识实体只在一处定义，其他地方通过 ID 引用。 |
| 联邦治理 | Federated Governance | 系统级仓库管理宏观架构与索引，应用级管理微观设计并上报。 |
| 限界上下文 | Bounded Context | DDD 中明确边界的业务上下文，拥有统一语言与领域模型。 |
| 聚合根 | Aggregate Root | DDD 中聚合的根实体，保证聚合内一致性边界。 |
| 架构决策记录 | ADR | 记录架构决策的上下文、决定与后果的文档。 |

## 量化与交易（业务术语）

| ID | 术语 | 英文 | 定义 | 易混淆项 |
|----|------|------|------|----------|
| BT-KLINE | K线 | Candlestick/Bar | 某周期内开高低收（OHLC）及成交量的单根柱状数据 | Bar 与 Candlestick 在本项目中同义 |
| BT-TICK | Tick | Tick | 单笔成交或行情快照（价格、量、时间） | 与 Bar 区分：Bar 为聚合后的 K 线 |
| BT-BAR | Bar | Bar | 与 K 线同义，强调为 vnpy BarData 结构 | 见 BT-KLINE |
| BT-STRATEGY | 策略 | Strategy | 可回测、可实盘执行的交易逻辑（信号、开平仓规则） | 与“指标”区分：策略产生交易信号并执行 |
| BT-INDICATOR | 技术指标 | Technical Indicator | 由 K 线或 Tick 计算得到的派生序列（如 MA、MACD、RSI） | 仅计算与展示，不直接下单 |
| BT-BACKTEST | 回测 | Backtest | 用历史 Bar 数据驱动策略运行并统计绩效的过程 | 与实盘区分：无真实下单 |
| BT-SIGNAL | 交易信号 | Signal | 策略产生的多/空/平仓等建议或指令 | 信号可被策略执行或仅用于展示 |
| BT-SESSION | 交易时段 | Trading Session | 一日内连续交易的时间区间（如 9:00–11:30） | 用于 K 线按“交易时段”聚合 |
| BT-CONTRACT | 合约 | Contract | 可交易的标的（如期货合约代码） | 来自 vnpy 的 ContractData |
| BT-GATEWAY | 交易网关 | Gateway | 连接交易所或经纪商的接入模块（如 CTP） | 由 vnpy 网关体系承载 |

## 图表与可视化（业务术语）

| ID | 术语 | 英文 | 定义 |
|----|------|------|------|
| BT-CHART | 图表 | Chart | 展示 K 线与指标的画布/视图（单图、双图、四图等） |
| BT-DUAL-CHART | 双图视图 | Dual Chart | 两个周期或两个合约并排展示的图表布局 |
| BT-QUAD-CHART | 四图视图 | Quad Chart | 2×2 网格展示四个周期或四个图表的布局 |
| BT-VIEWBOX | 视口 | ViewBox | 图表内可缩放、平移的坐标区域（pyqtgraph） |
| BT-CURSOR | 光标 | Cursor | 图表上跟随鼠标的十字线及时间/价格标签 |

## 技术术语（ATMQuant）

| ID | 术语 | 定义 | 使用场景 |
|----|------|------|----------|
| TT-VNPY | VeighNa / vnpy | 开源 Python 量化交易框架，提供事件引擎、网关、策略、回测等 | 项目基础框架 |
| TT-CTP | CTP | 上期技术期货交易接口 | 国内期货实盘网关 |
| TT-DATAFEED | 数据源 | DataFeed | 提供历史或实时 Bar/Tick 的组件（如 Tushare、AKShare） | 配置中的 DATAFEED_NAME |
| TT-EVENT-ENGINE | 事件引擎 | Event Engine | vnpy 内基于事件总线的消息分发机制 | 各模块通过事件协作 |
| TT-MAIN-ENGINE | 主引擎 | Main Engine | vnpy 统一管理网关、应用、策略的入口 | main.py 中创建 |
| TT-HEADLESS-CALC | 无头计算器 | Headless Calculator | 不依赖 Qt/UI 的指标计算器，供策略与回测复用 | 与图表内指标共享算法 |

## 缩写对照

| 缩写 | 全称 | 说明 |
|------|------|------|
| ADR | Architecture Decision Record | 架构决策记录 |
| OHLC | Open/High/Low/Close | 开高低收 |
| CTA | CTA Strategy | 期货策略（vnpy 模块名） |
| PRD | Product Requirements Document | 产品需求说明书 |
| ADD | Architecture Design Document | 架构设计说明书 |
| TDD | Test Design Document | 测试设计说明书（非仅指 Test-Driven Development） |

## 视角与层级（与 knowledge 结构对应）

| 视角 | 含义 |
|------|------|
| 业务视角 | 业务域、子域、限界上下文、聚合等，不依赖技术实现。 |
| 产品视角 | 产品线、模块、功能点、用例。 |
| 技术视角 | 系统、应用、模块与接口等物理实现。 |
| 数据视角 | 数据存储、数据实体、字段与数据流。 |

## 映射关系（常用）

| 关系 | 含义 |
|------|------|
| implemented_by_app_id | 限界上下文由哪个应用（代码库/模块）实现。 |
| relies_on_context_ids | 产品模块依赖哪些限界上下文。 |
| invokes_api_ids | 功能点调用的 API 或接口列表。 |
| persisted_as_entity_ids | 聚合持久化对应的数据实体 ID。 |
| maps_to_aggregate_id | 数据实体对应的业务聚合根。 |
