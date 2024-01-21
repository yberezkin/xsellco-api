from xsellco_api.async_.client import AsyncClient


class AsyncUsers(AsyncClient):
    endpoint = "users"

    async def get_user(self, user_id: int):
        response = await self._request("GET", f"{self.endpoint}/{user_id}")
        return response.json()

    async def get_users(self, page: int = 1, page_limit: int = 100):
        params = {"page_limit": page_limit, "page": page}
        response = await self._request("GET", endpoint=self.endpoint, params=params)
        return response.json()
