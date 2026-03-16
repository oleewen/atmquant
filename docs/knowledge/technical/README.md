# technical — 技术视角（ATMQuant）

本目录描述 **ATMQuant 的物理实现、模块划分与接口**。与业务、产品、数据视角通过 ID 显式关联。

- **系统架构总览**：[SYSTEM-ARCHITECTURE.md](./SYSTEM-ARCHITECTURE.md)（系统职责、边界与模块关系）
- **SYS-ATMQUANT**：[SYS-ATMQUANT/README.md](./SYS-ATMQUANT/README.md)（应用/模块索引与业务映射）

---

## 技术索引表

| 类型 | 名称           | ID             | 路径     | 说明                     |
|------|----------------|----------------|----------|--------------------------|
| 系统 | ATMQuant 交易系统 | SYS-ATMQUANT   | [SYS-ATMQUANT](./SYS-ATMQUANT/) | 单体应用；图表、指标、策略、回测、数据、日志 |

---

## 层级结构

```
系统 (SYS) → 应用/模块 (APP 或包)
```

本项目为单体应用，不拆微服务；「应用」对应代码包或 vnpy App（如 core、config、vnpy_chartwizard、vnpy_ctastrategy）。

---

## 与其他视角的映射

- **技术 ← 业务**：business 限界上下文的 `implemented_by_app_id` 指向本系统内模块或包。
- **技术 ← 产品**：product 功能点的 `invokes_api_ids` 可指向本系统内接口或模块。

更多见 [INDEX.md](../../INDEX.md) 与 [DESIGN.md](../../DESIGN.md)。
