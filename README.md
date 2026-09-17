# Agent Engineering Skills

一组面向 AI Agent 协作开发的通用技能：用简短日志接续工作，用决策记录保留取舍，用与变更匹配的证据验证结果。

灵感来自 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 的 `.agents/notes` 和 `.agents/skills`。这里提供 **9 个可独立安装的技能**。Agent Notes 保留上游同名 `dsh-archive-agent-notes` 技能及必要规范，尽量少改写，英文原文也因此保留；其他技能采用通用化整理，并补充可选的日常工作日志。不依赖某个模型、编程语言或包管理器。

> 上游的 Agent Notes 主要是设计决策记录，并非每日流水。这个仓库把“今天做了什么”和“为什么这样设计”分开保存，既便于交接，也便于长期维护。

## 作为 Codex 插件安装

本仓库同时提供一个包含全部 9 个技能的 Codex 插件。仓库根目录的 `.codex-plugin/plugin.json` 声明插件，`.agents/plugins/marketplace.json` 提供仓库级插件目录；技能、模板、规范及许可证直接复用 `skills/`，无需构建或重复复制。

使用支持 `codex plugin` 命令的 Codex CLI，在本仓库根目录执行：

```sh
codex plugin marketplace add .
codex plugin add agent-engineering-skills@agent-engineering-skills
```

安装完成后新建 Codex 任务或 CLI 会话，再使用下文的 `$agent-code-review` 等技能。桌面端可在插件目录中选择 **Agent Engineering Skills** 来源并安装；如果未出现，重启应用。只需部分技能时，使用下一节的独立安装器，避免同时安装同名独立技能与整包插件。

以上方式读取本地文件。维护者将本次适配提交并推送到 GitHub 后，其他用户也可以使用远程仓库安装：

```sh
codex plugin marketplace add kiritoko1029/agent-engineering-skills
codex plugin add agent-engineering-skills@agent-engineering-skills
```

更新本地源码不会自动更新已安装缓存。发布更新时修改插件版本，更新 marketplace 来源后重新执行安装命令，并新建任务验证。卸载插件使用：

```sh
codex plugin remove agent-engineering-skills@agent-engineering-skills
```

