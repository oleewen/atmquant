#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件连接配置（如 CTP）
从 .env 读取 CTP_* 变量，未配置时使用 SimNow 7x24 环境占位。
"""

import os
from pathlib import Path
from typing import Any


def _load_env() -> None:
    """加载项目根目录 .env 到环境变量"""
    for parent in Path(__file__).resolve().parents:
        env_path = parent / ".env"
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip())
            except Exception:
                pass
            break


_load_env()

# SimNow 7x24 模拟环境默认地址（供测试/未配置时使用）
SIMNOW_TD = "180.168.146.187:10201"
SIMNOW_MD = "180.168.146.187:10211"

# SimNow交易时段环境配置
#SIMNOW_TD = "182.254.243.31:30001"
#SIMNOW_MD = "182.254.243.31:30011"

# CTP 连接配置：优先从环境变量 CTP_* 读取
CURRENT_CTP_SETTINGS: dict[str, Any] = {
    "用户名": os.getenv("CTP_USER", "your_simnow_account"),
    "密码": os.getenv("CTP_PASSWORD", ""),
    "经纪商代码": os.getenv("CTP_BROKER", "9999"),
    "交易服务器": os.getenv("CTP_TD_ADDRESS", SIMNOW_TD),
    "行情服务器": os.getenv("CTP_MD_ADDRESS", SIMNOW_MD),
    "产品名称": os.getenv("CTP_APP_ID", "simnow_client_test"),
    "授权编码": os.getenv("CTP_AUTH_CODE", "0000000000000000"),
}
