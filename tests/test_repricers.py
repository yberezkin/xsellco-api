from unittest.mock import Mock, mock_open, patch

import pytest

from xsellco_api.api import Repricers

PATCH_TARGET = "xsellco_api.base.request"


@pytest.fixture
def repricers_client():
    return Repricers(user_name="test_user", password="test_password")


def test_get_report(repricers_client):
    mock_response = Mock()
    mock_response.text = "header1,header2\nvalue1,value2"

    with patch(PATCH_TARGET, return_value=mock_response):
        report = repricers_client.get_report()
        assert report == [{"header1": "value1", "header2": "value2"}]


def test_upload_report_data(repricers_client):
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}

    with patch(PATCH_TARGET, return_value=mock_response):
        result = repricers_client.upload_report(data=[{"header1": "value1", "header2": "value2"}])
        assert result == {"status": "success"}


def test_upload_report_file_path(repricers_client):
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}

    m_open = mock_open(read_data="header1,header2\nvalue1,value2")

    with patch(PATCH_TARGET, return_value=mock_response), patch("builtins.open", m_open):
        result = repricers_client.upload_report(file_path="mock_path.csv")
        assert result == {"status": "success"}


def test_generate_csv_bytes_from_data(repricers_client):
    data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]
    result = repricers_client._generate_csv_bytes_from_data(data)
    assert result == b"header1,header2\nvalue1,value2\nvalue3,value4\n"


# Additional tests can be added to cover edge cases, errors, etc.
def test_upload_report_no_data_or_filepath(repricers_client):
    with pytest.raises(ValueError, match="Either 'data' or 'file_path' must be provided."):
        repricers_client.upload_report()


def test_upload_report_data_and_filepath_provided(repricers_client):
    with pytest.raises(ValueError, match="Both 'data' and 'file_path' were provided. Please provide only one."):
        repricers_client.upload_report(data=[{"header1": "value1"}], file_path="mock_path.csv")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_upload_report_file_not_found(_, repricers_client):
    with pytest.raises(FileNotFoundError):
        repricers_client.upload_report(file_path="non_existent_path.csv")


@patch("xsellco_api.api.repricers.Repricers._generate_csv_bytes_from_data", side_effect=Exception("Unexpected error"))
@patch("xsellco_api.api.repricers.logger.exception")
def test_upload_report_unexpected_error(mocked_logger, _):
    repricers_client = Repricers(user_name="test_user", password="test_password")
    with pytest.raises(Exception, match="Unexpected error"):
        repricers_client.upload_report(data=[{"header1": "value1"}])

    # Check if the logger.exception was called with the expected message
    mocked_logger.assert_called_with("An unexpected error occurred: Unexpected error", exc_info=True)


def test_generate_csv_bytes_from_empty_data():
    with patch("xsellco_api.api.repricers.logger.exception") as mock_logger:
        with pytest.raises(IndexError):  # This is raised when trying to access data[0] on an empty list
            Repricers._generate_csv_bytes_from_data([])
        mock_logger.assert_called_once()


def test_generate_csv_bytes_from_mismatched_data():
    data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3"}]  # Mismatched keys

    csv_bytes = Repricers._generate_csv_bytes_from_data(data)
    csv_string = csv_bytes.decode("UTF-8")

    # Check the number of delimiters in each row
    for row in csv_string.strip().split("\n"):
        assert row.count(",") == 1, "Mismatched dictionary keys detected."
