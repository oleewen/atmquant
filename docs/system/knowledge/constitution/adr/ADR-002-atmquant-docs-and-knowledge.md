# ADR-002: ATMQuant 文档根与知识库位置

## 状态

已通过 (Accepted)

## 上下文 (Context)

ATMQuant 为基于 vnpy 的 Python 单体应用，需将「文档体系」与「代码仓库」统一：文档中心、知识库、解决方案与需求分析均需有明确根路径，且与根目录 README 一致，便于 AI Agent 与贡献者定位。

## 决策 (Decision)

1. **文档根**：以仓库内 **`docs/`** 为文档中心根目录；根目录 `README.md` 通过「文档体系」小节明确指向 `docs/README.md` 与 `docs/INDEX.md`。
2. **知识库位置**：知识库主体位于 **`docs/knowledge/`**，包含 constitution、business、product、technical、data 五部分，与 [ADR-001](ADR-001-knowledge-repo-structure.md) 一致。
3. **索引约定**：全局索引与映射速查在 `docs/INDEX.md`；各视角入口为 `docs/knowledge/README.md` 及各子目录 README。
4. **Agent 指南**：项目根目录 `AGENTS.md` 中「关键路径」与「参考文档」明确列出 `docs/` 与 `docs/knowledge/`，与本文一致。

## 后果 (Consequences)

**正面**：

- 文档与代码同仓，版本一致；Agent 与人类均可从 README 快速进入文档体系。
- 知识库与 solutions/analysis/requirements 同处 docs 下，引用路径简单。

**负面**：

- 若未来拆出独立文档仓，需调整 README 与 AGENTS.md 中的路径说明。
