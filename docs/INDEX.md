# ATMQuant 知识库 — 全局索引

本索引按**业务知识、解决方案、需求分析、需求交付**组织。设计依据见 [DESIGN.md](./DESIGN.md)（若存在）。

---

## 一、业务知识 (knowledge)

知识库主体，包含宪法层与四视角（业务、产品、技术、数据）。

### 1.1 宪法与治理层 (constitution)

| 入口 | 说明 |
|------|------|
| [knowledge/constitution/README.md](./knowledge/constitution/README.md) | 宪法层使命与核心组件 |
| [knowledge/constitution/adr/](./knowledge/constitution/adr/) | 架构决策记录 (ADR) |
| [knowledge/constitution/standards/](./knowledge/constitution/standards/) | 命名规范、ADR 模板等 |
| [knowledge/constitution/GLOSSARY.md](./knowledge/constitution/GLOSSARY.md) | 全局术语表（ATMQuant） |

### 1.2 业务视角 (business)

| 入口 | 说明 |
|------|------|
| [knowledge/business/README.md](./knowledge/business/README.md) | 业务视角说明、层级与映射字段 |
| 层级 | 业务域 (BD) → 子域 (BSD) → 限界上下文 (BC) → 聚合 (AGG) |
| 示例 | [BD-ATMQUANT](./knowledge/business/BD-ATMQUANT/) → [BSD-CHART](./knowledge/business/BD-ATMQUANT/BSD-CHART/) 等 |

**关键映射字段**：限界上下文 → 技术 `implemented_by_app_id`；聚合 → 数据 `persisted_as_entity_ids`。

### 1.3 产品视角 (product)

| 入口 | 说明 |
|------|------|
| [knowledge/product/README.md](./knowledge/product/README.md) | 产品视角说明、层级与映射字段 |
| 层级 | 产品线 (PL) → 模块 (PM) → 功能 (FT) → 用例 (UC) |
| 示例 | [PL-ATMQUANT](./knowledge/product/PL-ATMQUANT/) → [PM-CHART](./knowledge/product/PL-ATMQUANT/PM-CHART/) 等 |

**关键映射字段**：产品模块 → 业务 `relies_on_context_ids`；功能 → 技术 `invokes_api_ids`。

### 1.4 技术视角 (technical)

| 入口 | 说明 |
|------|------|
| [knowledge/technical/README.md](./knowledge/technical/README.md) | 技术视角说明、层级与映射字段 |
| 层级 | 系统 (SYS) → 应用/模块 |
| 示例 | [SYS-ATMQUANT](./knowledge/technical/SYS-ATMQUANT/) |

**关键映射字段**：限界上下文的 `implemented_by_app_id` 指向本层模块或包。

### 1.5 数据视角 (data)

| 入口 | 说明 |
|------|------|
| [knowledge/data/README.md](./knowledge/data/README.md) | 数据视角说明、层级与映射字段 |
| 层级 | 数据存储 (DS) → 数据实体 (ENT) |
| 示例 | [DATA-ARCHITECTURE.md](./knowledge/data/DATA-ARCHITECTURE.md) |

**关键映射字段**：数据实体 `maps_to_aggregate_id`；数据存储 `_meta.yaml` 中可写 `app_id`。

### 1.6 核心映射关系速查

| 关系方向 | 源 | 目标 | 关键字段/含义 |
|----------|-----|------|----------------|
| 落地实现 | 限界上下文 (BC) | 应用/模块 | `implemented_by_app_id` |
| 需求支撑 | 产品模块 (PM) | 限界上下文 (BC) | `relies_on_context_ids` |
| 数据持久化 | 聚合 (AGG) | 数据实体 (ENT) | `persisted_as_entity_ids` |
| 数据归属 | 数据实体 (ENT) | 模块 | 通过 DS 的 app_id 或 ENT 的 owned_by |

---

## 二、解决方案 (solutions)

| 入口 | 说明 |
|------|------|
| [solutions/README.md](./solutions/README.md) | 解决方案说明与命名规范 |
| 输出 | `solutions/SOLUTION-{ID}.md`；可归档至 `solutions/archive/` |

---

## 三、需求分析 (analysis)

| 入口 | 说明 |
|------|------|
| [analysis/README.md](./analysis/README.md) | 需求分析说明与命名规范 |
| 输出 | `analysis/REQUIREMENT-{ID}.md`；文档内 `parent` 指向对应 SOLUTION |

---

## 四、需求交付 (requirements)

| 入口 | 说明 |
|------|------|
| [requirements/README.md](./requirements/README.md) | 需求交付阶段目标、结构说明 |
| 输出 | `requirements/REQUIREMENT-{ID}/` 按阶段组织，含 PRD/ADD/TDD 等 |
