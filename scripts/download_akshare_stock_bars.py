#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 AKShare 拉取 A 股全市场 2022-2026 年日/周/月线，落盘到本地并导入数据库。

用法:
  # 拉取并落盘到本地，再导入当前配置的数据库（.env 中 DATABASE_TYPE=sqlite 即导入 SQLite）
  python scripts/download_akshare_stock_bars.py

  # 仅下载到本地文件，不导入数据库
  python scripts/download_akshare_stock_bars.py --download-only

  # 仅从本地文件导入数据库（不重新拉取）
  python scripts/download_akshare_stock_bars.py --import-only

  # 指定本地目录与日期范围
  python scripts/download_akshare_stock_bars.py --data-dir data/akshare_bars --start 20220101 --end 20261231

  # 仅拉取前 N 只股票（测试用）
  python scripts/download_akshare_stock_bars.py --limit 10

使用 SQLite：在 .env 中设置 DATABASE_TYPE=sqlite、DATABASE_NAME=atmquant.db，并安装 vnpy_sqlite 后，
执行脚本即可将日线/周线导入 SQLite；月线仅保存到本地 CSV。
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime, time as dt_time
from pathlib import Path
from typing import List, Tuple

# 项目根目录
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# 先加载配置，再导入 vnpy / database
from config.settings import apply_settings
apply_settings()

import pandas as pd
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData
from vnpy.trader.utility import ZoneInfo

CHINA_TZ = ZoneInfo("Asia/Shanghai")
# 日/周/月均下载并落盘；导入数据库时仅导入日线与周线（vnpy Interval 无 MONTHLY）
INTERVALS = [
    (Interval.DAILY, "daily"),
    (Interval.WEEKLY, "weekly"),
    (None, "monthly"),  # None 表示仅落盘 CSV，不参与 BarData/DB
]
INTERVALS_FOR_DB = [(Interval.DAILY, "daily"), (Interval.WEEKLY, "weekly")]
DEFAULT_START = "20220101"
DEFAULT_END = "20261231"
REQUEST_DELAY = 0.4  # 请求间隔（秒），降低被封风险


def _parse_code_to_symbol_exchange(code: str) -> Tuple[str, Exchange] | None:
    """将 AKShare 的 code（如 000001.SZ、600519.SH）转为 (symbol, exchange)。"""
    code = (code or "").strip().upper()
    if not code or "." not in code:
        return None
    sym, suffix = code.rsplit(".", 1)
    sym = sym.strip()
    if suffix == "SH":
        return (sym, Exchange.SSE)
    if suffix == "SZ":
        return (sym, Exchange.SZSE)
    return None


def _symbol_to_exchange(symbol: str) -> Exchange:
    """根据 6 位代码判断交易所。"""
    s = (symbol or "").strip()
    if s.startswith("6") or s.startswith("5"):
        return Exchange.SSE
    return Exchange.SZSE


def get_stock_list():
    """获取 A 股代码列表，返回 [(symbol, exchange, name), ...]。"""
    import akshare as ak
    df = None
    try:
        df = ak.stock_info_a_code_name()
    except Exception:
        pass
    # 优先用 stock_info_a_code_name；若失败或无有效列则用 stock_zh_a_spot_em
    def _parse_first_api(d):
        if d is None or d.empty:
            return []
        code_col = "code" if "code" in d.columns else ("代码" if "代码" in d.columns else None)
        name_col = "name" if "name" in d.columns else ("名称" if "名称" in d.columns else None)
        if code_col is None:
            for c in d.columns:
                if str(c).lower() in ("code", "代码") or "code" in str(c).lower():
                    code_col = c
                    break
            if code_col is None:
                return []
        if name_col is None:
            name_col = next((c for c in d.columns if str(c).lower() in ("name", "名称") or "名称" in str(c)), "")
        rows = []
        for _, row in d.iterrows():
            parsed = _parse_code_to_symbol_exchange(str(row[code_col]))
            if not parsed:
                continue
            symbol, exchange = parsed
            name = str(row.get(name_col, "") or "").strip() if name_col else ""
            rows.append((symbol, exchange, name))
        return rows

    rows = _parse_first_api(df)
    if rows:
        return rows
    # 首个接口未返回有效列表时，尝试 stock_zh_a_spot_em
    try:
        df2 = ak.stock_zh_a_spot_em()
        if df2 is not None and not df2.empty:
            code_col = "代码" if "代码" in df2.columns else ("code" if "code" in df2.columns else None)
            name_col = "名称" if "名称" in df2.columns else ("name" if "name" in df2.columns else None)
            if code_col is None:
                for c in df2.columns:
                    if "代码" in str(c) or str(c).lower() == "code":
                        code_col = c
                        break
                if code_col is None:
                    return []
            if name_col is None:
                for c in df2.columns:
                    if "名称" in str(c) or str(c).lower() == "name":
                        name_col = c
                        break
                if name_col is None:
                    name_col = ""
            rows = []
            for _, row in df2.iterrows():
                code = str(row[code_col]).strip()
                if not code:
                    continue
                parsed = _parse_code_to_symbol_exchange(code)
                if parsed:
                    symbol, exchange = parsed
                else:
                    symbol = code[-6:].zfill(6) if len(code) >= 6 else code.zfill(6)
                    if len(symbol) != 6:
                        continue
                    exchange = _symbol_to_exchange(symbol)
                name = str(row.get(name_col, "") or "").strip() if name_col else ""
                rows.append((symbol, exchange, name))
            return rows
    except Exception:
        pass
    return []


