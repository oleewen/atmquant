# business — 业务视角（ATMQuant）

本目录描述 **ATMQuant 业务版图、领域逻辑与规则**，不依赖具体技术实现。与产品、技术、数据视角通过 ID 显式关联。

---

## 业务索引表

| 类型       | 名称           | ID               | 路径     | 说明                     |
|------------|----------------|------------------|----------|--------------------------|
| 业务域     | 量化交易       | BD-ATMQUANT      | [BD-ATMQUANT](./BD-ATMQUANT/) | 图表、指标、策略、数据、日志 |
| 子域       | 图表与展示     | BSD-CHART        | [BSD-CHART](./BD-ATMQUANT/BSD-CHART/) | K 线、多周期、双图/四图、光标与视口 |
| 子域       | 指标计算       | BSD-INDICATOR    | [BSD-INDICATOR](./BD-ATMQUANT/BSD-INDICATOR/) | 技术指标计算与无头计算器 |
| 子域       | 策略与回测     | BSD-STRATEGY     | [BSD-STRATEGY](./BD-ATMQUANT/BSD-STRATEGY/) | 策略开发、回测、信号与执行 |
| 子域       | 数据与配置     | BSD-DATA         | [BSD-DATA](./BD-ATMQUANT/BSD-DATA/) | 数据源、Bar/Tick、配置与合约 |
| 子域       | 日志与告警     | BSD-LOGGING     | [BSD-LOGGING](./BD-ATMQUANT/BSD-LOGGING/) | 日志、告警机器人（飞书/钉钉等） |
| 限界上下文 | 图表展示       | BC-CHART-VIEW    | 见 BSD-CHART 下 | 多周期图表、双图/四图、交互 |
| 限界上下文 | 指标管理       | BC-INDICATOR-MGR | 见 BSD-INDICATOR 下 | 指标注册、参数、与图表/策略联动 |
| 限界上下文 | 策略执行与回测 | BC-STRATEGY-RUN | 见 BSD-STRATEGY 下 | 策略加载、回测引擎、实盘执行 |
| 限界上下文 | 数据接入与配置 | BC-DATA-CONFIG  | 见 BSD-DATA 下 | 数据源、环境配置、合约管理 |
| 限界上下文 | 日志告警       | BC-LOG-ALERT    | 见 BSD-LOGGING 下 | 日志分级、告警规则与推送 |

---

## 层级结构

```
业务域 (BD) → 业务子域 (BSD) → 限界上下文 (BC) → 聚合 (AGG)
```

- **业务域**：如 BD-ATMQUANT，目录 `{BD-ID}/`，含 `_meta.yaml`。
- **业务子域**：域下子划分，目录 `{BSD-ID}/`，含 `_meta.yaml`。
- **限界上下文**：DDD 边界与统一语言，目录 `{BC-ID}/`，含 `_meta.yaml` 与可选 `aggregates/`。
- **聚合**：以聚合根为核心的一致性边界，文件 `aggregates/{AGG-ID}.yaml`。

---

## 元数据约定

### _meta.yaml 常用字段

| 层级   | 建议字段 | 说明 |
|--------|----------|------|
| 业务域 | id, name, description, owner | 可选 strategic_classification：core_domain / supporting_domain / generic_domain |
| 子域   | id, name, description | |
| 限界上下文 | id, name, description, ubiquitous_language, **implemented_by_app_id** | **implemented_by_app_id**：实现该上下文的 technical 应用/模块 ID |

### 聚合 YAML 常用字段

- `id`, `name`, `description`, `root_entity`, `entities`, `invariants`
- **persisted_as_entity_ids**：持久化到的 data 数据实体 ID 列表（核心映射）

---

## 与其他视角的映射

- **业务 → 技术**：限界上下文的 `implemented_by_app_id` 指向 technical 的 APP 或模块。
- **业务 → 数据**：聚合的 `persisted_as_entity_ids` 指向 data 的 ENT。

更多见 [INDEX.md](../../INDEX.md) 与 [DESIGN.md](../../DESIGN.md)。
