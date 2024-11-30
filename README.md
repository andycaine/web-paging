# web-paging

Easy paging for the web.

## Description

`web-paging` is a simple library for paginating through web responses.

## Getting started

Install via pip (ideally in a virtualenv):

```bash
pip install web-paging
```

Then use the `web_paging.pageable` decorator to wrap any pageable view functions. E.g. if using Flask:

```python
from functools import partial

from flask import Flask, request, render_template
import web_paging


app = Flask(__name__)


def get_flask_arg(name, default):
    return request.args.get(name, default)


pageable = partial(
    web_paging.pageable,
    param_getter=lambda name, default: request.args.get(name, default),
    full_path_getter=lambda: request.full_path,
    response_factory=render_template
)


@app.get('/pageable')
@pageable('items.html')
def pageable_view(paging_key):
    items, next_paging_key = find_items(paging_key=paging_key)
    return dict(items=items), next_paging_key
```

The view is passed a paging key which can be used to identify the correct items to return. This is just a dict containing the attributes needed to find the correct results for the current page. For example, in a DynamoDB Query this dict would contain the attributes needed to create the ExclusiveStartKey. Similarly, the next_paging_key would be a dict created from the LastEvaluatedKey, containing the attributes needed to create the ExclusiveStartKey for the next page.

The `response_factory` function (`flask.render_template` in the example above) is passed the template name and a context object, containing the context returned from the view function (`dict(items=items)` in this example), plus some variables to render pagination links:

```html
{% if web_paging_paging_tokens %}
<p>
  {% if web_paging_previous_path %}
    <a href="{{ web_paging_previous_path }}">
      Previous page
    </a>
  {% endif %}
  {% if web_paging_next_path %}
    <a href="{{ web_paging_next_path }}">
      Next page
    </a>
  {% endif %}
</p>
{% endif %}
```

`web_paging_previous_path` and `web_paging_next_path` are instances of `markupsafe.Markup`.

The context also includes a couple of variables representing the page numbers of the previous and next pages. These variables are `web_paging_next_page` and `web_paging_previous_page`.

## Flask Support

`web-paging` has built-in support for Flask.  Install with:

```bash
pip install "web-paging[flask]"
```

Then you can use the `web_paging.flask_pageable` decorator:

```python
from web_paging import flask_pageable

@app.get('/pageable')
@flask_pageable('items.html')
def pageable_view(paging_key):
    items, next_paging_key = find_items(paging_key=paging_key)
    return dict(items=items), next_paging_key
```
