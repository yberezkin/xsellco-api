import httpx
import pytest

from xsellco_api.async_.client import AsyncClient
from xsellco_api.exceptions import XsellcoAPIError


@pytest.mark.asyncio
async def test_async_client_initialization():
    async_client = AsyncClient("username", "password")
    assert async_client.user_name == "username"
    assert async_client.password == "password"
    assert async_client._client is None


@pytest.mark.asyncio
async def test_async_client_context_manager():
    async with AsyncClient("username", "password") as async_client:
        assert isinstance(async_client._client, httpx.AsyncClient)
    assert async_client._client is None


@pytest.mark.asyncio
async def test_async_client_close():
    async_client = AsyncClient("username", "password")
    await async_client._get_client()  # Ensures the httpx.AsyncClient is created
    await async_client.close()
    assert async_client._client is None


@pytest.mark.asyncio
@pytest.mark.parametrize("method, endpoint", [("GET", "test"), ("POST", "test")])
async def test_async_client_request(httpx_mock, method, endpoint):
    httpx_mock.add_response(method=method, url=f"https://api.xsellco.com/v1/{endpoint}")
    async_client = AsyncClient("username", "password")
    response = await async_client._request(method, endpoint)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async_client_request_exception(httpx_mock):
    httpx_mock.add_exception(httpx.RequestError("Test Error"))
    async_client = AsyncClient("username", "password")
    with pytest.raises(XsellcoAPIError):
        await async_client._request("GET", "test")
