import csv
from io import StringIO
from typing import Dict, List


def generate_csv_bytes_from_data(data: List[Dict]) -> bytes:
    try:
        with StringIO(newline="") as csvfile:
            wr = csv.DictWriter(csvfile, fieldnames=data[0].keys(), lineterminator="\n")
            wr.writeheader()
            wr.writerows(data)
            return csvfile.getvalue().encode("UTF-8")
    except Exception as ex:
        raise RuntimeError(f"Error generating CSV bytes: {ex}") from ex


def validate_data_headers(data: List[Dict], required_headers: List[str]) -> None:
    missing_headers = set(required_headers) - set(data[0].keys())
    if missing_headers:
        raise ValueError(f"Missing mandatory header columns: {', '.join(missing_headers)}")
