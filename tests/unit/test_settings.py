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


def test_preview_is_noindex_and_uses_security_headers_without_database():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.preview",
            "DJANGO_SECRET_KEY": (
                "preview-test-robots-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"
            ),
            "VERCEL_ENV": "preview",
        }
    )
    env.pop("DATABASE_URL", None)
    env.pop("DATABASE_ENV", None)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-c",
            (
                "import django, tempfile; django.setup(); "
                "from django.conf import settings; "
                "settings.STATIC_ROOT=tempfile.mkdtemp(); "
                "from django.core.management import call_command; "
                "call_command('collectstatic', verbosity=0, interactive=False); "
                "from django.test import Client; c=Client(); "
                "r=c.get('/ru/', HTTP_HOST='preview.vercel.app', "
                "HTTP_X_FORWARDED_PROTO='https'); "
                "assert r.status_code == 200; "
                'assert b\'<meta name="robots" content="noindex, nofollow">\' '
                "in r.content; "
                "assert r.headers['X-Robots-Tag'] == 'noindex, nofollow'; "
                "assert r.headers['X-Frame-Options'] == 'DENY'; "
                "assert r.headers['X-Content-Type-Options'] == 'nosniff'; "
                "assert r.headers['Referrer-Policy'] == "
                "'strict-origin-when-cross-origin'"
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


def test_production_without_database_serves_public_shell():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.production",
            "DJANGO_SECRET_KEY": ("production-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
            "DJANGO_ALLOWED_HOSTS": "production.invalid",
        }
    )
    env.pop("DATABASE_URL", None)
    env.pop("DATABASE_ENV", None)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-c",
            (
                "import django, tempfile; django.setup(); "
                "from django.conf import settings; "
                "settings.STATIC_ROOT=tempfile.mkdtemp(); "
                "from django.core.management import call_command; "
                "call_command('collectstatic', verbosity=0, interactive=False); "
                "from django.test import Client; c=Client(); "
                "r=c.get('/ru/', HTTP_HOST='production.invalid', secure=True); "
                "assert r.status_code == 200; "
                "assert b'compute_node_unavailable' in r.content"
            ),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
