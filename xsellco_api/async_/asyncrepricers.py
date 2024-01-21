import csv
import logging
from typing import Any, Dict, List, Optional

from xsellco_api.async_.client import AsyncClient
from xsellco_api.common.utils import generate_csv_bytes_from_data, validate_data_headers

logger = logging.getLogger(__name__)


class AsyncRepricers(AsyncClient):
    HOST = "api.repricer.com"
    endpoint = "repricers"

    REQUIRED_HEADERS = ["sku", "marketplace", "merchant_id", "fba"]

    async def get_report(self) -> List[Dict]:
        response = await self._request("GET", self.endpoint)
        reader = csv.DictReader((line for line in response.text.splitlines()), delimiter=",")
        return [dict(e) for e in reader]

    async def upload_report(self, data: Optional[List[Dict]] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
        if not data and not file_path:
            raise ValueError("Either 'data' or 'file_path' must be provided.")

        if data and file_path:
            raise ValueError("Both 'data' and 'file_path' were provided. Please provide only one.")

        headers = {"content-type": "text/plain"}

        try:
            _bytes = b""
            if data:
                validate_data_headers(data, self.REQUIRED_HEADERS)
                _bytes = generate_csv_bytes_from_data(data)
            elif file_path:
                with open(file_path, "rb") as file:
                    _bytes = file.read()

            response = await self._request("POST", self.endpoint, data=_bytes, headers=headers)
            return response.json()

        except (ValueError, FileNotFoundError) as known_ex:
            logger.exception(f"Known exception occurred: {known_ex}", exc_info=False)
            raise
