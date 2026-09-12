"""Behavior tests using isolated repositories; no installed user skills are touched."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "scripts"


class RepositoryToolsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="agent-skills-tests-", dir=os.environ.get("AGENT_SKILLS_TEST_TMP")
        )
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / "repository"
        (self.repo / "scripts").mkdir(parents=True)
        for name in ("install_skills.py", "validate_repo.py"):
            shutil.copy2(TOOLS / name, self.repo / "scripts" / name)
        self.create_skill("alpha")
        (self.repo / "README.md").write_text("# Example repository\n", encoding="utf-8")
        self.target = self.workspace / "new-project" / ".agents" / "skills"

    def create_skill(self, name: str) -> Path:
        folder = self.repo / "skills" / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: A reusable skill for testing.\n---\n\n# Skill\n",
            encoding="utf-8",
        )
        return folder

    def run_tool(self, name: str, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts" / name), *arguments],
            cwd=cwd or self.workspace,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        return result

    def install(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return self.run_tool("install_skills.py", "--target", str(self.target), *arguments)

    def validate(self) -> subprocess.CompletedProcess[str]:
        return self.run_tool("validate_repo.py")

    def assert_success(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def symlink_or_skip(self, link: Path, destination: Path, *, directory: bool = False) -> None:
        try:
            link.symlink_to(destination, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"creating symbolic links is unavailable on this host: {exc}")

    def test_dry_run_prints_plan_without_creating_target_or_parents(self) -> None:
        before = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        result = self.install("--skill", "alpha")
        self.assert_success(result)
        self.assertIn("DRY RUN", result.stdout)
        self.assertIn(str(self.target / "alpha"), result.stdout)
        self.assertFalse((self.workspace / "new-project").exists())
        after = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        self.assertEqual(after, before)

    def test_apply_copies_complete_skill_with_resolvable_resource_link(self) -> None:
        source = self.repo / "skills" / "alpha"
        resource = source / "references" / "nested" / "guide.md"
        resource.parent.mkdir(parents=True)
        resource.write_text("# Resource\n你好\n", encoding="utf-8")
        binary = source / "asset.bin"
        binary.write_bytes(bytes(range(256)))
        with (source / "SKILL.md").open("a", encoding="utf-8") as handle:
            handle.write("[Guide](references/nested/guide.md)\n")
        self.assert_success(self.install("--skill", "alpha", "--apply"))
        installed = self.target / "alpha"
        self.assertEqual((installed / "SKILL.md").read_bytes(), (source / "SKILL.md").read_bytes())
        self.assertEqual((installed / "references/nested/guide.md").read_bytes(), resource.read_bytes())
        self.assertEqual((installed / "asset.bin").read_bytes(), binary.read_bytes())
        self.assertEqual(sorted(path.name for path in self.target.iterdir()), ["alpha"])

    def test_all_installs_every_skill_and_duplicate_selection_is_idempotent(self) -> None:
        self.create_skill("beta")
        self.assert_success(self.install("--all", "--apply"))
        self.assertEqual(sorted(path.name for path in self.target.iterdir()), ["alpha", "beta"])
        second_target = self.workspace / "second"
        result = self.run_tool(
            "install_skills.py", "--target", str(second_target),
            "--skill", "alpha", "--skill", "alpha", "--apply",
        )
        self.assert_success(result)
        self.assertEqual([path.name for path in second_target.iterdir()], ["alpha"])

    def test_conflict_refuses_whole_batch_and_preserves_original(self) -> None:
        self.create_skill("beta")
        existing = self.target / "beta"
        existing.mkdir(parents=True)
        sentinel = existing / "keep.txt"
        sentinel.write_bytes(b"existing user content\x00")
        before = sentinel.read_bytes()
        result = self.install("--skill", "alpha", "--skill", "beta", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflict", result.stdout)
        self.assertEqual(sentinel.read_bytes(), before)
        self.assertFalse((self.target / "alpha").exists())
        self.assertEqual([path.name for path in self.target.iterdir()], ["beta"])

    def test_invalid_and_missing_skill_names_never_create_target(self) -> None:
        for name in ("../alpha", "..\\alpha", "Alpha", "a_b", "a" * 64, "missing"):
            with self.subTest(name=name):
                self.assertNotEqual(self.install("--skill", name, "--apply").returncode, 0)
                self.assertFalse(self.target.exists())

    def test_selection_is_required_and_all_cannot_be_mixed_with_skill(self) -> None:
        self.assertNotEqual(self.install().returncode, 0)
        self.assertNotEqual(self.install("--all", "--skill", "alpha").returncode, 0)
        self.assertFalse(self.target.exists())

    def test_existing_file_target_is_rejected(self) -> None:
        target_file = self.workspace / "target.txt"
        target_file.write_text("preserve", encoding="utf-8")
        result = self.run_tool("install_skills.py", "--target", str(target_file), "--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target_file.read_text(encoding="utf-8"), "preserve")

    def test_normal_parent_relative_target_installs_into_sibling_project(self) -> None:
        result = self.run_tool(
            "install_skills.py", "--target", "../my-project/.agents/skills",
            "--skill", "alpha", "--apply", cwd=self.repo,
        )
        self.assert_success(result)
        installed = self.workspace / "my-project/.agents/skills/alpha/SKILL.md"
        self.assertEqual(installed.read_bytes(), (self.repo / "skills/alpha/SKILL.md").read_bytes())

    def test_link_followed_by_parent_segment_is_rejected_before_normalizing(self) -> None:
        outside = self.workspace / "outside" / "nested"
        outside.mkdir(parents=True)
        link = self.workspace / "directory-link"
        self.symlink_or_skip(link, outside, directory=True)
        result = self.run_tool(
            "install_skills.py", "--target", str(link / ".." / "escaped-target"), "--all", "--apply",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic links", result.stdout)
        self.assertFalse((self.workspace / "escaped-target").exists())
        self.assertFalse((outside.parent / "escaped-target").exists())

    def test_destination_inside_source_is_rejected(self) -> None:
        target = self.repo / "skills/alpha/nested-install"
        result = self.run_tool("install_skills.py", "--target", str(target), "--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(target.exists())

    def test_linked_source_resource_is_rejected(self) -> None:
        outside = self.workspace / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        self.symlink_or_skip(self.repo / "skills/alpha/linked.md", outside)
        result = self.install("--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.target.exists())

    def test_linked_source_skill_is_rejected(self) -> None:
        self.symlink_or_skip(self.repo / "skills/beta", self.repo / "skills/alpha", directory=True)
        result = self.install("--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.target.exists())

    def test_linked_destination_parent_is_rejected_without_writing_through_it(self) -> None:
        outside = self.workspace / "outside"
        outside.mkdir()
        self.symlink_or_skip(self.workspace / "new-project", outside, directory=True)
        result = self.install("--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_broken_destination_symlink_is_a_conflict(self) -> None:
        self.target.mkdir(parents=True)
        self.symlink_or_skip(self.target / "alpha", self.workspace / "missing", directory=True)
        result = self.install("--all", "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.target / "alpha").is_symlink())

    def test_valid_relative_links_references_anchors_and_external_links(self) -> None:
        docs = self.repo / "docs"
        docs.mkdir()
        (docs / "with space.md").write_text("# Heading\n", encoding="utf-8")
        (self.repo / "README.md").write_text(
            "[Skill](skills/alpha/SKILL.md#heading)\n"
            "[Spaced](<docs/with space.md#heading>)\n"
            "[Encoded](docs/with%20space.md)\n"
            "[Local heading](#anything)\n"
            "[External](https://example.invalid/no-network-check)\n"
            "[Email](mailto:example@example.invalid)\n"
            "[Reference][guide]\n\n[guide]: skills/alpha/SKILL.md\n"
            "Use `scripts/validate_repo.py`.\n"
            "Template: <项目名>. The word TODO can be discussed.\n"
            "```markdown\n[Example only](missing-example.md)\n```\n",
            encoding="utf-8",
        )
        self.assert_success(self.validate())

    def test_broken_inline_reference_image_and_script_links_fail(self) -> None:
        for markdown in (
            "[Missing](missing.md)", "![Image](missing.png)",
            "[Reference][missing]\n\n[missing]: missing.md", "Run `scripts/missing.py`.",
        ):
            with self.subTest(markdown=markdown):
                (self.repo / "README.md").write_text(markdown, encoding="utf-8")
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("broken local link", result.stdout)

    def test_local_link_escaping_repository_fails_even_when_file_exists(self) -> None:
        (self.workspace / "outside.md").write_text("exists", encoding="utf-8")
        for link in ("../outside.md", "%2e%2e/outside.md"):
            with self.subTest(link=link):
                (self.repo / "README.md").write_text(f"[Outside]({link})", encoding="utf-8")
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("escapes repository", result.stdout)

    def test_frontmatter_errors_and_missing_skill_entry_fail(self) -> None:
        entry = self.repo / "skills/alpha/SKILL.md"
        invalid = (
            "# Missing metadata\n",
            "---\nname: alpha\ndescription: missing delimiter\n",
            "---\nname: other\ndescription: Good.\n---\n",
            "---\nname: alpha\ndescription: \n---\n",
            "---\nname: alpha\n---\n",
            "---\nname: alpha\ndescription: |\n  Multiline\n---\n",
            "---\nname: alpha\nname: alpha\ndescription: Good.\n---\n",
            '---\nname: alpha\ndescription: ""\n---\n',
        )
        for content in invalid:
            with self.subTest(content=content):
                entry.write_text(content, encoding="utf-8")
                self.assertNotEqual(self.validate().returncode, 0)
        entry.unlink()
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing SKILL.md", result.stdout)

    def test_double_quoted_frontmatter_is_supported(self) -> None:
        (self.repo / "skills/alpha/SKILL.md").write_text(
            '---\nname: "alpha"\ndescription: "Use this: it has a colon and # symbol."\n---\n# Body\n',
            encoding="utf-8",
        )
        self.assert_success(self.validate())

    def test_explicit_generation_markers_fail_but_general_placeholders_pass(self) -> None:
        for marker in ("{{TODO}}", "<TODO: fill this>", "<!-- TODO: replace -->"):
            with self.subTest(marker=marker):
                (self.repo / "README.md").write_text(marker, encoding="utf-8")
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unresolved generated TODO", result.stdout)
        (self.repo / "README.md").write_text("Template: <日期> / <项目名>.\nTODO is a word.", encoding="utf-8")
        self.assert_success(self.validate())


if __name__ == "__main__":
    unittest.main()
