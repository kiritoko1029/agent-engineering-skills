# 来源与通用化说明

本仓库参考 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 的真实文件进行整理，不是只根据目录名或搜索摘要改写。参考快照为 [`c291e7961a515f6d7af9304e7fd1d257929aef26`](https://github.com/deepseek-ai/deepseek-harness/tree/c291e7961a515f6d7af9304e7fd1d257929aef26)，该提交时间为 2026-09-10，阅读与整理日期为 2026-09-12。以下链接固定到该快照，便于复核。

## 逐项映射

| 通用技能 | 主要来源 | 提取的核心做法 |
| --- | --- | --- |
| `dsh-archive-agent-notes` | [同名上游技能](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-archive-agent-notes/SKILL.md)、[Agent Notes 规范](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/README.md)、[implemented 规范](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/AGENTS.md)、[归档规范](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/archived/AGENTS.md) | 保留原技能结构与写作、替代、清理、归档规则，将必要规范随技能打包 |
| `agent-code-review` | [dsh-code-review](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-code-review/SKILL.md) | 沿真实调用路径证明触发条件与影响，不制造审查问题 |
| `agent-simplify` | [dsh-find-simplifications](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-find-simplifications/SKILL.md) | 区分实际消费者与测试，衡量删除能力的代价与净维护成本 |
| `agent-verify-change` | [dsh-pre-push-checks](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-pre-push-checks/SKILL.md)、[根 AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/AGENTS.md) | 将修改映射到所需证据；不默认全量，不重复已有有效检查 |
| `agent-ci-reliability` | [dsh-ci-test-reliability](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-ci-test-reliability/SKILL.md)、[CI 诊断参考](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-ci-test-reliability/references/ci-flake-diagnosis.md) | 从并发、资源、完成信号与清理路径诊断故障，修正原因 |
| `agent-performance` | [dsh-speed-up-perf](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-speed-up-perf/SKILL.md) | 固定工作负载，测量基线，验证瓶颈与正确性 |
| `agent-docs` | [dsh-doc](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-doc/SKILL.md)、[dsh-prose-standard](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-prose-standard/SKILL.md)、[dsh-trim-cot-leakage](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-trim-cot-leakage/SKILL.md) | 一个事实有维护位置；读者无需会话上下文也能理解；精简时保留条件和例外 |
| `agent-deliver-stack` | [dsh-merging-stacked-prs](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-merging-stacked-prs/SKILL.md) | 验证真实依赖、精确提交和每层状态；请求被接受不等于已合入 |
| `agent-change-journal` | 本仓库新增，借鉴上游记录可追溯结果的思路 | 把用户关注的每日总结明确为独立日志，保存进度和接续入口 |

## 笔记中的可复用经验

除了技能入口，也阅读了笔记规范与具体记录，判断哪些内容值得长期保留：

- [统一决策记录格式](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/process/2026-07-05-uniform-agent-note-format.md)：用状态和备选方案区分提议、事实与被拒绝的选择。
- [文档层级与预算](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/process/2026-07-04-doc-tiers-and-budgets.md)：先明确内容归属，避免在多个入口复制规则。
- [具体表述与可核实事实](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/process/2026-08-09-concrete-prose-names-actors-and-recorded-facts.md)：写清主体、动作和来源，而不是用抽象词遮住缺失的事实。
- [冻结归档](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/process/2026-07-26-frozen-agent-note-archive.md)：区分需要维护的当前事实与已经封存的历史。
- [移除集中笔记索引](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/implemented/process/2026-07-19-remove-generated-agent-note-index.md)：沿用目录与检索作为活跃笔记清单，不另建集中索引。
- [被拒绝的组件合并](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/rejected/simplification/2026-07-19-fold-compaction-package-split.md) 与 [待实施的变异测试](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/notes/proposed/testing/2026-06-11-mutation-testing.md)：保留状态与拒绝理由，避免后来者把未采用方案误读成当前实现。

## Agent Notes 的最小适配

[dsh-archive-agent-notes](../skills/dsh-archive-agent-notes/SKILL.md) 保留上游名称、英文原文结构和核心语义。写作、已实施记录与归档规范放在技能自身的 `references/` 中，单独安装即可读取。上游案例保留并注明来源。

| 实际适配 | 原因 |
| --- | --- |
| 必需规范的跨仓库相对链接改为包内链接；历史依据链接固定提交 | 单独安装后仍可读取规范与追溯依据 |
| 英文、中文、sidecar 三件套改为正文及项目实际存在的配套文件 | 目标项目不一定维护同一套双语系统；已有配套文件仍须整体处理 |
| 专属 `pnpm` 和哈希校验器改为项目实际校验；没有校验器时明确人工核对与限制 | 不要求使用者引入 DeepSeek 的构建系统，也不声称具备未提供的自动冻结校验 |

非平凡改动必须新增或更新笔记、三种活跃状态、六种分类、标准章节、真实备选方案、同主题替代审查、完整合并前保留独特理据、按未来价值归档以及归档正文永久冻结，均保留上游规则。归档时不修正文或出链；只修活跃资料的入链。清理失去价值的 rejected 笔记仍按原规则处理，任务范围与执行权限由用户和项目决定。

初版的 `agent-decision-notes` 与 `agent-note-maintenance` 两个入口由上游同名技能取代。已安装初版的项目需核对本地修改后移除旧入口，避免重复触发；安装器不会自动删除已安装目录。每日日志仍是独立补充。

## 其他技能的适配

其他技能保留各自已说明的通用化范围；本次只收敛 Agent Notes，不把整套仓库描述为逐字复制的上游发行版。

| 上游约定或实现 | 本仓库的处理及原因 |
| --- | --- |
| 文档模板、字数预算与等行双语 | 按读者任务组织内容，保留必要约束，不强制特定版式 |
| 必须运行的 `pnpm` 命令和项目覆盖门槛 | 从使用者项目读取真实命令与要求，按变更选择充分证据 |
| Cordis 插件、事件、SDK 等领域规则 | 不作为通用规则移植；需要时在项目自身规范中定义 |
| GitHub 原生 stack 与固定 CLI | 保留依赖和状态核验原则，具体同步与合入使用平台已支持的流程 |
| 工作流中的预设动作 | 用户请求和现有授权决定范围；加载技能本身不授权发布、合入或清理 |

## 没有独立移植的技能

[dsh-translate-docs](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/dsh-translate-docs/SKILL.md) 深度依赖该仓库的双语配对系统。这里仅在 `agent-docs` 保留“已有翻译按改动范围同步”的原则，不引入整套翻译基础设施。

[record-browser-gif](https://github.com/deepseek-ai/deepseek-harness/blob/c291e7961a515f6d7af9304e7fd1d257929aef26/.agents/skills/record-browser-gif/SKILL.md) 依赖浏览器控制、编码与发布工具，也包含每次 GUI PR 必须录制的项目约定。本仓库不将它作为所有工程任务的通用要求；需要此能力时可另建针对目标浏览器的技能。

本仓库没有搬运上游运行时代码、自动化脚本或整批历史笔记。日志、模板、安装与校验工具是为通用使用新增；[LICENSE](../LICENSE) 与 [NOTICE](../NOTICE.md) 保留归因和分发许可。
