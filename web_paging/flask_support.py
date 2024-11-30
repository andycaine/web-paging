from functools import partial

from flask import (
    render_template, request
)
import web_paging


flask_pageable = partial(
    web_paging.pageable,
    param_getter=lambda name, default: request.args.get(name, default),
    full_path_getter=lambda: request.full_path,
    response_factory=render_template
)
