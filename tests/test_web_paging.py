import pytest
from markupsafe import Markup

from web_paging import pageable


@pytest.fixture
def items():
    return [i for i in range(100)]


@pytest.fixture
def view(items):
    def _view(paging_key):
        start = 0
        if paging_key:
            start = paging_key

        page = items[start:start + 10]
        next_paging_key = start + 10
        return dict(page=page), next_paging_key
    return _view


@pytest.fixture
def params():
    return {}


@pytest.fixture
def response_factory():
    def _response_factory(template, **context):
        return (context, template)
    return _response_factory


@pytest.fixture
def full_path_getter():
    def _full_path_getter():
        return '/foo/?bar=test_bar'
    return _full_path_getter


@pytest.fixture
def pager(view, params, response_factory, full_path_getter):
    return pageable(template='foo',
                    param_getter=params.get,
                    full_path_getter=full_path_getter,
                    response_factory=response_factory)(view)


def assert_markup(markup, expected):
    assert markup == expected
    assert isinstance(markup, Markup)


def assert_page(template, context, next, prev, items):
    assert template == 'foo'
    assert context['web_paging_next_page'] == next
    assert context['web_paging_previous_page'] == prev
    assert context['page'] == items
    pt = context['web_paging_paging_tokens']
    assert_markup(context['web_paging_next_path'],
                  f'/foo/?bar=test_bar&pt={pt}&page={next}')
    if prev:
        assert_markup(context['web_paging_previous_path'],
                      f'/foo/?bar=test_bar&pt={pt}&page={prev}')


def test_pageable(items, params, pager):
    context, template = pager()

    assert_page(template, context, 2, 0, items[0:10])

    params['pt'] = context['web_paging_paging_tokens']
    params['page'] = '2'

    context, template = pager()

    assert_page(template, context, 3, 1, items[10:20])

    params['pt'] = context['web_paging_paging_tokens']
    params['page'] = '1'

    context, template = pager()

    assert_page(template, context, 2, 0, items[0:10])


def test_invalid_page(items, params, pager):
    params['page'] = 'invalid-page'
    context, template = pager()

    assert_page(template, context, 2, 0, items[0:10])


def test_invalid_paging_token(items, params, pager):
    params['pt'] = 'invalid-token'
    params['page'] = '3'
    context, template = pager()

    assert_page(template, context, 2, 0, items[0:10])
