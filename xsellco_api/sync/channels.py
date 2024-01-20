from typing import Any, Dict

from xsellco_api.sync.client import SyncClient


class Channels(SyncClient):
    endpoint = "channels"

    def get_channel(self, channel_id: int):
        return self._request("GET", f"{self.endpoint}/{channel_id}").json()

    def get_channels(
        self, channel_type: str | None = None, channel_country: str | None = None, page: int = 1, page_limit: int = 100
    ):
        params: Dict[str, Any] = {"page_limit": page_limit, "page": page}
        if channel_type:
            params.update({"channel_type": channel_type})
        if channel_country:
            params.update({"channel_country": channel_country})
        return self._request("GET", endpoint=self.endpoint, params=params).json()
