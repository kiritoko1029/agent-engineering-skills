# 初始版本验证记录

日期：2026-09-12。执行环境：Windows，Python 3.14.2。此记录描述初始提交 `a03a445` 的本地结果，包含后来被上游技能替换的两个 Notes 入口；不是当前版本的技能数量或验证声明。后续修改需按影响重新验证，最新云端结果见 [GitHub Actions](https://github.com/kiritoko1029/agent-engineering-skills/actions)。

| 检查 | 结果 | 范围与限制 |
| --- | --- | --- |
| skill-creator 官方 `quick_validate.py` | 10 个技能全部通过 | frontmatter、命名与未完成脚手架检查；不证明工作流行为正确 |
| `python scripts/validate_repo.py` | 通过 | 本仓库技能格式与 Markdown 相对文件链接；不联网查链接或验证锚点 |
| `python -m unittest discover -s tests -v` | 20 项中 15 通过，5 跳过，无失败 | Windows 当前账户没有创建符号链接的权限，相关 5 项跳过；不能据此声称符号链接防护已实测通过 |
| 实际安装预览与 `--all --apply` | 10 个技能安装成功 | 目标为隔离工作目录；安装后校验相对模板链接通过 |
| 来源路径核对 | 24 个固定提交文件存在 | 检查本地上游快照中的对应文件；不是对未来上游状态的保证 |

工具测试覆盖完整资源复制、预览无改动、同名冲突整批拒绝且保留原文件、无效技能名、正常父目录相对路径安装，以及格式错误和断链拒绝等行为。源码内包含符号链接相关测试，但本机因权限跳过，需在支持环境执行。

官方校验器所需 PyYAML 6.0.3 仅安装在分析用的临时目录。分发仓库的安装器与校验器没有该依赖，不会自行下载软件。

## 独立工作流试用

另一个 Agent 使用日志与决策两个技能处理隔离的缓存项目。输入为该项目的 README、源码和测试；任务只要求交接记录与设计取舍，没有授权修改产品代码。

实际测试共 3 项，2 失败、1 通过：缓存 `None` 意外调用取数函数，缓存 `0` 被取数结果替代。Agent 将原开发目标记为未完成，保留失败证据，将尚未落实的方案写为 `proposed`，没有把记录整理完成当作功能完成，没有改动源码或补造 Git 提交依据。

根据这次试用，日志技能明确区分“开发目标状态”与“记录任务状态”。该试用仅覆盖这两个技能的一种场景，不等同于所有技能在所有 Agent 宿主上的完整验证。

初始提交随后通过了 [GitHub Actions](https://github.com/kiritoko1029/agent-engineering-skills/actions/runs/34678507282)。测试文件本身是可重复执行的验证入口。

## Agent Notes 最小适配验证

2026-09-12，用上游同名 `dsh-archive-agent-notes` 及三个随包规范替换初版两个 Notes 入口后，9 个技能通过官方格式校验，仓库相对链接和 `git diff --check` 通过。新 Notes 技能在隔离目录实际安装成功，安装后的规范引用检查通过。

独立审阅对照固定版本的上游四份文件，确认非平凡改动必须记录、已交付状态、替代与清理条件、归档正文及出链不修复、永久冻结等核心语义保留。本次没有修改安装器、校验器或测试代码，没有为文档变更重复运行本地工具测试；云端检查以对应提交的 GitHub Actions 结果为准。

## Codex 插件适配验证

2026-09-14，macOS，`codex-cli 0.154.0`：

- plugin-creator 随附的 `validate_plugin.py` 校验通过；其 PyYAML 依赖仅安装在临时虚拟环境，仓库工具仍只用标准库。
- 使用隔离的 Codex 配置目录执行 `codex plugin marketplace add <本仓库绝对路径> --json` 和 `codex plugin add agent-engineering-skills@agent-engineering-skills --json`，两步退出码均为 0，安装版本为 `1.0.0`。未写入日常 Codex 配置或覆盖用户技能。
- 安装缓存包含全部 9 个技能；`skills/` 下的 23 个文件逐项 SHA-256 与源码一致，包括模板、参考规范和许可证。
- `python3 scripts/validate_repo.py` 通过；`python3 -m unittest discover -s tests -v` 的 22 项测试全部通过，无跳过；`git diff --check` 通过。
- 首次工具测试中 5 项受 macOS `/var` 临时路径符号链接影响。测试夹具改为解析临时根目录的真实路径后通过；安装器对用户指定符号链接路径的拒绝规则未放宽，相关测试仍通过。

本次实测覆盖本地 marketplace 发现、插件安装和资源完整性，未测试桌面端点击安装及新任务中的技能执行。GitHub 远程安装需先提交并推送适配文件；本次未发布远程仓库。

## ZCode 插件适配验证

2026-09-15，macOS，Python 3.14.7，静态验证：

- `python3 scripts/validate_repo.py` 通过，包含新增的 ZCode 清单与 marketplace 结构、技能路径及版本同步校验。
- `python3 -m unittest discover -s tests -v` 的 22 项测试全部通过，无跳过；夹具已同步复制 `.zcode-plugin/plugin.json` 与 `marketplace.json`，并覆盖清单字段错误、marketplace 来源指向缺失目录、名称不符与版本不同步的拒绝行为。
- 本机没有可独立调用的 `zcode` 命令行，未实际执行桌面端的市场添加、插件安装、启用与技能触发；需按 README 步骤在客户端验证。GitHub 远程安装需先提交并推送适配文件，本次未发布远程仓库。

## Kimi Code 插件适配验证

2026-09-17，Windows，Kimi Code 0.42.0，Python 3.14.2：

- 使用独立的 `KIMI_CODE_HOME` 启动本机 `kimi web --host 127.0.0.1 --port 0 --no-open`，保留令牌鉴权。通过官方服务 API 从本地仓库安装，再读取安装列表；仅写入任务临时目录，没有修改日常 Kimi 配置。
- 运行时返回插件 `agent-engineering-skills` 版本 `1.0.0`、`state: ok`、`enabled: true`、`skillCount: 9`、`hasErrors: false`。托管副本中 `skills/` 的 23 个文件逐项 SHA-256 与源码一致，包括模板、参考规范及许可证。验证后测试服务已退出。
- `python scripts/validate_repo.py` 通过；工具测试 23 项中 18 项通过、5 项因 Windows 创建符号链接权限不足跳过，无测试失败。新增检查覆盖 Kimi 清单缺失或损坏、错误名称或技能路径，以及意外启用启动注入或服务的拒绝行为。

首次实测安装成功，但测试脚本退出时发送了缺少 JSON 请求体的关闭请求；修正测试脚本后重跑，安装、文件核对和服务关闭均完成。该脚本只用于本地验证，不随插件分发。

此验证覆盖真实运行时的本地安装、启用、技能发现及资源完整性，没有发起模型调用或验证技能执行效果，也不等同于逐项测试桌面端交互。Kimi 协议依据 [官方插件文档](https://www.kimi.com/code/docs/kimi-code-cli/customization/plugins) 与 [服务 API](https://www.kimi.com/code/docs/kimi-code-cli/reference/server-api.html)。远程检查以对应提交的 GitHub Actions 结果为准。
