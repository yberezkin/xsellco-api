class XsellcoAPIError(Exception):
    """Base exception for xsellco API errors."""

    pass


class XsellcoAuthError(XsellcoAPIError):
    """Raised when there's an authentication error (401)."""

    pass


class XsellcoNotFoundError(XsellcoAPIError):
    """Raised when the requested resource is not found (404)."""

    pass


class XsellcoRateLimitError(XsellcoAPIError):
    """Raised when rate limit is reached (429)."""

    pass


class XsellcoServerError(XsellcoAPIError):
    """Raised when the Xsellco API returns a 500 Internal Server Error."""

    pass
