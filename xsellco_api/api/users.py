# encoding: utf-8
from __future__ import annotations

from xsellco_api.base import BaseClient


class Users(BaseClient):
    endpoint = "users"

    def get_users(self, user_id: int | None = None):
        resp = self._request("GET", endpoint=self.endpoint if not user_id else f"{self.endpoint}/{user_id}")
        return resp.json()
