# 维护本技能仓库

本仓库保存通用开发技能，不包含 DeepSeek Harness 的运行时实现。Agent Notes 保留上游同名 `dsh-archive-agent-notes` 技能及其必要规范；维护 Notes 时遵守随包 `references/`。其他技能保留通用化整理，工作日志是独立的可选补充。

- 修改技能时先读目标 `SKILL.md` 和被引用的资源；优先修正影响判断的内容，不增加泛化的仪式和重复检查。
- 每个技能独立可安装。资源和必要规范放在自己的目录；入口使用单行 `name` 和 `description` frontmatter，目录名与 `name` 一致。
- 新增技能或改变范围时同步 README 技能目录及 `docs/upstream.md` 中的归因说明。保留根许可证和每个技能的许可证。
- 适配已有技能时优先保留上游名称、结构和核心规则，只调整独立使用所必需的项目依赖；在 `docs/upstream.md` 说明实际差异，不另行拆分或放宽原规则。
- 仓库说明使用中文；Notes 技能与规范为减少改写保留英文原文。命令、路径与代码标识保持准确。示例明确区分虚构设定与真实执行结果；未交付方案使用 `proposed`。
- 验证结构：`python scripts/validate_repo.py`。修改工具时运行 `python -m unittest discover -s tests -v`，必要时在临时目录试用。
- 不手动发布远程仓库或覆盖用户技能；脚本默认预览，只有显式 `--apply` 才安装。
