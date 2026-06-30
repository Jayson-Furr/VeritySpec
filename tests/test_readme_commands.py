from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

SKIPPED_PREFIXES = (
    ". ",
    "pip install",
    "python -m pip",
    "python3 -m venv",
    "PYTHONPATH=src python3 -m unittest",
)


def read_readme_bash_commands() -> list[str]:
    commands: list[str] = []
    in_bash_block = False

    for line in README.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "```bash":
            in_bash_block = True
            continue
        if in_bash_block and stripped == "```":
            in_bash_block = False
            continue
        if not in_bash_block or not stripped or stripped.startswith("#"):
            continue
        commands.append(stripped)

    return commands


def is_skipped_command(command: str) -> bool:
    return command.startswith(SKIPPED_PREFIXES)


def command_to_args(command: str, tmp_root: Path) -> tuple[list[str], dict[str, str]]:
    args = shlex.split(command)
    env_overrides: dict[str, str] = {}
    while args and "=" in args[0] and not args[0].startswith("-"):
        key, value = args.pop(0).split("=", 1)
        if key == "PYTHONPATH" and value == "src":
            value = str(ROOT / "src")
        env_overrides[key] = value

    if not args:
        raise ValueError(f"README command has no executable: {command}")

    if args[0] == "verity":
        verity_executable = shutil.which("verity")
        if verity_executable:
            args[0] = verity_executable
        else:
            args = [sys.executable, "-m", "verityspec", *args[1:]]
            env_overrides["PYTHONPATH"] = str(ROOT / "src")
    elif args[0] == "python3":
        args[0] = sys.executable

    rewritten: list[str] = []
    for arg in args:
        if arg == "build":
            rewritten.append(str(tmp_root / "build"))
        elif arg.startswith("build/"):
            rewritten.append(str(tmp_root / arg))
        else:
            rewritten.append(arg)

    return rewritten, env_overrides


class ReadmeCommandSmokeTests(unittest.TestCase):
    def test_safe_readme_bash_commands_execute(self) -> None:
        commands = read_readme_bash_commands()
        self.assertGreater(len(commands), 0, "README should contain bash command examples")

        runnable = [command for command in commands if not is_skipped_command(command)]
        skipped = [command for command in commands if is_skipped_command(command)]
        self.assertGreater(len(runnable), 0, "README should contain runnable CLI command examples")
        self.assertGreater(len(skipped), 0, "README install/setup examples should be explicit skips")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            for command in runnable:
                with self.subTest(command=command):
                    args, env_overrides = command_to_args(command, tmp_root)
                    env = os.environ.copy()
                    env.update(env_overrides)
                    result = subprocess.run(
                        args,
                        cwd=ROOT,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )

                    self.assertEqual(
                        0,
                        result.returncode,
                        "\n".join(
                            [
                                f"README command failed: {command}",
                                f"Executed as: {shlex.join(args)}",
                                f"stdout:\n{result.stdout}",
                                f"stderr:\n{result.stderr}",
                            ]
                        ),
                    )

    def test_readme_bash_commands_are_classified(self) -> None:
        commands = read_readme_bash_commands()
        for command in commands:
            executable = shlex.split(command)[0]
            self.assertTrue(
                command.startswith(("verity ", "PYTHONPATH=src python3 -m verityspec"))
                or is_skipped_command(command),
                f"README command must be runnable or intentionally skipped: {command}",
            )
            if not is_skipped_command(command):
                self.assertIn(executable, {"verity", "PYTHONPATH=src"})


if __name__ == "__main__":
    unittest.main()
