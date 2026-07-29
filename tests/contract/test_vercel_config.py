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


def test_production_runtime_contract_is_host_exact_and_indexing_disabled():
    production = Path("src/config/settings/production.py").read_text()
    public_urls = Path("src/config/public_urls.py").read_text()
    middleware = Path("src/webapp/middleware.py").read_text()

    assert "VERCEL_URL" in production
    assert "VERCEL_PROJECT_PRODUCTION_URL" in production
    assert "PUBLIC_BASE_URL" in production
    assert "PUBLIC_INDEXING_ENABLED = False" in production
    assert 'required("DJANGO_ALLOWED_HOSTS")' not in production
    assert "exact hostname required" in public_urls
    assert 'response.headers["X-Robots-Tag"] = "noindex, nofollow"' in middleware

    runtime_contract = "\n".join((production, public_urls, middleware))
    assert "migrate" not in runtime_contract.lower()
    assert "kan_worker" not in runtime_contract


def test_vercel_runtime_does_not_require_build_only_static_manifest():
    production = Path("src/config/settings/production.py").read_text()
    build = Path("src/config/settings/build.py").read_text()

    assert "django.contrib.staticfiles.storage.StaticFilesStorage" in production
    assert "whitenoise.middleware.WhiteNoiseMiddleware" in production
    assert "public" in build
    assert "static" in build
