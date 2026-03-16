# data — 数据视角（ATMQuant）

本目录描述 **ATMQuant 数据存储、数据实体与治理属性**。与业务、技术视角通过 ID 显式关联。

- **数据架构总览**：[DATA-ARCHITECTURE.md](./DATA-ARCHITECTURE.md)（存储全景、核心实体与数据流）

---

## 层级结构

```
数据存储 (DS) → 数据实体 (ENT)
```

- **数据存储**：如 MySQL、SQLite、.env、文件系统，目录 `{DS-ID}/`，含 `_meta.yaml`。
- **数据实体**：表或逻辑实体，文件 `schema/{ENT-ID}.yaml`。

---

## 元数据约定

### 数据存储 _meta.yaml

| 字段 | 说明 |
|------|------|
| id, name, description | 存储标识与描述 |
| type | 如 MySQL / SQLite / File / Env |
| app_id | 归属的 technical 应用/模块 ID（可选） |

### 数据实体 YAML

| 字段 | 说明 |
|------|------|
| id, name, description | 实体标识与描述 |
| fields | 字段列表（name, type, is_primary 等） |
| maps_to_aggregate_id | 对应的 business 聚合根 ID（可选） |

---

## 本视角内示例

- 数据架构与实体概览：[DATA-ARCHITECTURE.md](./DATA-ARCHITECTURE.md)
- 若需按 DS/ENT 细分，可在本目录下新建 `{DS-ID}/` 与 `schema/{ENT-ID}.yaml`。

---

## 与其他视角的映射

- **数据 ← 业务**：聚合的 `persisted_as_entity_ids` 指向本层 ENT；ENT 的 `maps_to_aggregate_id` 指向 business 的 AGG。
- **数据 ← 技术**：数据存储的 `app_id` 指向 technical 的模块或应用。

更多见 [INDEX.md](../../INDEX.md) 与 [DESIGN.md](../../DESIGN.md)。
