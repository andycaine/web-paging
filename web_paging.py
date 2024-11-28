import base64
import functools
import json


def to_url_token(data: dict):
    """Create a URL-safe token for the given data."""
    if not data:
        return None
    s = json.dumps(data).encode('utf-8')
    return base64.urlsafe_b64encode(s).rstrip(b'=').decode('utf-8')


def from_url_token(token: dict, default=None):
    """Decode the given URL-safe token."""
    if not token:
        return default
    try:
        s = base64.urlsafe_b64decode(token + '=' * (-len(token) % 4))
        return json.loads(s)
    except Exception:
        return default


def pageable(template, param_getter,
             response_factory):
    def decorator(fn):
        @functools.wraps(fn)
        def decorated_fn(*args, **kwargs):
            paging_tokens = param_getter('pt', None)
            try:
                page = int(param_getter('page', 1))
            except ValueError:
                page = 1
            paging_keys = from_url_token(paging_tokens, {})
            paging_key = None
            if paging_keys and page > 1 and str(page) in paging_keys:
                paging_key = paging_keys[str(page)]

            # if paging_key is None, make sure page = 1
            if paging_key is None:
                page = 1

            kwargs['paging_key'] = paging_key
            ctx, next_paging_key = fn(*args, **kwargs)

            if next_paging_key:
                paging_keys[page + 1] = next_paging_key

            new_paging_tokens = to_url_token(paging_keys)

            ctx['web_paging_previous_page'] = page - 1 if page > 0 else None
            ctx['web_paging_next_page'] = page + 1 if next_paging_key else None
            ctx['web_paging_paging_tokens'] = new_paging_tokens
            return response_factory(template, **ctx)
        return decorated_fn
    return decorator