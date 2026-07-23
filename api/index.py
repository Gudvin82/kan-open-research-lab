# ruff: noqa: I001

from src.config.asgi import application
# Django resolves installed apps from strings at runtime, so keep these imports
# explicit for Vercel's Python file tracer.
from src.public import (
    apps as _public_apps,
    context_processors as _public_context_processors,
    middleware as _public_middleware,
    urls as _public_urls,
    views as _public_views,
)

# Vercel's Python runtime discovers ASGI applications exposed as ``app``.
app = application

_BUNDLED_MODULES = (
    _public_apps,
    _public_context_processors,
    _public_middleware,
    _public_urls,
    _public_views,
)
