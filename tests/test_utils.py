from web_paging.utils import add_query_params


def test_add_query_params_existing_params():
    url_path = "/some/path?foo=bar"
    new_params = {"baz": "qux"}
    expected_url = "/some/path?foo=bar&baz=qux"
    new_url = add_query_params(url_path, new_params)
    assert new_url == expected_url


def test_add_query_params_no_params():
    url_path = "/some/path"
    new_params = {"baz": "qux", "foo": "bar"}
    expected_url = "/some/path?baz=qux&foo=bar"
    new_url = add_query_params(url_path, new_params)
    assert new_url == expected_url


def test_add_query_params_same_params():
    url_path = "/some/path?baz=foo"
    new_params = {"baz": "qux"}
    expected_url = "/some/path?baz=qux"
    new_url = add_query_params(url_path, new_params)
    assert new_url == expected_url
