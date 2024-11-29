from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def add_query_params(url_path, new_params):
    # Parse the URL into components
    parsed_url = urlparse(url_path)

    # Parse existing query parameters into a dictionary
    existing_params = parse_qs(parsed_url.query)

    # Update with new parameters (parse_qs returns lists; normalize to single
    # values)
    for key, value in new_params.items():
        existing_params[key] = [value]

    # Reconstruct the query string
    updated_query = urlencode(existing_params, doseq=True)

    # Rebuild the URL with the updated query string
    updated_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        updated_query,
        parsed_url.fragment
    ))

    return updated_url
