"""Fast checks that need no Telegram account or external service."""
import ast
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SourceSanityTests(unittest.TestCase):
    def test_all_python_sources_parse(self):
        sources = [
            path
            for path in ROOT.rglob("*.py")
            if ".venv" not in path.parts and "__pycache__" not in path.parts
        ]
        self.assertGreater(len(sources), 0)
        for path in sources:
            with self.subTest(path=path.relative_to(ROOT)):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_configuration_has_environment_fallback(self):
        selector = (ROOT / "Eivabot/config/vars.py").read_text(encoding="utf-8")
        self.assertIn("from .Config import Config", selector)
        self.assertIn("from Eiva_config import Config", selector)

    def test_importing_package_does_not_connect(self):
        package = (ROOT / "Eivabot/__init__.py").read_text(encoding="utf-8")
        self.assertNotIn(".start(bot_token=", package)
        self.assertNotIn(".start()", package)

    def test_startup_checks_credentials_before_start(self):
        source = (ROOT / "Eivabot/__main__.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        calls = []
        for node in ast.walk(main):
            if not isinstance(node, ast.Call):
                continue
            called = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if called in {"validate_config", "start"}:
                calls.append((node.lineno, called))
        line_by_name = {name: min(line for line, value in calls if value == name)
                        for name in ("validate_config", "start")}
        self.assertLess(line_by_name["validate_config"], line_by_name["start"])

    def test_safe_calculator_accepts_math_and_rejects_code(self):
        module_path = ROOT / "Eivabot/utils/safe_math.py"
        spec = importlib.util.spec_from_file_location("safe_math_under_test", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.evaluate("(2 + 3) * 4"), 20)
        with self.assertRaises(ValueError):
            module.evaluate("__import__('os').system('whoami')")


if __name__ == "__main__":
    unittest.main()
