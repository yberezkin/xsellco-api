import csv
import logging
from io import StringIO
from typing import Any, Dict, List, Optional

from xsellco_api.sync.client import SyncClient

logger = logging.getLogger(__name__)


class Repricers(SyncClient):
    HOST = "api.repricer.com"  # Repricer uses a different HOST for its API calls
    endpoint = "repricers"

    REQUIRED_HEADERS = ["sku", "marketplace", "merchant_id", "fba"]

    def _validate_data_headers(self, data: List[Dict]) -> None:
        missing_headers = set(self.REQUIRED_HEADERS) - set(data[0].keys())
        if missing_headers:
            raise ValueError(f"Missing mandatory header columns: {', '.join(missing_headers)}")

    def get_report(self) -> List[Dict]:
        """
        Retrieves a repricer report.
        https://developers.repricer.com/reference/get-a-repricer-file
        """
        response = self._request("GET", self.endpoint)
        reader = csv.DictReader((line for line in response.text.splitlines()), delimiter=",")
        return [dict(e) for e in reader]

    def upload_report(self, data: Optional[List[Dict]] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Uploads a repricer report.
        https://developers.repricer.com/reference/upload-a-repricer-file
        """
        if not data and not file_path:
            raise ValueError("Either 'data' or 'file_path' must be provided.")

        if data and file_path:
            raise ValueError("Both 'data' and 'file_path' were provided. Please provide only one.")

        headers = {"content-type": "text/plain"}

        _bytes: bytes = b""

        try:
            if data:
                self._validate_data_headers(data)  # Validate headers
                _bytes = self._generate_csv_bytes_from_data(data)
            elif file_path:
                # When we're using file path, we don't validate headers. We assume the file is valid.
                with open(file_path, "rb") as file:
                    _bytes = file.read()

            response = self._request("POST", self.endpoint, data=_bytes, headers=headers)

            return response.json()

        except (ValueError, FileNotFoundError) as known_ex:
            logger.exception(f"Known exception occurred: {known_ex}", exc_info=False)
            raise

    @staticmethod
    def _generate_csv_bytes_from_data(data: List[Dict]) -> bytes:
        try:
            with StringIO(
                newline=""
            ) as csvfile:  # Explicitly set newline to an empty string for cross-platform compatibility
                wr = csv.DictWriter(csvfile, fieldnames=data[0].keys(), lineterminator="\n")
                wr.writeheader()
                wr.writerows(data)
                return csvfile.getvalue().encode("UTF-8")
        except Exception as ex:
            logger.exception(f"Error generating CSV bytes: {ex}", exc_info=True)
            raise
