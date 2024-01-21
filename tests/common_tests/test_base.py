from http import HTTPStatus

import pytest
from httpx import Request, Response

from xsellco_api.common.base import BaseClient
from xsellco_api.exceptions import (
    XsellcoAPIError,
    XsellcoAuthError,
    XsellcoNotFoundError,
    XsellcoRateLimitError,
    XsellcoServerError,
)


def test_base_client_initialization():
    client = BaseClient("username", "password")
    assert client.user_name == "username"
    assert client.password == "password"
    assert client.headers["accept"] == "application/json"
    assert client.headers["content-type"] == "application/json"
    assert client.url == "https://api.xsellco.com/v1"


def test_process_response_success():
    response = Response(status_code=HTTPStatus.OK, request=Request(method="GET", url="https://test"))
    assert BaseClient._process_response(response) == response


def test_process_response_unexpected_error():
    # Simulate a response that would raise an unexpected error when processed
    response = "not a valid response object"
    with pytest.raises(XsellcoAPIError):
        BaseClient._process_response(response)


@pytest.mark.parametrize(
    "status_code, exception_type",
    [
        (HTTPStatus.UNAUTHORIZED, XsellcoAuthError),
        (HTTPStatus.NOT_FOUND, XsellcoNotFoundError),
        (HTTPStatus.TOO_MANY_REQUESTS, XsellcoRateLimitError),
        (HTTPStatus.INTERNAL_SERVER_ERROR, XsellcoServerError),
        (499, XsellcoAPIError),  # Test for an arbitrary non-handled HTTP status
    ],
)
def test_process_response(status_code, exception_type):
    response = Response(status_code=status_code, request=Request(method="GET", url="https://test"))
    with pytest.raises(exception_type):
        BaseClient._process_response(response)
