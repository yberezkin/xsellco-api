from http import HTTPStatus
from typing import Dict

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

DEPRECATION_MESSAGE = """The xsellco_api.api module is deprecated and will be removed in a future version.
Please update your code to use the new async or sync modules.
ex: from xsellco_api.sync import Repricers, Channels, Users
or
from xsellco_api.async_ import AsyncRepricers, AsyncChannels, AsyncUsers
"""


class BaseClient:
    SCHEME = "https://"
    HOST = "api.xsellco.com"
    API_VERSION = "v1"
    USER_AGENT = f"python-{__package_name__}-{__version__}"

    def __init__(self, user_name: str, password: str) -> None:
        self.user_name = user_name
        self.password = password
        self._client = None

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

    @staticmethod
    def _process_response(response: httpx.Response) -> httpx.Response:
        try:
            response.raise_for_status()
            return response
        except HTTPStatusError as http_err:
            status_code = http_err.response.status_code
            if status_code == HTTPStatus.UNAUTHORIZED:
                msg = f"{HTTPStatus.UNAUTHORIZED.description} for: {response.url}"
                raise XsellcoAuthError(msg)
            elif status_code == HTTPStatus.NOT_FOUND:
                raise XsellcoNotFoundError(f"{HTTPStatus.NOT_FOUND.description} for: {response.url}")
            elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
                raise XsellcoRateLimitError(f"{HTTPStatus.TOO_MANY_REQUESTS.description}")
            elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                raise XsellcoServerError(f"{HTTPStatus.INTERNAL_SERVER_ERROR.description} from {response.url}")
            else:
                raise XsellcoAPIError(f"HTTP Error {status_code}: {http_err.response.text}") from http_err
        except Exception as e:
            raise XsellcoAPIError(f"Unexpected error: {e}") from e
