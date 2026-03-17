# ATMQuant - 开发指南

**日期：** 2026-03-17

## 环境要求

- **Python：** 3.10 或更高
- **系统：** 支持 PySide6 的 Windows / macOS / Linux
- **可选：** CTP 等交易/数据账号、MySQL（若不用默认 SQLite）

## 环境搭建

### 1. 克隆与虚拟环境

```bash
# 进入项目目录
cd atmquant

# 创建虚拟环境
python3 -m venv venv

# 激活（Linux/macOS）
source venv/bin/activate

# 激活（Windows）
# venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

说明：TA-Lib 可能需要系统级安装（如 `brew install ta-lib`），再 `pip install ta-lib`。

### 3. 配置

```bash
cp .env.example .env
# 编辑 .env：数据库、数据源、告警等（见 .env.example 注释）
```

- **数据库：** 默认 `DATABASE_TYPE=sqlite`、`DATABASE_NAME=atmquant.db`；用 MySQL 时填写 `DATABASE_HOST/PORT/USER/PASSWORD`。
- **数据源：** `DATAFEED_NAME` 与安装的数据源对应（如 tushare、akshare）。
- **告警：** 飞书/钉钉机器人可填 `FEISHU_*` / `DINGTALK_*`。

## 本地运行

```bash
# 确保已激活 venv 并安装依赖、配置 .env
python main.py
```

程序会加载 `.env`、创建事件引擎与主引擎、注册 CTP/CTA 策略/回测/ChartWizard、打开主窗口。

## 构建与打包

- 项目当前以源码运行为主，无内置构建/打包脚本；若需打包可自行使用 PyInstaller 等并依赖 PySide6 与 vnpy 文档。

## 测试

```bash
# 全部测试
pytest

# 仅单元测试、详细输出
pytest tests/unit -v

# 带覆盖率（core）
pytest tests/ --cov=core --cov-report=term-missing
```

- 测试目录：`tests/unit`、`tests/integration`、`tests/backtest`。
- 配置与 fixture：见 `tests/conftest.py`。

## 常用开发任务

- **改配置：** 修改 `config/settings.py` 或 `.env`，必要时改 `config/alert_config.py`、`config/futures_config.py` 等。
- **新增指标：** 在 `core/indicators/` 新增 `*_item.py`，实现 `ChartItem` + `ConfigurableIndicator`；若需在界面扩展列表中出现，在 `core/charts/enhanced_chart_widget.py` 的 `EXTENDED_INDICATORS_CONFIG` 中注册。
- **新增策略：** 在 `core/strategies/` 继承 `BaseCtaStrategy`，按 vnpy CTA 规范实现 `on_tick`/`on_bar` 等；在 CTA 策略 App 中加载使用。
- **回测：** 使用 vnpy_ctabacktester 界面或 `scripts/backtest_3ma_strategy.py` 等脚本。

## 代码规范

- 遵循 PEP 8，使用类型注解与中文注释（见 AGENTS.md、.ai/CONVENTIONS.md）。
- 提交信息建议 Conventional Commits：feat / fix / docs / style / refactor / test / chore。

## 文档与知识库

- 仓库文档中心：`docs/README.md`。
- 本工程文档索引：`docs/index.md`。
- 知识库：`docs/knowledge/`（四视角 + 宪法层）。

---

_由 BMAD document-project 工作流生成_
