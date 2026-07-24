import re
from collections.abc import Iterable
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured

_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def normalize_production_host(value: str, *, source: str) -> str:
    """Return one exact ASCII hostname or fail closed on ambiguous input."""

    if "\\" in value or any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: control characters are forbidden"
        )
    raw = value.strip()
    if not raw:
        raise ImproperlyConfigured(f"Invalid production host in {source}: empty value")

    candidate = raw if "://" in raw else f"//{raw}"
    parsed = urlsplit(candidate)
    if parsed.scheme and parsed.scheme != "https":
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: unsupported scheme"
        )
    if parsed.username is not None or parsed.password is not None:
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: userinfo is forbidden"
        )
    if parsed.query or parsed.fragment:
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: query and fragment are forbidden"
        )

    try:
        host = parsed.hostname
        _ = parsed.port
    except ValueError as exc:
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: invalid port or hostname"
        ) from exc
    if not host or host.startswith(".") or "*" in host:
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: exact hostname required"
        )

    try:
        ascii_host = host.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: hostname encoding failed"
        ) from exc
    if len(ascii_host) > 253 or any(
        not _HOST_LABEL.fullmatch(label) for label in ascii_host.split(".")
    ):
        raise ImproperlyConfigured(
            f"Invalid production host in {source}: malformed hostname"
        )
    return ascii_host


def normalize_public_base_url(value: str, *, source: str) -> str:
    """Normalize a public URL to a stable HTTPS origin without path or port."""

    host = normalize_production_host(value, source=source)
    return f"https://{host}"


def unique_hosts(values: Iterable[tuple[str, str]]) -> list[str]:
    hosts: list[str] = []
    for source, value in values:
        host = normalize_production_host(value, source=source)
        if host not in hosts:
            hosts.append(host)
    return hosts
