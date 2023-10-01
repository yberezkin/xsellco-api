# encoding: utf-8

import csv
import logging
from io import StringIO
from typing import Any, Dict, List

from xsellco_api.base import BaseClient

logger = logging.getLogger(__name__)


class Repricers(BaseClient):
    HOST = "api.repricer.com"  # Repricer uses a different HOST for its API calls
    endpoint = "repricers"

    def get_report(self) -> List[Dict]:
        """
        https://developers.repricer.com/reference/get-a-repricer-file
        """
        response = self._request("GET", self.endpoint)
        reader = csv.DictReader((line for line in response.text.splitlines()), delimiter=",")
        return [dict(e) for e in reader]

    def upload_report(self, data: List[Dict] | None = None, file_path: str | None = None) -> Dict[str, Any]:
        """
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
                _bytes = self._generate_csv_bytes_from_data(data)
            elif file_path:
                with open(file_path, "rb") as file:
                    _bytes = file.read()

            response = self._request("POST", self.endpoint, data=_bytes, headers=headers)

            return response.json()

        except (ValueError, FileNotFoundError) as known_ex:
            logger.exception(f"Known exception occurred: {known_ex}", exc_info=True)
            raise

        except Exception as ex:
            # Handle any other unexpected exceptions
            logger.exception(f"An unexpected error occurred: {ex}", exc_info=True)
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
