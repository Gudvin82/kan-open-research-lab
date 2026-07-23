import json
import tomllib
from pathlib import Path


def test_vercel_configuration_is_scoped_and_migration_free():
    config = json.loads(Path("vercel.json").read_text())
    assert config["$schema"] == "https://openapi.vercel.sh/vercel.json"
    assert config["framework"] is None
    assert config["outputDirectory"] == "public"
    assert "collectstatic" in config["buildCommand"]
    assert list(config["functions"]) == ["api/index.py"]
    assert config["functions"]["api/index.py"]["maxDuration"] == 30
    assert config["rewrites"] == [{"source": "/(.*)", "destination": "/api/index"}]

    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    vercel = pyproject["tool"]["vercel"]
    assert vercel["entrypoint"] == "api.index:app"

    build_commands = json.dumps({"vercel.json": config, "tool.vercel": vercel}).lower()
    assert "migrate" not in build_commands
    assert "deploy" not in build_commands


def test_vercel_bundle_excludes_development_and_worker_surfaces():
    ignored = {
        line.strip()
        for line in Path(".vercelignore").read_text().splitlines()
        if line.strip()
    }
    assert {
        "node_modules",
        "package.json",
        "package-lock.json",
        "playwright.config.ts",
        "tests",
        "research_engine",
        "artifacts",
        ".agents",
        ".github",
        ".specify",
        ".env*",
        "AGENTS.md",
        "Dockerfile",
        "compose*.yaml",
        "scripts",
        "staticfiles",
        "/public",
        "tmp",
    } <= ignored

    dockerfile = Path("Dockerfile").read_text()
    assert "npm" not in dockerfile
    assert "node" not in dockerfile
    assert "playwright" not in dockerfile.lower()


def test_vercel_configuration_contains_no_database_or_worker_secret():
    inspected = "\n".join(
        [
            Path("vercel.json").read_text(),
            Path("pyproject.toml").read_text(),
            Path(".vercelignore").read_text(),
        ]
    ).lower()
    assert "database_url=" not in inspected
    assert "postgresql://" not in inspected
    assert "kan_worker" not in inspected
    assert "research_engine/src" not in inspected
