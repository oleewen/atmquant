# -*- coding: utf-8 -*-
"""
AKShare 数据源接口
支持 A 股日线/周线/月线与国内期货日线，与 vnpy 数据服务接口一致。
"""

from datetime import datetime, time
from collections.abc import Callable
from typing import List

import pandas as pd

from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData, HistoryRequest, TickData
from vnpy.trader.utility import ZoneInfo

CHINA_TZ = ZoneInfo("Asia/Shanghai")

# 交易所 -> AKShare get_futures_daily market 参数
EXCHANGE_TO_AK_MARKET = {
    Exchange.CFFEX: "CFFEX",
    Exchange.SHFE: "SHFE",
    Exchange.DCE: "DCE",
    Exchange.CZCE: "CZCE",
    Exchange.INE: "INE",
}

# 期货交易所集合（AKShare get_futures_daily 支持的）
AKSHARE_FUTURES_EXCHANGES = set(EXCHANGE_TO_AK_MARKET.keys())

# A 股交易所
STOCK_EXCHANGES = {Exchange.SSE, Exchange.SZSE}

# K 线周期 -> 股票 period 参数
INTERVAL_TO_AK_STOCK_PERIOD = {
    Interval.DAILY: "daily",
    Interval.WEEKLY: "weekly",
    Interval.MINUTE: None,  # 分钟需单独接口，暂不实现
}


def _parse_date_to_datetime(date_val, bar_time: time = time(15, 0)) -> datetime:
    """将日期转为带时区的 datetime（日线用收盘时间 15:00）。"""
    if hasattr(date_val, "strftime"):
        dt = datetime.combine(date_val, bar_time)
    else:
        s = str(date_val).replace("-", "")[:8]
        dt = datetime.strptime(s, "%Y%m%d").replace(tzinfo=CHINA_TZ)
        dt = dt.replace(hour=bar_time.hour, minute=bar_time.minute, second=0, microsecond=0)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CHINA_TZ)
    return dt


def _query_stock_bars(req: HistoryRequest, output: Callable) -> List[BarData]:
    """查询 A 股 K 线。"""
    try:
        import akshare as ak
    except ImportError:
        output("查询 A 股 K 线失败：请先安装 akshare，执行 pip install akshare")
        return []

    period = INTERVAL_TO_AK_STOCK_PERIOD.get(req.interval) if req.interval else "daily"
    if period is None:
        output("AKShare 数据源暂不支持该 K 线周期（如分钟线），请使用日线/周线/月线")
        return []

    start_str = req.start.strftime("%Y%m%d") if req.start else "19900101"
    end_str = req.end.strftime("%Y%m%d") if req.end else datetime.now(CHINA_TZ).strftime("%Y%m%d")

    try:
        df = ak.stock_zh_a_hist(
            symbol=req.symbol,
            period=period,
            start_date=start_str,
            end_date=end_str,
            adjust="qfq",
        )
    except Exception as e:
        output(f"AKShare 获取 A 股数据失败：{e}")
        return []

    if df is None or df.empty:
        return []

    # 列名兼容：AKShare 可能为 日期/开盘/收盘 或 日期/开盘价/收盘价 等
    date_col = "日期" if "日期" in df.columns else "date"
    if date_col not in df.columns:
        output("AKShare 返回的 A 股数据缺少日期列")
        return []

    open_col = "开盘" if "开盘" in df.columns else "开盘价"
    high_col = "最高" if "最高" in df.columns else "最高价"
    low_col = "最低" if "最低" in df.columns else "最低价"
    close_col = "收盘" if "收盘" in df.columns else "收盘价"
    vol_col = "成交量" if "成交量" in df.columns else "volume"
    turnover_col = "成交额" if "成交额" in df.columns else "成交金额" if "成交金额" in df.columns else None

    bars: List[BarData] = []
    for _, row in df.iterrows():
        dt = _parse_date_to_datetime(row[date_col])
        open_price = float(row[open_col])
        high_price = float(row[high_col])
        low_price = float(row[low_col])
        close_price = float(row[close_col])
        volume = float(row[vol_col])
        turnover = float(row[turnover_col]) if turnover_col and turnover_col in row else 0.0

        bar = BarData(
            symbol=req.symbol,
            exchange=req.exchange,
            interval=req.interval or Interval.DAILY,
            datetime=dt,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            volume=volume,
            turnover=turnover,
            gateway_name="AKShare",
        )
        bars.append(bar)
    return bars


