def sanitize_url(url: str) -> str:
    """Converts a url to a normalized state.

    ## Validators

    1. Ensures that url ends with /

    Args:
        url (str): url to sanitize

    Returns:
        str: sanitized url
    """
    return url if url.endswith("/") else f"{url}/"
