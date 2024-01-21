import httpx
import pytest

from xsellco_api.exceptions import XsellcoAPIError
from xsellco_api.sync.client import SyncClient


def test_sync_client_initialization():
    client = SyncClient("username", "password")
    assert client.user_name == "username"
    assert client.password == "password"
    assert client._client is None


def test_sync_client_context_manager():
    with SyncClient("username", "password") as client:
        assert isinstance(client._client, httpx.Client)
    assert client._client is None


def test_sync_client_close():
    client = SyncClient("username", "password")
    client._get_client()  # Ensures the httpx.Client is created
    client.close()
    assert client._client is None


@pytest.mark.parametrize("method, endpoint", [("GET", "test"), ("POST", "test")])
def test_sync_client_request(httpx_mock, method, endpoint):
    httpx_mock.add_response(method=method, url=f"https://api.xsellco.com/v1/{endpoint}")
    client = SyncClient("username", "password")
    response = client._request(method, endpoint)
    assert response.status_code == 200


def test_sync_client_request_exception(httpx_mock):
    httpx_mock.add_exception(httpx.RequestError("Test Error"))
    client = SyncClient("username", "password")
    with pytest.raises(XsellcoAPIError):
        client._request("GET", "test")
