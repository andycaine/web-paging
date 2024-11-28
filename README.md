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
from web_paging import pageable


app = Flask(__name__)


def get_flask_arg(name, default):
    return request.args.get(name, default)


pageable = partial(pageable,
                   param_getter=get_flask_arg,
                   response_factory=render_template)


@app.get('/pageable')
@pageable('items.html')
def pageable_view(paging_key):
    items, next_paging_key = find_items(paging_key=paging_key)
    return dict(items=items), next_paging_key
```

The view is passed a paging key which can be used to identify the correct items to return. This is just a dict containing the attributes needed to find the correct results for the current page. For example, in a DynamoDB Query this dict would contain the attributes needed to create the ExclusiveStartKey. Similarly, the next_paging_key would be a dict created from the LastEvaluatedKey, containing the attributes needed to create the ExclusiveStartKey for the next page.

The `response_factory` function (`flask.render_template` in the example above) is passed the template name and a context object, containing the context returned from the view function (`dict(items=items)` in this example), plus some variables that can be used to render pagination links. These variables are `web_paging_next_page`, `web_paging_previous_page`, and `web_paging_paging_tokens`. Any pageable URLs created should pass through the paging tokens and the current page using the `pt` and `page` request parameters, respectively.  E.g. using Jinja2:

```html
{% if web_paging_previous_page %}
    <a href="{{ url_for ('pageable_view') }}?pt={{ web_paging_paging_tokens }}&page={{ web_paging_previous_page }}">Previous page</a>
{% endif %}
{% if web_paging_next_page %}
    <a href="{{ url_for ('pageable_view') }}?pt={{ web_paging_paging_tokens }}&page={{ web_paging_next_page }}">Next page</a>
{% endif %}
```