def fetch_bars_akshare(symbol: str, period: str, start_date: str, end_date: str) -> pd.DataFrame | None:
    """单次拉取一只股票的 K 线，返回 DataFrame 或 None。"""
    import akshare as ak
    try:
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
        )
    except Exception:
        return None
    if df is None or df.empty:
        return None
    return df


def df_to_bar_data(
    df: pd.DataFrame,
    symbol: str,
    exchange: Exchange,
    interval: Interval,
) -> List[BarData]:
    """将 AKShare 返回的 DataFrame 转为 BarData 列表。"""
    date_col = "日期" if "日期" in df.columns else "date"
    if date_col not in df.columns:
        return []
    open_col = "开盘" if "开盘" in df.columns else "开盘价"
    high_col = "最高" if "最高" in df.columns else "最高价"
    low_col = "最低" if "最低" in df.columns else "最低价"
    close_col = "收盘" if "收盘" in df.columns else "收盘价"
    vol_col = "成交量" if "成交量" in df.columns else "volume"
    turnover_col = "成交额" if "成交额" in df.columns else "成交金额" if "成交金额" in df.columns else None
    bar_time = dt_time(15, 0)
    bars = []
    for _, row in df.iterrows():
        try:
            date_val = row[date_col]
            if hasattr(date_val, "strftime"):
                dt = datetime.combine(date_val, bar_time)
            else:
                s = str(date_val).replace("-", "")[:8]
                dt = datetime.strptime(s, "%Y%m%d").replace(tzinfo=CHINA_TZ)
                dt = dt.replace(hour=15, minute=0, second=0, microsecond=0)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=CHINA_TZ)
            bar = BarData(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                datetime=dt,
                open_price=float(row[open_col]),
                high_price=float(row[high_col]),
                low_price=float(row[low_col]),
                close_price=float(row[close_col]),
                volume=float(row[vol_col]),
                turnover=float(row[turnover_col]) if turnover_col and turnover_col in df.columns else 0.0,
                gateway_name="AKShare",
            )
            bars.append(bar)
        except (TypeError, ValueError, KeyError):
            continue
    return bars


def _save_akshare_df_to_csv(df: pd.DataFrame, path: Path) -> None:
    """将 AKShare 返回的 DataFrame 写成与 BarData 一致的 CSV 列名。"""
    date_col = "日期" if "日期" in df.columns else "date"
    open_col = "开盘" if "开盘" in df.columns else "开盘价"
    high_col = "最高" if "最高" in df.columns else "最高价"
    low_col = "最低" if "最低" in df.columns else "最低价"
    close_col = "收盘" if "收盘" in df.columns else "收盘价"
    vol_col = "成交量" if "成交量" in df.columns else "volume"
    turnover_col = "成交额" if "成交额" in df.columns else ("成交金额" if "成交金额" in df.columns else None)
    turnover_series = df[turnover_col].astype(float) if turnover_col and turnover_col in df.columns else pd.Series(0.0, index=df.index)
    out = pd.DataFrame({
        "datetime": pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d %H:%M:%S"),
        "open": df[open_col].astype(float),
        "high": df[high_col].astype(float),
        "low": df[low_col].astype(float),
        "close": df[close_col].astype(float),
        "volume": df[vol_col].astype(float),
        "turnover": turnover_series,
    })
    out.to_csv(path, index=False, encoding="utf-8-sig")


