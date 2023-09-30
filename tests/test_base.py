from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import ConnectionError, HTTPError

from xsellco_api.base import BaseClient
from xsellco_api.exceptions import (
    XsellcoAPIError,
    XsellcoAuthError,
    XsellcoNotFoundError,
    XsellcoRateLimitError,
    XsellcoServerError,
)

# Constants for testing
TEST_USERNAME = "test_user"
TEST_PASSWORD = "test_pass"


@pytest.fixture
def base_client():
    return BaseClient(TEST_USERNAME, TEST_PASSWORD)


def test_base_client_initialization(base_client):
    assert base_client.user_name == TEST_USERNAME
    assert base_client.password == TEST_PASSWORD


def test_base_client_headers(base_client):
    headers = base_client.headers
    assert headers["user-agent"].startswith("python-")
    assert headers["accept"] == "application/json"
    assert headers["content-type"] == "application/json"


def test_base_client_url(base_client):
    assert base_client.url == "https://api.xsellco.com/v1"


@patch("xsellco_api.base.request")
def test_base_client_request_success(mock_request, base_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "success"
    mock_request.return_value = mock_response

    response = base_client._request("GET", "test_endpoint")

    assert response.status_code == 200
    assert response.text == "success"


@pytest.mark.parametrize(
    "status_code, exception",
    [
        (HTTPStatus.UNAUTHORIZED, XsellcoAuthError),
        (404, XsellcoNotFoundError),
        (429, XsellcoRateLimitError),
        (500, XsellcoServerError),
        (400, XsellcoAPIError),
    ],
)
@patch("xsellco_api.base.request")
def test_base_client_request_failures(mock_request, base_client, status_code, exception):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError()
    mock_response.status_code = status_code
    mock_request.return_value = mock_response

    with pytest.raises(exception):
        base_client._request("GET", "test_endpoint")


@patch("xsellco_api.base.request")
def test_base_client_request_connection_error(mock_request, base_client):
    # Mock the request method to raise a ConnectionError
    mock_request.side_effect = ConnectionError("Failed to establish a new connection: [Errno 61] Connection refused")

    with pytest.raises(ConnectionError):
        base_client._request("GET", "test_endpoint")
