# business — 业务视角

本目录描述**业务版图、领域逻辑与规则**，不依赖具体技术实现。与产品、技术、数据视角通过 ID 显式关联。

---

## 业务索引表

| 类型   | 名称         | ID            | 路径                                                              | 说明                      |
|--------|--------------|---------------|-------------------------------------------------------------------|---------------------------|
| 业务域 | 量化交易     | BD-ATMQUANT   | [BD-ATMQUANT](./BD-ATMQUANT/)                                      | ATMQuant 核心业务域        |
| 子域   | 图表与展示   | BSD-CHART     | [BSD-CHART](./BD-ATMQUANT/BSD-CHART/)                               | 多周期图表与交互展示        |
| 子域   | 指标计算     | BSD-INDICATOR | [BSD-INDICATOR](./BD-ATMQUANT/BSD-INDICATOR/)                       | 指标计算与配置/装载         |
| 子域   | 策略与回测   | BSD-STRATEGY  | [BSD-STRATEGY](./BD-ATMQUANT/BSD-STRATEGY/)                         | 策略运行与回测              |
| 子域   | 数据与配置   | BSD-DATA      | [BSD-DATA](./BD-ATMQUANT/BSD-DATA/)                                 | 数据源/数据库/运行配置       |
| 子域   | 日志与告警   | BSD-LOGGING   | [BSD-LOGGING](./BD-ATMQUANT/BSD-LOGGING/)                           | 日志与告警推送              |
| 限界上下文 | 图表展示 | BC-CHART-VIEW | [BC-CHART-VIEW](./BD-ATMQUANT/BSD-CHART/BC-CHART-VIEW/)               | 图表展示边界                |
| 限界上下文 | 指标管理 | BC-INDICATOR-MGR | [BC-INDICATOR-MGR](./BD-ATMQUANT/BSD-INDICATOR/BC-INDICATOR-MGR/)    | 指标配置与扩展装载           |
| 限界上下文 | 策略运行 | BC-STRATEGY-RUN | [BC-STRATEGY-RUN](./BD-ATMQUANT/BSD-STRATEGY/BC-STRATEGY-RUN/)        | 策略运行与回测边界           |
| 限界上下文 | 数据与配置 | BC-DATA-CONFIG | [BC-DATA-CONFIG](./BD-ATMQUANT/BSD-DATA/BC-DATA-CONFIG/)               | 运行配置与数据准备           |
| 限界上下文 | 日志与告警 | BC-LOG-ALERT | [BC-LOG-ALERT](./BD-ATMQUANT/BSD-LOGGING/BC-LOG-ALERT/)                | 日志与告警边界              |


---

## 层级结构

```
业务域 (BD) → 业务子域 (BSD) → 限界上下文 (BC) → 聚合 (AGG)
```

- **业务域**：如订单域、用户域，目录 `{BD-ID}/`，含 `_meta.yaml`。
- **业务子域**：域下子划分，如订单履约，目录 `{BSD-ID}/`，含 `_meta.yaml`。
- **限界上下文**：DDD 边界与统一语言，目录 `{BC-ID}/`，含 `_meta.yaml` 与 `aggregates/`。
- **聚合**：以聚合根为核心的一致性边界，文件 `aggregates/{AGG-ID}.yaml`。

---

## 元数据约定

### _meta.yaml 常用字段

| 层级 | 建议字段 | 说明 |
|------|----------|------|
| 业务域 | id, name, description, owner, strategic_classification | strategic_classification 可选：core_domain / supporting_domain / generic_domain |
| 子域 | id, name, description, domain_expert | |
| 限界上下文 | id, name, description, ubiquitous_language, implemented_by_app_id | **implemented_by_app_id**：实现该上下文的 technical 应用 ID |

### 聚合 YAML 常用字段

- `id`, `name`, `description`, `root_entity`, `entities`, `invariants`
- **persisted_as_entity_ids**：持久化到的 data 数据实体 ID 列表（核心映射）

---

## 与其他视角的映射

- **业务 → 技术**：限界上下文的 `implemented_by_app_id` 指向 technical 的 APP。
- **业务 → 数据**：聚合的 `persisted_as_entity_ids` 指向 data 的 ENT。

更多见仓库根目录 [INDEX.md](../../INDEX.md) 与 [DESIGN.md](../../DESIGN.md)。
