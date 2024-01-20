from http import HTTPStatus

import httpx
import pytest

from xsellco_api.exceptions import (
    XsellcoAPIError,
    XsellcoAuthError,
    XsellcoNotFoundError,
    XsellcoRateLimitError,
    XsellcoServerError,
)
from xsellco_api.sync.client import BaseClient


def test_initialization():
    client = BaseClient("username", "password")
    assert client.user_name == "username"
    assert client.password == "password"
    # Test other properties as needed
    assert client.headers["accept"] == "application/json"
    assert client.headers["content-type"] == "application/json"


def test_context_manager_initialization():
    with BaseClient("username", "password") as client:
        assert client._client is not None
    # Assert that the client is closed after exiting the context
    assert client._client is None


def test_client_reuse(httpx_mock):
    httpx_mock.add_response(method="GET", url="https://api.xsellco.com/v1/test", status_code=200)
    client = BaseClient("user", "pass")

    response1 = client._request("GET", "test")
    client1 = client._client

    response2 = client._request("GET", "test")
    client2 = client._client

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert client1 is client2  # Same client object is reused


def test_close_method():
    client = BaseClient("username", "password")
    client._get_client()  # Ensure client is created
    assert client._client is not None
    client.close()
    assert client._client is None


def test_successful_request(httpx_mock):
    httpx_mock.add_response(method="GET", url="https://api.xsellco.com/v1/test", status_code=200)
    client = BaseClient("user", "pass")
    response = client._request("GET", "test")
    assert response.status_code == 200


def test_request_exception(httpx_mock):
    httpx_mock.add_exception(httpx.RequestError("Test Error"))
    client = BaseClient("user", "pass")
    with pytest.raises(XsellcoAPIError):
        client._request("GET", "test")


# Parametrized test for different HTTP errors
@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (HTTPStatus.UNAUTHORIZED, XsellcoAuthError),
        (HTTPStatus.NOT_FOUND, XsellcoNotFoundError),
        (HTTPStatus.TOO_MANY_REQUESTS, XsellcoRateLimitError),
        (HTTPStatus.INTERNAL_SERVER_ERROR, XsellcoServerError),
        (418, XsellcoAPIError),  # 418 I'm a teapot (generic HTTP error)
    ],
)
def test_http_errors(httpx_mock, status_code, expected_exception):
    httpx_mock.add_response(method="GET", url="https://api.xsellco.com/v1/test", status_code=status_code)
    client = BaseClient("user", "pass")
    with pytest.raises(expected_exception):
        client._request("GET", "test")
