# encoding: utf-8
import logging
from http import HTTPStatus
from typing import Dict, Optional, Union

from requests import HTTPError, RequestException, Response, request
from requests.auth import HTTPBasicAuth

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
    Base Class for Xsellco 's API.
    """

    SCHEME = "https://"
    HOST = "api.xsellco.com"
    API_VERSION = "v1"
    USER_AGENT = f"python-{__package_name__}-{__version__}"

    def __init__(self, user_name: str, password: str) -> None:
        self.user_name = user_name
        self.password = password

    @property
    def basic_auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.user_name, self.password)

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
    ) -> Response:
        """
        Make a request to xsellco's API.

        :param method: HTTP method e.g., GET, POST, etc.
        :type method: str
        :param endpoint: API endpoint e.g., 'users/'
        :type endpoint: str
        :param data: JSON data to be sent in the request body. Defaults to None.
        :type data: dict, optional
        :param params: URL parameters. Defaults to None.
        :type params: dict, optional
        :param headers: Additional headers to be sent with the request. Defaults to None.
        :type headers: dict, optional
        :param timeout: Request timeout. Defaults to None.
        :type timeout: float or int, optional
        :return: Response object from the requests library.
        :rtype: Response
        """
        data = data or {}
        params = params or {}

        all_headers = {**self.headers, **(headers or {})}

        try:
            resp = request(
                method,
                url=f"{self.url}/{endpoint}",
                params=params,
                data=data if data and method in ("POST", "PUT", "PATCH") else None,
                headers=all_headers,
                auth=self.basic_auth,
                timeout=timeout,
            )
            return self._process_response(resp)
        except RequestException as req_ex:
            # Handle any HTTP request-related exceptions
            logger.exception(f"Request Exception: {req_ex}")
            raise

    @staticmethod
    def _process_response(response: Response) -> Response:
        """
        Process the response from the API.

        :param response: Response object from the requests library.
        :type response: Response
        :return response: Response object from the requests library if no errors occurred.
        :rtype: response: Response
        """

        # Check for HTTP error status codes
        try:
            response.raise_for_status()
        except HTTPError:
            # Handle specific status codes
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                msg = f"{HTTPStatus.UNAUTHORIZED.description} for: {response.url}. Check your username and password."
                logger.error(msg)
                raise XsellcoAuthError(msg)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                msg = f"{HTTPStatus.NOT_FOUND.description} for: {response.url}"
                logger.error(msg)
                raise XsellcoNotFoundError(msg)
            elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                msg = f"{HTTPStatus.TOO_MANY_REQUESTS.description} Try again later."
                logger.error(msg)
                raise XsellcoRateLimitError(msg)
            elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                msg = (
                    f"{HTTPStatus.INTERNAL_SERVER_ERROR.description} from {response.url}. "
                    f"Please try again later or contact support."
                )
                logger.error(msg)
                raise XsellcoServerError(msg)
            else:
                msg = f"HTTP Error {response.status_code}: {response.text}"
                logger.error(msg)
                raise XsellcoAPIError(msg)

        return response
