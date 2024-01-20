import pytest

from xsellco_api.sync.repricers import Repricers


def test_get_report(httpx_mock):
    # Mock the response for the report
    csv_content = "header1,header2\nvalue1,value2"
    httpx_mock.add_response(method="GET", url="https://api.repricer.com/v1/repricers", content=csv_content)

    repricer = Repricers("username", "password")
    report = repricer.get_report()

    assert len(report) == 1
    assert report[0] == {"header1": "value1", "header2": "value2"}


def test_upload_report_with_data(httpx_mock):
    # Mock the response for uploading the report
    httpx_mock.add_response(method="POST", url="https://api.repricer.com/v1/repricers", json={"success": True})

    repricer = Repricers("username", "password")
    data = [{"sku": "value1", "marketplace": "value2", "merchant_id": "value3", "fba": "value4"}]
    response = repricer.upload_report(data=data)

    assert response == {"success": True}


def test_upload_report_with_file(httpx_mock, tmp_path):
    # Create a temporary CSV file
    file_path = tmp_path / "report.csv"
    file_path.write_text("header1,header2\nvalue1,value2")

    # Mock the response for uploading the report
    httpx_mock.add_response(method="POST", url="https://api.repricer.com/v1/repricers", json={"success": True})

    repricer = Repricers("username", "password")
    response = repricer.upload_report(file_path=str(file_path))

    assert response == {"success": True}


def test_upload_report_no_data_no_file():
    repricer = Repricers("username", "password")

    with pytest.raises(ValueError) as ex:
        repricer.upload_report()

    assert "Either 'data' or 'file_path' must be provided." in str(ex.value)


def test_upload_report_both_data_and_file(tmp_path):
    repricer = Repricers("username", "password")
    data = [{"key": "value"}]
    file_path = tmp_path / "test.csv"
    file_path.write_text("key,value\n1,2")

    with pytest.raises(ValueError) as ex:
        repricer.upload_report(data=data, file_path=str(file_path))

    assert "Both 'data' and 'file_path' were provided. Please provide only one." in str(ex.value)


def test_upload_report_file_not_found():
    repricer = Repricers("username", "password")

    with pytest.raises(FileNotFoundError):
        repricer.upload_report(file_path="nonexistent.csv")


def test_generate_csv_bytes_data_error():
    repricer = Repricers("username", "password")
    data = [{"key1": "value1"}, {"key2": "value2"}]  # Different keys in dictionaries

    with pytest.raises(Exception):
        repricer.upload_report(data=data)
