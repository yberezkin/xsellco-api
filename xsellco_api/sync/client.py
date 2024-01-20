import logging
from http import HTTPStatus
from typing import Dict, Optional, Union

import httpx
from httpx import HTTPStatusError

from xsellco_api.exceptions import (
    XsellcoAPIError,
    XsellcoAuthError,
    XsellcoNotFoundError,
    XsellcoRateLimitError,
    XsellcoServerError,
)
from xsellco_api.info import __package_name__, __version__

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Base Class for Xsellco's API using httpx for synchronous requests.
    """

    SCHEME = "https://"
    HOST = "api.xsellco.com"
    API_VERSION = "v1"
    USER_AGENT = f"python-{__package_name__}-{__version__}"

    def __init__(self, user_name: str, password: str) -> None:
        self.user_name = user_name
        self.password = password
        self.client = httpx.Client(base_url=self.url, headers=self.headers, auth=(self.user_name, self.password))

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "user-agent": self.USER_AGENT,
            "accept": "application/json",
            "content-type": "application/json",
        }

    @property
    def url(self) -> str:
        return f"{self.SCHEME}{self.HOST}/{self.API_VERSION}"

    def _request(
        self,
        method: str,
        endpoint: str,
        data=None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: Optional[Union[float, int]] = None,
    ) -> httpx.Response:
        try:
            # Correctly constructing the URL using the base URL and the endpoint
            all_headers = {**self.headers, **(headers or {})}
            response = self.client.request(
                method,
                f"{endpoint}".rstrip("/"),
                params=params,
                json=data if data and method in ("POST", "PUT", "PATCH") else None,
                headers=all_headers,
                timeout=timeout,
            )
            return self._process_response(response)
        except httpx.RequestError as req_err:
            # Handle request errors (e.g., network issues)
            logger.exception(f"Request Exception: {req_err}")
            raise XsellcoAPIError(f"Request Exception: {req_err}") from req_err

    @staticmethod
    def _process_response(response: httpx.Response) -> httpx.Response:
        """
        Process the response from the API.

        :param response: Response object from the requests library.
        :type response: Response
        :return response: Response object from the requests library if no errors occurred.
        :rtype: response: Response
        """
        try:
            response.raise_for_status()
            return response
        except HTTPStatusError as http_err:
            # Handle HTTP status errors (e.g., 404, 500, etc.)
            logger.exception(f"HTTP Exception: {http_err}")
            # Process specific HTTP errors based on status codes
            status_code = http_err.response.status_code
            # Handle specific status codes
            if status_code == HTTPStatus.UNAUTHORIZED:
                msg = f"{HTTPStatus.UNAUTHORIZED.description} for: {response.url}. Check your username and password."
                logger.error(msg)
                raise XsellcoAuthError(msg)
            elif status_code == HTTPStatus.NOT_FOUND:
                msg = f"{HTTPStatus.NOT_FOUND.description} for: {response.url}"
                logger.error(msg)
                raise XsellcoNotFoundError(msg)
            elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
                msg = f"{HTTPStatus.TOO_MANY_REQUESTS.description} Try again later."
                logger.error(msg)
                raise XsellcoRateLimitError(msg)
            elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                msg = (
                    f"{HTTPStatus.INTERNAL_SERVER_ERROR.description} from {response.url}."
                    f" Please try again later or contact support."
                )
                logger.error(msg)
                raise XsellcoServerError(msg)
            else:
                raise XsellcoAPIError(f"HTTP Error {status_code}: {http_err.response.text}") from http_err
        except Exception as e:
            # Catch other unforeseen errors
            logger.exception(f"Unexpected error: {e}")
            raise XsellcoAPIError(f"Unexpected error: {e}") from e

    def close(self):
        self.client.close()