def _query_futures_bars(req: HistoryRequest, output: Callable) -> List[BarData]:
    """查询国内期货日线（仅支持日线）。"""
    try:
        import akshare as ak
    except ImportError:
        output("查询期货 K 线失败：请先安装 akshare，执行 pip install akshare")
        return []

    if req.interval and req.interval != Interval.DAILY:
        output("AKShare 期货接口仅支持日线，请使用日线周期")
        return []

    market = EXCHANGE_TO_AK_MARKET.get(req.exchange)
    if not market:
        output(f"AKShare 暂不支持交易所 {req.exchange.value}，支持: CFFEX/SHFE/DCE/CZCE/INE")
        return []

    start_str = req.start.strftime("%Y%m%d") if req.start else "20100825"
    end_str = req.end.strftime("%Y%m%d") if req.end else datetime.now(CHINA_TZ).strftime("%Y%m%d")

    try:
        df = ak.get_futures_daily(
            start_date=start_str,
            end_date=end_str,
            market=market,
            index_bar=False,
        )
    except Exception as e:
        output(f"AKShare 获取期货数据失败：{e}")
        return []

    if df is None or df.empty:
        return []

    # 合约代码统一大写比较
    want_symbol = req.symbol.upper().strip()
    df = df[df["symbol"].astype(str).str.upper().str.strip() == want_symbol]
    if df.empty:
        output(f"未在 {market} 找到合约 {req.symbol} 在 {start_str}~{end_str} 的数据")
        return []

    bars = []
    for _, row in df.iterrows():
        date_val = row["date"]
        dt = _parse_date_to_datetime(date_val)
        try:
            open_p = float(row["open"])
            high_p = float(row["high"])
            low_p = float(row["low"])
            close_p = float(row["close"])
            vol = float(row["volume"]) if pd.notna(row.get("volume")) else 0.0
            oi = float(row["open_interest"]) if pd.notna(row.get("open_interest")) else 0.0
            turn = float(row["turnover"]) if pd.notna(row.get("turnover")) else 0.0
        except (TypeError, ValueError) as e:
            output(f"解析期货行失败: {e}")
            continue
        bar = BarData(
            symbol=req.symbol,
            exchange=req.exchange,
            interval=Interval.DAILY,
            datetime=dt,
            open_price=open_p,
            high_price=high_p,
            low_price=low_p,
            close_price=close_p,
            volume=vol,
            turnover=turn,
            open_interest=oi,
            gateway_name="AKShare",
        )
        bars.append(bar)
    return bars


class AkshareDatafeed(BaseDatafeed):
    """AKShare 数据服务：A 股日/周/月线 + 国内期货日线。"""

    def init(self, output: Callable = print) -> bool:
        """AKShare 无需登录，直接返回 True。"""
        try:
            import akshare as ak  # noqa: F401
            return True
        except ImportError:
            output("未安装 akshare，请执行: pip install akshare")
            return False

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> List[BarData]:
        """根据交易所类型分发到 A 股或期货接口。"""
        if req.exchange in STOCK_EXCHANGES:
            return _query_stock_bars(req, output)
        if req.exchange in AKSHARE_FUTURES_EXCHANGES:
            return _query_futures_bars(req, output)
        output(f"AKShare 数据源暂不支持交易所: {req.exchange.value}")
        return []

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> List[TickData]:
        """AKShare 不提供历史 Tick，返回空列表。"""
        output("AKShare 不支持历史 Tick 数据")
        return []