def save_bars_to_csv(bars: List[BarData], path: Path) -> None:
    """将 BarData 列表写入 CSV（便于后续从文件导入）。"""
    if not bars:
        return
    rows = []
    for b in bars:
        rows.append({
            "datetime": b.datetime.strftime("%Y-%m-%d %H:%M:%S") if b.datetime else "",
            "open": b.open_price,
            "high": b.high_price,
            "low": b.low_price,
            "close": b.close_price,
            "volume": b.volume,
            "turnover": b.turnover,
        })
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")


def load_bars_from_csv(path: Path, symbol: str, exchange: Exchange, interval: Interval) -> List[BarData]:
    """从 CSV 加载为 BarData 列表。"""
    if not path.exists():
        return []
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return []
    if df.empty or "datetime" not in df.columns:
        return []
    bars = []
    for _, row in df.iterrows():
        try:
            dt_str = str(row["datetime"]).strip()
            if " " in dt_str:
                dt = datetime.strptime(dt_str[:19], "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.strptime(dt_str[:10], "%Y-%m-%d")
            dt = dt.replace(tzinfo=CHINA_TZ)
            bar = BarData(
                symbol=symbol,
                exchange=exchange,
                interval=interval,
                datetime=dt,
                open_price=float(row["open"]),
                high_price=float(row["high"]),
                low_price=float(row["low"]),
                close_price=float(row["close"]),
                volume=float(row["volume"]),
                turnover=float(row.get("turnover", 0) or 0),
                gateway_name="AKShare",
            )
            bars.append(bar)
        except (TypeError, ValueError, KeyError):
            continue
    return bars


def load_stock_list_from_file(path: Path) -> List[Tuple[str, Exchange, str]]:
    """从 CSV 文件加载股票列表，格式：symbol,exchange,name 或 code,name。"""
    if not path.exists():
        return []
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return []
    if df.empty:
        return []
    rows = []
    if "symbol" in df.columns and "exchange" in df.columns:
        for _, row in df.iterrows():
            try:
                ex_str = str(row["exchange"]).strip()
                if ex_str.startswith("Exchange."):
                    ex_str = ex_str.split(".", 1)[1]
                exchange = Exchange(ex_str)
                symbol = str(row["symbol"]).strip()
                name = str(row.get("name", "") or "").strip()
                if symbol:
                    rows.append((symbol, exchange, name))
            except (ValueError, KeyError):
                continue
        return rows
    if "code" in df.columns:
        code_col, name_col = "code", "name" if "name" in df.columns else "名称"
        for _, row in df.iterrows():
            code = str(row[code_col]).strip()
            parsed = _parse_code_to_symbol_exchange(code)
            if parsed:
                symbol, exchange = parsed
            else:
                symbol = code[-6:].zfill(6) if len(code) >= 6 else code.zfill(6)
                if len(symbol) != 6:
                    continue
                exchange = _symbol_to_exchange(symbol)
            name = str(row.get(name_col, "") or "").strip() if name_col in df.columns else ""
            rows.append((symbol, exchange, name))
        return rows
    return []


def run_download(
    data_dir: Path,
    start_date: str,
    end_date: str,
    skip_existing: bool = True,
    limit: int | None = None,
    stock_list_file: Path | None = None,
) -> None:
    """拉取全市场日/周/月线并保存到本地目录。"""
    if stock_list_file and stock_list_file.exists():
        stock_list = load_stock_list_from_file(stock_list_file)
    else:
        stock_list = get_stock_list()
    if not stock_list:
        print("未获取到 A 股列表。请先运行 --save-stock-list 生成列表，或用 --stock-list-file 指定已保存的 CSV。")
        return
    if limit is not None and limit > 0:
        stock_list = stock_list[:limit]
        print(f"仅处理前 {limit} 只（测试模式）")
    print(f"共 {len(stock_list)} 只 A 股，时间范围 {start_date} ~ {end_date}，保存到 {data_dir}")
    for interval_enum, period in INTERVALS:
        (data_dir / period).mkdir(parents=True, exist_ok=True)
    total_files = 0
    failed = 0
    for i, (symbol, exchange, name) in enumerate(stock_list):
        if (i + 1) % 200 == 0 or i == 0:
            print(f"进度: {i+1}/{len(stock_list)} {symbol} {name or ''}")
        for interval_enum, period in INTERVALS:
            out_file = data_dir / period / f"{symbol}.{exchange.value}.csv"
            if skip_existing and out_file.exists():
                total_files += 1
                continue
            df = fetch_bars_akshare(symbol, period, start_date, end_date)
            time.sleep(REQUEST_DELAY)
            if df is None or df.empty:
                failed += 1
                continue
            if interval_enum is not None:
                bars = df_to_bar_data(df, symbol, exchange, interval_enum)
                if bars:
                    save_bars_to_csv(bars, out_file)
                    total_files += 1
            else:
                # 月线：仅落盘同一格式的 CSV，不写入数据库
                if not df.empty:
                    _save_akshare_df_to_csv(df, out_file)
                    total_files += 1
    print(f"下载完成，有效文件数: {total_files}，失败/跳过: {failed}")


def run_import(data_dir: Path, batch_size: int = 5000) -> None:
    """将本地 CSV 导入当前配置的数据库（如 SQLite）。仅导入日线、周线。"""
    from vnpy.trader.database import get_database
    db = get_database()
    imported = 0
    for interval_enum, period in INTERVALS_FOR_DB:
        dir_path = data_dir / period
        if not dir_path.exists():
            continue
        csv_files = list(dir_path.glob("*.csv"))
        print(f"导入 {period}: {len(csv_files)} 个文件")
        for fp in csv_files:
            # 文件名格式: symbol.exchange.csv
            stem = fp.stem
            if "." not in stem:
                continue
            symbol, exchange_str = stem.rsplit(".", 1)
            try:
                exchange = Exchange(exchange_str)
            except ValueError:
                continue
            bars = load_bars_from_csv(fp, symbol, exchange, interval_enum)
            if not bars:
                continue
            for i in range(0, len(bars), batch_size):
                chunk = bars[i : i + batch_size]
                if db.save_bar_data(chunk):
                    imported += len(chunk)
    print(f"导入完成，共写入 {imported} 条 K 线")


def main():
    parser = argparse.ArgumentParser(description="AKShare A 股全市场日/周/月线拉取并导入数据库")
    parser.add_argument("--data-dir", type=str, default="data/akshare_bars", help="本地存储目录")
    parser.add_argument("--start", type=str, default=DEFAULT_START, help="开始日期 YYYYMMDD")
    parser.add_argument("--end", type=str, default=DEFAULT_END, help="结束日期 YYYYMMDD")
    parser.add_argument("--download-only", action="store_true", help="仅下载到本地，不导入数据库")
    parser.add_argument("--import-only", action="store_true", help="仅从本地文件导入数据库")
    parser.add_argument("--no-skip-existing", action="store_true", help="下载时覆盖已存在的 CSV")
    parser.add_argument("--limit", type=int, default=None, help="仅处理前 N 只股票（测试用）")
    parser.add_argument("--save-stock-list", action="store_true", help="仅获取 A 股列表并保存到 data-dir/stock_list.csv 后退出")
    parser.add_argument("--stock-list-file", type=str, default=None, help="从指定 CSV 读取股票列表（避免后台运行时获取列表失败）")
    args = parser.parse_args()
    data_dir = project_root / args.data_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    if args.import_only:
        run_import(data_dir)
        return
    if getattr(args, "save_stock_list", False):
        lst = get_stock_list()
        if not lst:
            print("未获取到 A 股列表，请检查 akshare 与网络")
            sys.exit(1)
        out = data_dir / "stock_list.csv"
        rows = [(s, e.value if hasattr(e, "value") else str(e), n) for s, e, n in lst]
        pd.DataFrame(rows, columns=["symbol", "exchange", "name"]).to_csv(out, index=False, encoding="utf-8-sig")
        print(f"已保存 {len(lst)} 只股票到 {out}")
        return
    run_download(
        data_dir,
        start_date=args.start,
        end_date=args.end,
        skip_existing=not args.no_skip_existing,
        limit=args.limit,
        stock_list_file=Path(args.stock_list_file) if args.stock_list_file else None,
    )
    if not args.download_only:
        run_import(data_dir)


if __name__ == "__main__":
    main()
