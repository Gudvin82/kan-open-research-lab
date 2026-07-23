import json
import tomllib
from pathlib import Path


def test_vercel_configuration_is_scoped_and_migration_free():
    config = json.loads(Path("vercel.json").read_text())
    assert config["$schema"] == "https://openapi.vercel.sh/vercel.json"
    assert config["framework"] is None
    function = config["functions"]["src/config/asgi.py"]
    assert 1 <= function["maxDuration"] <= 1800
    assert set(function) <= {"maxDuration", "excludeFiles", "includeFiles"}

    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    vercel = pyproject["tool"]["vercel"]
    assert vercel["entrypoint"] == "src.config.asgi:application"

    build_commands = json.dumps({"vercel.json": config, "tool.vercel": vercel}).lower()
    assert "migrate" not in build_commands
    assert "deploy" not in build_commands
