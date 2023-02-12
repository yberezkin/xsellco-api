# encoding: utf-8
from __future__ import annotations

from typing import Dict

from requests import Response, request
from requests.auth import HTTPBasicAuth

from xsellco_api.info import __package_name__, __version__


class BaseClient:
    SCHEME = "https://"
    HOST = "api.xsellco.com"
    API_VERSION = "v1"
    USER_AGENT = f"python-{__package_name__}-{__version__}"
    URL = f"{SCHEME}{HOST}/{API_VERSION}"

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

    def _request(
        self,
        method: str,
        endpoint: str,
        data=None,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: float | int | None = None,
    ) -> Response:
        if params is None:
            params = {}
        if data is None:
            data = {}

        resp = request(
            method,
            f"{self.URL}/{endpoint}",
            params=params,
            data=data if data and method in ("POST", "PUT", "PATCH") else None,
            headers=headers or self.headers,
            auth=self.basic_auth,
            timeout=timeout,
        )
        return resp
