import logging
from typing import Optional, Union

import httpx

from xsellco_api.common.base import BaseClient
from xsellco_api.exceptions import XsellcoAPIError

logger = logging.getLogger(__name__)


class AsyncClient(BaseClient):
    async def _get_client(self):
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.url, headers=self.headers, auth=(self.user_name, self.password)
            )
        return self._client

    async def __aenter__(self):
        await self._get_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        data=None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[Union[float, int]] = None,
    ) -> httpx.Response:
        try:
            data = data or {}
            params = params or {}
            all_headers = {**self.headers, **(headers or {})}

            if isinstance(data, bytes):
                # If data is bytes, use the content parameter
                request_args = {"content": data}
            else:
                # For non-bytes data, use the json parameter if applicable
                request_args = {"data": data} if data and method in ("POST", "PUT", "PATCH") else {}
            client = await self._get_client()
            response = await client.request(
                method, f"{endpoint}".rstrip("/"), params=params, headers=all_headers, timeout=timeout, **request_args
            )
            return self._process_response(response)
        except httpx.RequestError as req_err:
            logger.exception(f"Request Exception: {req_err}")
            raise XsellcoAPIError(f"Request Exception: {req_err}") from req_err
