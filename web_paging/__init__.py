from .core import pageable  # noqa: F401

try:
    from .flask_support import flask_pageable
except ImportError:
    flask_pageable = None
