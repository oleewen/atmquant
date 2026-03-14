#!/usr/bin/env bash
# ATMQuant 启动脚本：激活虚拟环境、检查/启动 MySQL、运行 main.py
# 使用: 在项目根目录执行 ./scripts/restart.sh 或 bash scripts/restart.sh

set -e
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "[restart] 项目目录: $REPO_ROOT"

# 1) 激活虚拟环境
VENV="$REPO_ROOT/venv"
if [[ ! -d "$VENV" ]]; then
    echo "[restart] 错误: 未找到虚拟环境 $VENV，请先执行 python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi
echo "[restart] 激活虚拟环境: $VENV"
# shellcheck source=../venv/bin/activate
source "$VENV/bin/activate"

# 2) 若使用 MySQL，检查并尝试启动 MySQL
if [[ -f "$REPO_ROOT/.env" ]]; then
    # 简单解析 .env 中的 DATABASE_TYPE（不依赖 python）
    if grep -q '^[[:space:]]*DATABASE_TYPE[[:space:]]*=[[:space:]]*mysql' "$REPO_ROOT/.env" 2>/dev/null; then
        echo "[restart] 检测到 MySQL 配置，检查 MySQL 服务..."
        if command -v mysqladmin &>/dev/null; then
            if mysqladmin ping 2>/dev/null; then
                echo "[restart] ✓ MySQL 已运行"
            else
                echo "[restart] MySQL 未响应，尝试启动..."
                if command -v brew &>/dev/null && brew services list 2>/dev/null | grep -q mysql; then
                    brew services start mysql 2>/dev/null || true
                    sleep 2
                fi
                if command -v mysql.server &>/dev/null; then
                    mysql.server start 2>/dev/null || true
                    sleep 2
                fi
                if mysqladmin ping 2>/dev/null; then
                    echo "[restart] ✓ MySQL 已启动"
                else
                    echo "[restart] ⚠️  MySQL 仍无法连接，请手动启动后重试（如: brew services start mysql 或 mysql.server start）"
                    if [[ -t 0 ]]; then
                        read -r -p "是否继续启动程序? [y/N] " -n 1; echo
                        if [[ ! "$REPLY" =~ ^[yY]$ ]]; then
                            exit 1
                        fi
                    else
                        echo "[restart] 非交互模式，继续启动程序"
                    fi
                fi
            fi
        else
            echo "[restart] ⚠️  未找到 mysqladmin，跳过 MySQL 检查（请确保 MySQL 已启动）"
        fi
    fi
fi

# 3) 启动主程序
echo "[restart] 启动: python main.py"
exec python main.py "$@"
