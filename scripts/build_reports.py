"""Build self-contained Markdown reports with complete relevant source listings."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]


def main():
    common = ["app/__init__.py", "app/calculator.py", "run.py", "app/static/style.css", "app/static/app.js", "requirements.txt", "requirements-dev.txt"] + [str(path.relative_to(ROOT)).replace("\\", "/") for path in sorted((ROOT / "app/templates").glob("*.html"))]
    sources = {
        "01": common + ["app/templates/calculator.html"],
        "02": common + ["app/templates/todo.html", "tests/ui/test_calculator_todo.py"],
        "03": common + ["app/templates/login.html", "app/templates/account.html", "scripts/browser.py", "scripts/browser_smoke.py", "tests/conftest.py", "tests/ui/pages/base_page.py", "tests/ui/pages/login_page.py", "tests/ui/test_forms.py", "tests/ui/pages/contact_page.py"],
        "04": common + ["app/templates/contact.html", "tests/conftest.py", "scripts/browser.py", "tests/ui/pages/base_page.py", "tests/ui/pages/contact_page.py", "tests/ui/pages/login_page.py", "tests/ui/test_forms.py", "tests/unit/test_web.py"],
        "05": ["tests/api/test_public_api.py", "postman/lab05.collection.json", "postman/lab05.environment.json", "requirements-dev.txt", "requirements.txt", "tests/conftest.py"],
        "06": common + ["tests/unit/test_calculator.py", "tests/unit/test_web.py", "tests/conftest.py"],
        "08": common + ["load/k6/health.js", "scripts/summarize_load.py"],
        "09": [".github/workflows/run-tests.yml", "requirements.txt", "requirements-dev.txt", "pytest.ini", "tests/conftest.py", "scripts/browser.py", "tests/unit/test_calculator.py"],
    }
    target = ROOT / "reports"
    target.mkdir(exist_ok=True)
    manifest = []
    for number, files in sources.items():
        report = (ROOT / f"docs/lab{number}/report.md").read_text(encoding="utf-8")
        report += "\n\n## Общий статус выполнения на момент сборки\n\n" + (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
        if number == "08" and (ROOT / "artifacts/lab08/analysis.md").exists():
            report += "\n\n" + (ROOT / "artifacts/lab08/analysis.md").read_text(encoding="utf-8")
        report += "\n\n## Приложение. Листинги исходного кода\n"
        for name in dict.fromkeys(files):
            source = (ROOT / name).read_text(encoding="utf-8")
            language = {".py": "python", ".js": "javascript", ".json": "json", ".html": "html", ".css": "css", ".yml": "yaml"}.get(Path(name).suffix, "text")
            digest = hashlib.sha256(source.encode()).hexdigest()
            report += f"\n### {name}\n\nSHA-256: `{digest}`\n\n```{language}\n{source}\n```\n"
            manifest.append(f"{digest}  {name}")
        (target / f"lab{number}.md").write_text(report, encoding="utf-8")
    (target / "source-manifest.txt").write_text("\n".join(sorted(set(manifest))) + "\n", encoding="utf-8")
    print("Created 8 Markdown reports in reports/ (lab07 is outside this stage).")


if __name__ == "__main__":
    main()
