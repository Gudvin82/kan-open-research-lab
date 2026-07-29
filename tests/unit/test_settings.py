import os
import subprocess
import sys

PRODUCTION_ENV = {
    "DJANGO_SETTINGS_MODULE": "src.config.settings.production",
    "DJANGO_SECRET_KEY": ("production-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
    "VERCEL_ENV": "production",
    "VERCEL_URL": "kan-open-research-immutable-test.vercel.app",
    "VERCEL_PROJECT_PRODUCTION_URL": "kan-open-research-lab.vercel.app",
}


def run_python(
    source: str, environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(environment)
    for name in (
        "DATABASE_URL",
        "DATABASE_ENV",
        "DJANGO_ALLOWED_HOSTS",
        "PUBLIC_BASE_URL",
        "VERCEL_ENV",
        "VERCEL_URL",
        "VERCEL_PROJECT_PRODUCTION_URL",
    ):
        if name not in environment:
            env.pop(name, None)
    return subprocess.run(  # noqa: S603
        [sys.executable, "-c", source],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_production_settings_fail_without_secrets():
    env = os.environ.copy()
    for name in (
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DATABASE_URL",
        "PUBLIC_BASE_URL",
        "VERCEL_URL",
        "VERCEL_PROJECT_PRODUCTION_URL",
    ):
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


def test_production_uses_exact_vercel_hosts_without_legacy_allowlist():
    result = run_python(
        (
            "from src.config.settings import production as s; "
            "assert s.ALLOWED_HOSTS == ["
            "'kan-open-research-immutable-test.vercel.app', "
            "'kan-open-research-lab.vercel.app']; "
            "assert '*' not in s.ALLOWED_HOSTS; "
            "assert '.vercel.app' not in s.ALLOWED_HOSTS; "
            "assert s.PUBLIC_BASE_URL == "
            "'https://kan-open-research-lab.vercel.app'"
        ),
        PRODUCTION_ENV,
    )

    assert result.returncode == 0, result.stderr


def test_production_fails_closed_without_stable_or_immutable_host():
    result = run_python(
        "import src.config.settings.production",
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.production",
            "DJANGO_SECRET_KEY": PRODUCTION_ENV["DJANGO_SECRET_KEY"],
            "VERCEL_ENV": "production",
        },
    )

    assert result.returncode != 0
    assert "Production host configuration is missing" in result.stderr


def test_production_rejects_invalid_host_configuration():
    invalid_values = (
        "*",
        ".vercel.app",
        "https://user@example.com",
        "https://example.com?poison=1",
        "https://example.com#poison",
        "ftp://example.com",
        "bad_host.example",
        "https://example.com\n",
        r"https://example.com\@evil.example",
    )

    for value in invalid_values:
        environment = PRODUCTION_ENV | {"DJANGO_ALLOWED_HOSTS": value}
        result = run_python("import src.config.settings.production", environment)
        assert result.returncode != 0, value
        assert "Invalid production host" in result.stderr, value


def test_all_production_host_sources_are_strictly_validated():
    for source in (
        "VERCEL_URL",
        "VERCEL_PROJECT_PRODUCTION_URL",
        "PUBLIC_BASE_URL",
    ):
        result = run_python(
            "import src.config.settings.production",
            PRODUCTION_ENV | {source: "https://user@evil.example"},
        )
        assert result.returncode != 0, source
        assert "Invalid production host" in result.stderr, source


def test_public_base_url_takes_priority_and_is_reduced_to_https_origin():
    result = run_python(
        (
            "from src.config.settings import production as s; "
            "assert s.PUBLIC_BASE_URL == 'https://research.example'; "
            "assert 'research.example' in s.ALLOWED_HOSTS; "
            "assert 'kan-open-research-lab.vercel.app' in s.ALLOWED_HOSTS"
        ),
        PRODUCTION_ENV
        | {"PUBLIC_BASE_URL": "https://research.example:8443/project/path"},
    )

    assert result.returncode == 0, result.stderr


def test_production_strips_scheme_path_and_port_from_allowed_hosts():
    result = run_python(
        (
            "from src.config.settings import production as s; "
            "assert 'extra.example' in s.ALLOWED_HOSTS; "
            "assert all('://' not in host and '/' not in host and ':' not in host "
            "for host in s.ALLOWED_HOSTS)"
        ),
        PRODUCTION_ENV
        | {"DJANGO_ALLOWED_HOSTS": "https://extra.example:8443/some/path"},
    )

    assert result.returncode == 0, result.stderr


def test_production_rejects_unknown_request_host_and_emits_noindex():
    result = run_python(
        (
            "import django; django.setup(); "
            "from django.test import Client; c=Client(); "
            "import tempfile; "
            "from django.conf import settings; "
            "settings.STATIC_ROOT=tempfile.mkdtemp(); "
            "from django.core.management import call_command; "
            "call_command('collectstatic', verbosity=0, interactive=False); "
            "good=c.get('/ru/', "
            "HTTP_HOST='kan-open-research-immutable-test.vercel.app', "
            "HTTP_X_FORWARDED_PROTO='https'); "
            "assert good.status_code == 200; "
            'assert b\'<meta name="robots" content="noindex, nofollow">\' '
            "in good.content; "
            "assert good.headers['X-Robots-Tag'] == 'noindex, nofollow'; "
            "evil=c.get('/ru/', HTTP_HOST='evil.vercel.app', "
            "HTTP_X_FORWARDED_PROTO='https'); "
            "assert evil.status_code == 400"
        ),
        PRODUCTION_ENV,
    )

    assert result.returncode == 0, result.stderr


def test_preview_without_database_keeps_liveness_only():
    env = os.environ.copy()
    env.update(
        {
            "DJANGO_SETTINGS_MODULE": "src.config.settings.preview",
            "DJANGO_SECRET_KEY": ("preview-test-7f9a4d2c8e1b6a3f5d0c9e7b2a4f8d1c"),
        }
    )
    env.pop("DATABASE_URL", None)
    env.pop("PUBLIC_BASE_URL", None)
    env.pop("VERCEL_URL", None)
    env.pop("VERCEL_PROJECT_PRODUCTION_URL", None)
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
    env.pop("PUBLIC_BASE_URL", None)
    env.pop("VERCEL_URL", None)
    env.pop("VERCEL_PROJECT_PRODUCTION_URL", None)
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
    result = run_python(
        "import src.config.settings.production",
        PRODUCTION_ENV
        | {
            "DATABASE_URL": "postgresql://production:example@db/production",
            "DATABASE_ENV": "preview",
        },
    )
    assert result.returncode != 0
    assert "DATABASE_ENV=production" in result.stderr


def test_production_without_database_serves_public_shell():
    result = run_python(
        (
            "import django, tempfile; django.setup(); "
            "from django.conf import settings; "
            "settings.STATIC_ROOT=tempfile.mkdtemp(); "
            "from django.core.management import call_command; "
            "call_command('collectstatic', verbosity=0, interactive=False); "
            "from django.test import Client; c=Client(); "
            "r=c.get('/ru/', "
            "HTTP_HOST='kan-open-research-immutable-test.vercel.app', "
            "HTTP_X_FORWARDED_PROTO='https'); "
            "assert r.status_code == 200; "
            "assert b'compute_node_unavailable' in r.content"
        ),
        PRODUCTION_ENV,
    )
    assert result.returncode == 0, result.stderr


def test_vercel_production_runtime_renders_without_collectstatic_manifest():
    result = run_python(
        (
            "import django, tempfile; django.setup(); "
            "from django.conf import settings; "
            "settings.STATIC_ROOT=tempfile.mkdtemp(); "
            "from django.test import Client; c=Client(); "
            "r=c.get('/ru/', "
            "HTTP_HOST='kan-open-research-immutable-test.vercel.app', "
            "HTTP_X_FORWARDED_PROTO='https'); "
            "assert r.status_code == 200; "
            "assert b'/static/public/css/site.css' in r.content"
        ),
        PRODUCTION_ENV,
    )

    assert result.returncode == 0, result.stderr
