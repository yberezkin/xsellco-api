# encoding: utf-8
from __future__ import annotations

from xsellco_api.base import BaseClient


class Users(BaseClient):
    endpoint = "users"

    def get_user(self, user_id: int):
        return self._request("GET", f"{self.endpoint}/{user_id}").json()

    def get_users(self, page: int = 1, page_limit: int = 100):
        params = {"page_limit": page_limit, "page": page}
        return self._request("GET", endpoint=self.endpoint, params=params).json()
