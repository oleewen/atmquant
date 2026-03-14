---
project_name: 'atmquant'
user_name: 'Only'
date: '2026-03-14'
sections_completed: ['technology_stack', 'critical_rules']
existing_patterns_found: 4
---

# AI Agent 工程上下文 (Project Context)

_本文件包含 AI Agent 在本项目中实现代码时必须遵循的关键规则和模式。重点关注那些 Agent 可能会忽略的非显而易见细节。_

---

## 技术栈与版本 (Technology Stack & Versions)

- **语言**: Python 3.x
- **框架**: 基于 `vnpy 4.1` 的自定义实现（在 `vnpy/` 目录下有本地核心修改）
- **核心库**:
    - `PySide6`: GUI 界面 (版本 6.8.2.1)
    - `vnpy_ctastrategy`, `vnpy_ctabacktester`, `vnpy_chartwizard`: vnpy 核心应用模块
    - `numpy`, `pandas`, `ta-lib`: 数据处理与技术指标计算
    - `sqlalchemy`, `pymysql`: 数据库支持 (MySQL)
    - `loguru`: 日志系统
    - `akshare`, `vnpy_tushare`: 实时与历史数据源
- **测试**: `pytest`, `pytest-cov`

## 关键实现规则 (Critical Implementation Rules)

### 全局规则
- **语言规则**: 始终使用中文响应，生成中文内容、注释和文档。
- **内容生成**: 确保所有新生成的代码包含完整的中文文档字符串和注释。

### 策略开发规范
- **继承要求**: 必须继承 [base_strategy.py](file:///Users/only/workspaces/atmquant/core/strategies/base_strategy.py) 而非原始的 `CtaTemplate`。
- **生命周期**: 必须实现标准的生命周期钩子（如 `on_init`, `on_start`, `on_bar` 等）。
- **参数定义**: 必须在类级别明确定义 `parameters` 和 `variables` 列表。

### 日志与告警
- **统一接口**: 严禁使用 `print()`，必须统一使用 `self.logger` 或 [logger_manager.py](file:///Users/only/workspaces/atmquant/core/logging/logger_manager.py) 提供的日志能力。
- **告警机制**: 关键错误必须触发告警通知。

### 框架扩展与修改
- **本地优先**: 注意 [vnpy/](file:///Users/only/workspaces/atmquant/vnpy/) 目录下的本地代码修改，在开发相关功能时应优先参考本地实现而非官方文档。
- **模块化**: 新增功能应尽量保持模块化，避免侵入性修改核心引擎代码。

### 数据处理
- **数据源**: 优先使用 `akshare` 获取数据，确保数据格式与 `vnpy` 标准 `BarData` 兼容。
- **指标计算**: 使用 `ta-lib` 或 `vnpy.trader.utility.ArrayManager` 进行指标计算，避免手动实现复杂算法。

### 测试规范 (Testing Rules)
- **框架**: 使用 `pytest` 作为测试框架。
- **文件结构**: 测试文件必须放置在 `tests/` 目录下，并按照 `unit/`（单元测试）和 `integration/`（集成测试）分类。
- **命名规范**: 测试文件以 `test_` 开头，测试类以 `Test` 开头，测试方法以 `test_` 开头。
- **Mock 使用**: 涉及网络请求（如数据获取、API调用）的测试必须使用 Mock，严禁在单元测试中发起真实网络请求。
- **覆盖率**: 核心业务逻辑（如策略算法、订单管理）应追求高覆盖率。

### 代码质量与风格 (Code Quality & Style)
- **风格指南**: 遵循 PEP 8 编码规范。
- **类型提示**: 所有新函数和方法必须包含 Python 类型提示 (Type Hints)。
- **文档字符串**: 所有类和函数必须包含中文文档字符串 (Docstrings)，描述功能、参数和返回值。
- **导入规范**:
    1. 标准库导入
    2. 第三方库导入
    3. 本地项目导入（使用绝对导入，如 `from core.strategies import ...`）

### 开发工作流 (Development Workflow)
- **分支管理**: 开发新功能或修复 Bug 时，请基于 `main` 分支创建新的分支（如 `feature/xxx` 或 `fix/xxx`）。
- **提交信息**: 提交信息必须清晰描述变更内容（建议使用中文）。
- **验证**: 在提交代码前，必须确保本地运行测试通过 (`pytest`)。
