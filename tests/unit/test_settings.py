import os
import subprocess
import sys


def test_production_settings_fail_without_secrets():
    env = os.environ.copy()
    for name in ("DJANGO_SECRET_KEY", "DJANGO_ALLOWED_HOSTS", "DATABASE_URL"):
        env.pop(name, None)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-c",
            "import src.config.settings.production",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Required setting is missing" in result.stderr


def test_preview_without_database_keeps_liveness_only():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.preview",
            "DJANGO_SECRET_KEY": ("preview-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
        }
    )
    env.pop("DATABASE_URL", None)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-c",
            (
                "import django; django.setup(); "
                "from django.test import Client; c=Client(); "
                "assert c.get('/health/live/', "
                "HTTP_HOST='preview.vercel.app', secure=True).status_code == 200; "
                "assert c.get('/health/ready/', "
                "HTTP_HOST='preview.vercel.app', secure=True).status_code == 503"
            ),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_preview_rejects_non_preview_database_label():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.preview",
            "DJANGO_SECRET_KEY": ("preview-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
            "DATABASE_URL": "postgresql://preview:example@db/preview",
            "DATABASE_ENV": "production",
        }
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", "import src.config.settings.preview"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "DATABASE_ENV=preview" in result.stderr


def test_production_rejects_non_production_database_label():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.production",
            "DJANGO_SECRET_KEY": ("production-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
            "DJANGO_ALLOWED_HOSTS": "production.invalid",
            "DATABASE_URL": "postgresql://production:example@db/production",
            "DATABASE_ENV": "preview",
        }
    )
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", "import src.config.settings.production"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "DATABASE_ENV=production" in result.stderr
