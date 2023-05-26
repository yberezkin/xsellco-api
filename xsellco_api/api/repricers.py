# encoding: utf-8
from __future__ import annotations

import csv
from io import StringIO
from typing import Dict, List

from xsellco_api.base import BaseClient


class Repricers(BaseClient):
    # Repricer have separate HOST for api calls
    HOST = "api.repricer.com"
    endpoint = "repricers"
    header_text = "text/plain"

    def get_report(self) -> List[Dict]:
        headers = self.headers
        headers.update({"accept": self.header_text})

        response = self._request("GET", self.endpoint, headers=headers)
        _data = response.text.splitlines()

        reader = csv.DictReader(_data, delimiter=",")
        return [dict(e) for e in reader]

    def upload_report(self, data: List[Dict] | None = None, file_path: str | None = None):
        """
        https://developers.edesk.com/v1.0/reference/repricer-object
        In the same way that you may download a product template, containing a list of all your listings within our
        system, you may retrieve and upload this file programmatically. The file format you must upload is
        comma-separated ('CSV’). The format of the file you may retrieve is also comma-separated. When uploading a
        repricer file, only those listings contained within the file will be updated within our system. Also,
        the smaller the file size, the faster the desired action occurs.
        """
        headers = self.headers
        headers.update({"content-type": self.header_text})

        _bytes: bytes = b""

        if data is not None:
            with StringIO() as csvfile:
                wr = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                wr.writeheader()
                wr.writerows(data)
                _bytes = csvfile.getvalue().encode("UTF-8")

        elif file_path is not None:
            _bytes = open(file_path, "rb").read()

        else:
            raise ValueError("either `data` or `file_path` arguments must be provided")

        response = self._request("POST", self.endpoint, data=_bytes, headers=headers)
        return response.json()
