# ATMQuant - 数据模型

**日期：** 2026-03-17

## 概述

ATMQuant 业务侧数据模型主要集中在 `core/models/trade_models.py`，使用 SQLAlchemy 定义表结构，可与 vnpy_mysql 或本地 MySQL 配置配合使用。vnpy 自带的 K 线、合约、订单等对象见 vnpy 文档。

## 交易记录（TradeData）

**表名：** `trade_data`  
**用途：** 统一记录实盘与回测成交，用于统计与持久化。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键自增 |
| strategy_name | String(100) | 策略名称，索引 |
| capital | Float | 成交后资金 |
| gateway_name | String(50) | 网关名 |
| symbol | String(50) | 合约代码，索引 |
| exchange | String(20) | 交易所 |
| orderid | String(50) | 订单 id |
| tradeid | String(50) | 成交 id |
| direction | String(10) | LONG / SHORT |
| offset | String(20) | OPEN / CLOSE / CLOSETODAY |
| price | Float | 成交价 |
| volume | Integer | 成交量 |
| closed_volume | Integer | 已平仓手数，默认 0 |
| status | Integer | 1=未平仓 2=已平仓（TradeStatus 枚举） |
| datetime | DateTime | 成交时间，索引 |
| trade_type | String(20) | REAL / BACKTEST，默认 REAL，索引 |
| backtest_id | String(50) | 回测 ID（回测时使用），索引 |

**索引：**

- `idx_strategy_tradeid` (strategy_name, tradeid)
- `idx_strategy_symbol_direction` (strategy_name, symbol, direction)
- `idx_backtest_id` (backtest_id)

## 枚举

- **TradeStatus：** UN_CLOSED=1，CLOSED=2。

## 主要函数（trade_models.py）

| 函数 | 说明 |
|------|------|
| get_last_trade | 按策略、合约、方向取最近一笔成交 |
| get_unclosed_trades | 按策略、合约取未平仓记录 |
| save_trade_data | 保存成交记录 |
| update_db_trade_data | 更新库中 TradeData |
| get_trades_by_backtest_id | 按回测 ID 查询 |
| get_trades_by_strategy_and_period | 按策略与时间区间查询 |
| create_tables | 创建表（按当前 Base/engine） |

## 数据库配置

- 由 `config/settings.py` 从 `.env` 读取并写入 vnpy `SETTINGS`（database.name、host、port、user、password 等）。
- 使用 MySQL 时依赖 `vnpy_mysql`，`trade_models.py` 中从 `vnpy_mysql.mysql_database` 获取 `Base`、`engine`、`get_db_session`、`close_db_session`；若未安装 vnpy_mysql 则使用本地构造的 engine 与 session。

---

_由 BMAD document-project 工作流生成_
