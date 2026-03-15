# AKShare 数据源集成说明

## 概述

项目通过 `vnpy_akshare` 模块集成 [AKShare](https://github.com/akfamily/akshare) 作为可选数据源，与现有 datafeed 机制一致：在 `.env` 中设置 `DATAFEED_NAME=akshare` 即可使用。

## 安装

```bash
pip install akshare
```

依赖已写入 `requirements.txt`（`akshare>=1.14.0`）。本仓库内已包含 `vnpy_akshare` 包，无需单独安装。

## 配置

在 `.env` 中设置：

```env
DATAFEED_NAME=akshare
```

AKShare 为免费数据接口，**无需**配置 `DATAFEED_USERNAME` / `DATAFEED_PASSWORD`。

## 支持范围

| 类型     | 交易所 | K 线周期 | 说明 |
|----------|--------|----------|------|
| A 股     | SSE、SZSE | 日线、周线、月线 | 前复权日/周/月 K 线 |
| 国内期货 | CFFEX、SHFE、DCE、CZCE、INE | 仅日线 | 各交易所官网日线行情 |

- **A 股**：使用 `stock_zh_a_hist`，symbol 为 6 位代码（如 `600519`、`000001`）。
- **期货**：使用 `get_futures_daily`，symbol 为合约代码（如 `rb2510`、`IF2512`），按交易所与日期范围筛选。

暂不支持：分钟线、Tick、GFEX 交易所。

## 使用方式

与其它 datafeed 相同，由 CTA 回测、数据管理、K 线图表等模块通过 `get_datafeed()` 获取数据服务；当 `DATAFEED_NAME=akshare` 时会自动加载 `AkshareDatafeed`，无需改业务代码。

## 与 Tushare / 天勤 对比

- **AKShare**：免费、无需 Token，适合 A 股与期货日线回测与补数。
- **Tushare**：需 Token，数据维度更全，可作主数据源。
- **天勤 (tqsdk)**：需账号，支持期货分钟/Tick 与实盘行情。

可在不同环境使用不同 `DATAFEED_NAME`（如开发用 akshare，实盘用 tqsdk）。

## 批量下载 A 股全市场日/周/月线并导入 SQLite

脚本 `scripts/download_akshare_stock_bars.py` 可从 AKShare 拉取**全市场 A 股**在 2022–2026 年的**日线、周线、月线**，先落盘到本地 CSV，再导入当前配置的数据库。

### 使用 SQLite

1. 在 `.env` 中设置：
   ```env
   DATABASE_TYPE=sqlite
   DATABASE_NAME=atmquant.db
   ```
2. 安装 SQLite 驱动（若尚未安装）：
   ```bash
   pip install vnpy_sqlite
   ```
3. 执行（拉取并导入）：
   ```bash
   python scripts/download_akshare_stock_bars.py
   ```
4. 仅下载到本地、不写库：
   ```bash
   python scripts/download_akshare_stock_bars.py --download-only
   ```
5. 仅从已有 CSV 导入数据库：
   ```bash
   python scripts/download_akshare_stock_bars.py --import-only
   ```

### 本地文件与数据库说明

- **本地目录**：默认 `data/akshare_bars/`，下分 `daily/`、`weekly/`、`monthly/`，每只股票一个 CSV：`{symbol}.{exchange}.csv`（如 `600519.SSE.csv`）。
- **导入数据库**：仅**日线、周线**会写入 vnpy 数据库（SQLite/MySQL）；**月线**因 vnpy 无 `Interval.MONTHLY`，只保留在本地 CSV 中供离线使用。
- **断点续传**：默认跳过已存在的 CSV（`--no-skip-existing` 可覆盖）。
- **测试**：可用 `--limit 10` 只处理前 10 只股票，或缩短 `--start`/`--end` 日期范围。
