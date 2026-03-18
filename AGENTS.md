# ATMQuant AI Agents

## 角色与行为

- **语言规则**：始终使用中文响应用户请求；生成内容、注释和文档均为中文。
- **先思考后编码**：先分析问题并提出方案，在生成大量代码前可等待确认（除非用户另有指示）。
- **先阅读再改**：修改任何被引用的文件前，先阅读其内容或通过文档/AGENTS 查询。

## 项目概述

ATMQuant 是基于 vnpy 4.1 的开源 AI 量化交易框架，专注于图表可视化与策略研发。核心能力包括多周期图表、技术指标库、策略开发与回测、轻量配置与日志告警。完整介绍见 `README.md`。

## 关键路径

- **源码**：`core/`（charts、indicators、data、logging、strategies）、`config/`、`vnpy_*` 插件
- **测试**：`tests/`（unit、integration、backtest）
- **配置**：`config/`、`.env`（见 `.env.example`）
- **文档**：`docs/`（AI 可检索总索引 `docs/INDEX.md`；应用文档 `docs/application/`；系统知识库 `docs/system/`）
- **脚本**：`main.py`（入口）；`scripts/`（如存在，见 `docs/INDEX.md` 的未索引声明）

## 技术栈

- **语言**：Python 3.10+
- **框架**：vnpy 4.1、PySide6、pyqtgraph
- **依赖**：见 `requirements.txt`（numpy、pandas、ta-lib、loguru、python-dotenv 等）
- **代码风格**：PEP 8、类型注解、中文注释；遵从 `.ai/rules/` 与 `.ai/CONVENTIONS.md`

## 命令

```bash
# 虚拟环境与依赖
python3 -m venv venv && source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# 启动程序（自动加载 .env）
python main.py

# 测试
pytest
pytest tests/unit -v
pytest tests/ --cov=core --cov-report=term-missing
```

## 开发规范

- **提交**：Conventional Commits（feat/fix/docs/style/refactor/test/chore），中文描述可接受。
- **文档与需求**：澄清需求与设计优先于实现；系统级知识库/方案/需求流程入口见 `docs/system/INDEX.md`；AI 检索地图见 `docs/INDEX.md`。
- **测试**：修改或新增逻辑时优先考虑测试；不删除或跳过已有测试。

## 参考文档

- **项目与启动**：`README.md`
- **文档体系与知识库**：`docs/INDEX.md`、`docs/application/INDEX.md`、`docs/system/INDEX.md`、`docs/system/knowledge/README.md`
- **开发规范索引**：`.ai/CONVENTIONS.md`，规范源文件 `.ai/rules/`