适配依据为 [OpenAI 官方插件构建文档](https://developers.openai.com/plugins/build/plugins)中仍受支持的 Codex compatibility manifest 和仓库 marketplace 格式；本地安装验证范围见[验证记录](docs/validation.md)。

## 作为 ZCode 插件安装

本仓库同时是一个 ZCode 插件。根目录的 `.zcode-plugin/plugin.json` 声明插件，`marketplace.json` 提供插件目录；技能同样直接复用 `skills/`，与 Codex 整包、独立安装器互不影响。

在 ZCode 桌面端打开 **设置 → 插件**，通过 **创建 → 添加插件市场** 添加本仓库根目录作为本地市场；维护者推送后也可以直接添加 GitHub 仓库 `kiritoko1029/agent-engineering-skills`。从市场安装并启用 `agent-engineering-skills` 后，9 个技能即可在会话中按需触发。发布更新时同步修改 `.zcode-plugin/plugin.json` 与 `marketplace.json` 中的版本号，再在「市场源」面板刷新市场并重新安装；ZCode 以 marketplace 中的版本判断更新，两处不同步会漏报新版。

适配依据为 [ZCode 官方插件文档](https://zcode.z.ai/cn/docs/plugin)。本地已完成清单与校验器的静态验证（见[验证记录](docs/validation.md)）；桌面端的市场添加、安装、启用和技能触发需在客户端按上述步骤实际验证。

## 作为 Kimi Code 插件安装

仓库根目录的 `kimi.plugin.json` 将现有 `skills/` 打包为一个 Kimi Code 插件，包含全部 9 个技能及其模板、参考规范和许可证。按需加载技能，不添加会话启动注入、命令、Hooks 或 MCP 服务。

在支持 Plugins 的 Kimi Code **会话输入框**中执行以下斜杠命令（不是终端 shell 命令）：

```text
/plugins install https://github.com/kiritoko1029/agent-engineering-skills/tree/main
/reload
/plugins info agent-engineering-skills
```

这里指定 `main`，直接安装该分支版本；也可将 `main` 换成具体提交以固定版本。若安装本地源码，把 `/plugins install` 后的 URL 换成克隆后的仓库绝对路径。安装后可以按需调用，例如：

```text
/skill:agent-code-review 审查当前工作区相对 main 的改动。
```

Kimi Code 使用托管副本，编辑本地源码不会自动更新已安装插件；更新后重新安装并执行 `/reload`。插件为用户级安装，对该 Kimi Code 用户的项目生效；避免同时独立安装同名技能。需要停用或移除时，分别运行 `/plugins disable agent-engineering-skills` 或 `/plugins remove agent-engineering-skills`，再执行 `/reload`。

适配依据为 [Kimi Code 官方插件文档](https://www.kimi.com/code/docs/kimi-code-cli/customization/plugins)。本地实际安装与资源完整性验证见[验证记录](docs/validation.md)。原有 ZCode `marketplace.json` 继续用于 ZCode；Kimi 直接按仓库 URL 安装，无需额外市场文件。

## 从这里开始

先采用 `dsh-archive-agent-notes` 管理决策记录及其生命周期；需要日常总结时再加上可选的 `agent-change-journal`。其他技能在审查、排障或交付时按需使用。下面的示例同时安装 Notes 和日志技能。

仓库可以直接阅读或下载 ZIP 使用；私有仓库需要拥有读取权限。安装、校验工具需要 **Python 3.10+**，只使用标准库；没有 Python 也可以手动复制完整技能目录。下面先克隆并进入仓库，再从仓库根目录执行安装命令；系统只有 `python3` 时将 `python` 替换为 `python3`。

```sh
git clone https://github.com/kiritoko1029/agent-engineering-skills.git
cd agent-engineering-skills

# 查看将要安装的内容；默认不会写入任何文件
python scripts/install_skills.py --target ../my-project/.agents/skills --skill agent-change-journal --skill dsh-archive-agent-notes

# 确认目标正确后执行复制
python scripts/install_skills.py --target ../my-project/.agents/skills --skill agent-change-journal --skill dsh-archive-agent-notes --apply
```

`../my-project` 是示例路径，运行前替换成你的项目；含空格的路径加引号。PowerShell 可使用相同命令。目标应是技能集合目录，而不是某个具体技能目录。

安装全部技能：

```sh
python scripts/install_skills.py --target ../my-project/.agents/skills --all
python scripts/install_skills.py --target ../my-project/.agents/skills --all --apply
```

安装器复制整个技能目录，包含模板、`references/` 中的必要规范和许可证。**遇到同名目标会拒绝整次安装，不会覆盖现有技能。** 升级时先比较本地改动并保留副本，手动合并或改用新的目标目录；没有自动更新、卸载或远程发布功能。

`.agents/skills` 是本仓库采用的项目级示例路径。请按 Agent 宿主实际支持的技能搜索目录选择 `--target`；例如使用用户级 `~/.codex/skills` 时，这些技能会作用于该用户的多个项目。这里提供标准 `SKILL.md` 文件，不声称对所有宿主完成兼容测试。若宿主没有技能发现功能，直接让它读取目标 `SKILL.md`，并按需读取同目录引用的资源。

## 技能目录

| 技能 | 何时使用 | 主要结果 |
| --- | --- | --- |
| [agent-change-journal](skills/agent-change-journal/SKILL.md) | 当天总结、阶段结束、交接或恢复任务 | 实际改动、检查结果、限制与下一步 |
| [dsh-archive-agent-notes](skills/dsh-archive-agent-notes/SKILL.md) | 非平凡改动、新增 Note、审计、替代或归档决策记录 | 按上游规范记录决策、检查替代关系并维护生命周期 |
| [agent-code-review](skills/agent-code-review/SKILL.md) | 审查指定差异、模块或变更请求 | 有触发条件和证据的可执行问题 |
| [agent-simplify](skills/agent-simplify/SKILL.md) | 寻找可以删除或合并的复杂性 | 有实际消费者依据的简化建议或改动 |
| [agent-verify-change](skills/agent-verify-change/SKILL.md) | 验证修改、准备提交或交付 | 与变更面相符的检查及结果说明 |
| [agent-ci-reliability](skills/agent-ci-reliability/SKILL.md) | CI 偶发失败、超时、挂起或只在 CI 失败 | 复现条件、根因、修复和稳定性证据 |
| [agent-performance](skills/agent-performance/SKILL.md) | 性能退化调查或有明确目标的优化 | 可比较基线、瓶颈证据和正确性结果 |
| [agent-docs](skills/agent-docs/SKILL.md) | README、指南、接口文档或注释维护 | 有事实依据、职责明确的文档 |
| [agent-deliver-stack](skills/agent-deliver-stack/SKILL.md) | 同步或交付相互依赖的 PR、MR 或分支 | 依赖顺序、逐层验证和真实合入状态 |

这些技能可单独复制，互相没有强制加载依赖。支持 `$skill-name` 的宿主可以使用以下示例；其他宿主改成“读取对应 `SKILL.md` 并按其流程执行”。

```text
用 $agent-change-journal 总结本次修改，记录实际跑过的检查、未完成项和明天的接续入口。

用 $dsh-archive-agent-notes 及其随包规范记录为什么提议仅对幂等读取重试，并检查已有 Notes 的替代关系。未交付的方案使用 proposed，不补造测试结果。

用 $agent-code-review 审查当前工作区相对 main 的改动，重点检查取消和资源释放。

用 $agent-simplify 检查 src/cache 中没有实际消费者的复杂性，先给出有证据的候选项。

用 $agent-verify-change 验证当前变更，按受影响行为选择检查并报告限制。
```

## 把工作记录接入项目

安装技能后，把 [AGENTS.md 片段](templates/AGENTS.fragment.md) 中适合项目的约定合入已有指令文件，**不要覆盖原文件**。Agent Notes 的触发、格式和生命周期沿用随包规范；日常日志可按项目需要启用。只复制技能不会自动产生日报，也不会创建定时任务。

Agent Notes 使用下列生命周期与分类结构；调整项目根路径时同步相关规范和链接。工作日志可以沿用项目已有目录。

```text
my-project/
├── AGENTS.md
└── .agents/
    ├── skills/                    # 安装后的技能
    ├── journal/
    │   └── YYYY-MM-DD.md           # 当天任务小节、验证、接续入口
    └── notes/
        ├── proposed/<category>/   # 未实施或部分实施的提议
        ├── implemented/<category>/# 已落地且仍有参考价值的决策
        ├── rejected/<category>/   # 保留拒绝原因
        └── archived/<category>/   # 永久冻结的历史快照，不代表当前行为
```

`<category>` 默认沿用上游六个分类：`architecture`、`feature`、`bug-fix`、`simplification`、`process`、`testing`。分类不是任意标签；变更分类集合必须同步规范及项目已有的分类检查。决策文件使用 `YYYY-MM-DD-topic.md`，日期保留首次提出时间。

| 资料 | 回答的问题 | 更新方式 |
| --- | --- | --- |
| 工作日志 | 做了什么、验证了什么、还差什么？ | 一天可有多个任务小节；保留其他工作者内容 |
| 活跃决策 | 为什么选这个方案，代价是什么？ | 同步仍有效的事实；改变决策则新建继任记录，检查替代关系并链接相关活跃记录 |
| 操作与接口文档 | 现在如何使用、有哪些保证？ | 随代码行为维护 |
| 归档决策 | 当时为何如此选择？ | 封存后永久冻结；禁止修改正文、修复出链、移动或删除，当前修正在新记录中说明 |

工作日志不抄对话，不把计划当成果，也不把“跳过检查”记成“检查通过”。**每次非平凡改动必须在同一变更中新增或更新至少一份 Agent Note**；只有纯机械或局部编辑，且不改变行为、契约、结构、流程或决策理由时才豁免。已有条目能够承载同一决策时更新它，不创建重复记录。每份新 Note 都要检查替代关系；符合条件的已实施记录在同一变更中归档，部分替代保留活跃记录并互相链接。

归档时只能按规范搬移完整记录及其配套文件、添加归档元数据并处理活跃文档的入链，不得修改 Note 正文或核验、修复其出链。封存后永久冻结，不再编辑、翻译、重新排版、移动或删除。

查看 [填写后的日志示例](examples/journal/2026-09-12.md) 和它引用的 [提议示例](examples/notes/proposed/architecture/2026-09-12-read-retries.md)。两者使用虚构项目，仅展示写法；尚未交付的方案保留为 `proposed`，其中命令和测试数字不是本仓库的验证报告。

## 推荐使用节奏

1. 开始或恢复任务时，查找最近相关日志及直接引用的决策，结合当前代码确认状态。
2. 开发中按需要调用技能；非平凡改动必须新增或更新 Agent Note，新增时检查替代关系。
3. 结束阶段时执行必要检查；启用工作日志的项目写简短日志，给出具体下一步。
4. 发现活跃决策过时或知识重复时维护它；归档依据未来价值，不按年龄或条数清理，已封存记录永久冻结。

无需一次加载全部技能；检查范围、附属文件及文档要求按所用技能和项目规范执行。多 Agent 工作时可以按独立模块委派，但先划清写入范围，最后由负责交付的 Agent 核实真实产物。

## 仓库结构

```text
.zcode-plugin/plugin.json      # ZCode 插件声明
marketplace.json               # 根目录 ZCode 插件目录
kimi.plugin.json               # Kimi Code 插件声明，复用现有 skills/
.codex-plugin/plugin.json      # Codex 插件声明与展示元数据
.agents/plugins/marketplace.json # 仓库级 Codex 插件目录
skills/<skill-name>/SKILL.md     # 可独立安装的入口
skills/<skill-name>/assets/     # 仅在有需要时提供的模板
skills/<skill-name>/references/ # 随包保留的必要规范，单独安装后仍可读取
skills/<skill-name>/LICENSE     # 单独复制技能时保留的许可
templates/AGENTS.fragment.md    # 合入目标项目的工作约定
examples/                      # 已填示例，明确区分虚构与真实证据
docs/upstream.md                # 固定版本来源与通用化说明
scripts/install_skills.py       # 显式选择技能，默认预览，拒绝覆盖
scripts/validate_repo.py        # 格式与相对文件链接校验
tests/test_tools.py             # 工具行为测试
.github/workflows/validate.yml  # GitHub 上可运行的校验工作流
```

## 校验与贡献

```sh
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

校验器检查本仓库的 Codex、ZCode 与 Kimi Code 单插件布局、适用的 marketplace 标识及版本同步、技能发现路径，以及本仓库约定的 `name`、`description` 单行 frontmatter、技能目录命名和 Markdown 相对文件链接。它不是完整的宿主插件 schema 或 YAML / Markdown 解析器，不验证网页可访问性或页面锚点，也不能证明技能在真实任务中的决策质量。

初始版本的实际验证结果与平台限制见 [验证记录](docs/validation.md)。

新增技能时，先说明它解决的具体任务，再决定是否需要模板、参考资料或脚本。保持入口简短、触发准确、资源在单独安装后仍可访问；不要把一次项目事故变成所有任务的强制规则。脚本改动应验证实际行为；复杂工作流可用隔离示例进行独立试用。

本仓库的 GitHub Actions 配置运行上述检查；实际云端结果以推送后的运行记录为准。下载版可在自己的目录初始化 Git 并提交，再按需要添加远程仓库。

## 来源与许可

分析快照为 DeepSeek Harness 提交 [`c291e7961a515f6d7af9304e7fd1d257929aef26`](https://github.com/deepseek-ai/deepseek-harness/tree/c291e7961a515f6d7af9304e7fd1d257929aef26)，整理日期为 2026-09-12。逐项来源、保留的方法、删去的专属约束和新增内容见 [来源说明](docs/upstream.md)。本项目不是 DeepSeek 官方发行物。

采用 [MIT 许可证](LICENSE)，保留 DeepSeek 的版权与许可声明；另见 [NOTICE](NOTICE.md)。单独分发技能时，请同时保留该技能目录下的 `LICENSE`。
