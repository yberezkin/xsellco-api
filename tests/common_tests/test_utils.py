import pytest

from xsellco_api.common.utils import generate_csv_bytes_from_data, validate_data_headers


def test_generate_csv_bytes_from_data():
    # Sample data
    data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]
    # Expected CSV output as bytes
    expected_csv = b"header1,header2\nvalue1,value2\nvalue3,value4\n"
    result = generate_csv_bytes_from_data(data)
    # Assert the result matches the expected CSV output
    assert result == expected_csv


def test_generate_csv_bytes_from_data_with_empty_data():
    # Test with empty data
    data = []

    with pytest.raises(RuntimeError) as exc_info:
        generate_csv_bytes_from_data(data)

    # Optionally, you can assert the specific error message if needed
    assert "list index out of range" in str(exc_info.value)


def test_validate_data_headers():
    # Sample data
    data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]
    # Sample required headers
    required_headers = ["header1", "header2"]
    # Assert no exception is raised
    validate_data_headers(data, required_headers)


def test_validate_data_headers_with_missing_headers():
    # Sample data
    data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]
    # Sample required headers
    required_headers = ["header1", "header2", "header3"]
    # Assert a ValueError is raised
    with pytest.raises(ValueError) as exc_info:
        validate_data_headers(data, required_headers)

    # Optionally, you can assert the specific error message if needed
    assert "Missing mandatory header columns: header3" in str(exc_info.value)
