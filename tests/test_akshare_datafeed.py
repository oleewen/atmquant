# -*- coding: utf-8 -*-
"""AKShare 数据源模块与接口测试。"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

import pytest

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import HistoryRequest


@pytest.fixture(scope="module")
def apply_config():
    """确保配置已加载（datafeed 名由环境决定，不强制 akshare）。"""
    from config.settings import apply_settings
    apply_settings()


def test_akshare_module_import():
    """能正确导入 vnpy_akshare 并得到 Datafeed 类。"""
    from vnpy_akshare import Datafeed
    assert Datafeed is not None
    feed = Datafeed()
    assert feed.init() in (True, False)  # False 仅当未安装 akshare


def test_akshare_datafeed_interface(apply_config):
    """AkshareDatafeed 实现 init / query_bar_history / query_tick_history。"""
    from vnpy_akshare import Datafeed
    from vnpy.trader.datafeed import BaseDatafeed

    feed = Datafeed()
    assert isinstance(feed, BaseDatafeed)
    assert hasattr(feed, "init")
    assert hasattr(feed, "query_bar_history")
    assert hasattr(feed, "query_tick_history")


@pytest.mark.skipif(
    os.getenv("DATAFEED_NAME") != "akshare",
    reason="仅当 DATAFEED_NAME=akshare 时请求 AKShare 接口",
)
def test_akshare_query_stock_bars(apply_config):
    """当使用 akshare 数据源时，能拉取 A 股日线（需网络）。"""
    try:
        import akshare as ak  # noqa: F401
    except ImportError:
        pytest.skip("未安装 akshare")

    from vnpy_akshare import Datafeed
    from vnpy.trader.utility import ZoneInfo

    tz = ZoneInfo("Asia/Shanghai")
    end = datetime.now(tz)
    start = end - timedelta(days=30)
    req = HistoryRequest(
        symbol="600519",
        exchange=Exchange.SSE,
        start=start,
        end=end,
        interval=Interval.DAILY,
    )
    feed = Datafeed()
    out_lines = []
    output = lambda msg: out_lines.append(str(msg))
    bars = feed.query_bar_history(req, output=output)
    assert isinstance(bars, list)
    if bars:
        assert len(bars) > 0
        b = bars[0]
        assert b.symbol == "600519"
        assert b.exchange == Exchange.SSE
        assert b.interval == Interval.DAILY
        assert b.gateway_name == "AKShare"
        assert b.open_price > 0 and b.close_price > 0
