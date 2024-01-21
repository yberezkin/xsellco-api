import pytest

from xsellco_api.async_.asyncrepricers import AsyncRepricers


@pytest.mark.asyncio
async def test_get_report(httpx_mock):
    # Mock the response
    httpx_mock.add_response(method="GET", url="https://api.repricer.com/v1/repricers", text="sku,price\n123,10")

    async with AsyncRepricers("user", "pass") as repricers:
        report = await repricers.get_report()
        print(f"Report received: {report}")
        assert report == [{"sku": "123", "price": "10"}]


@pytest.mark.asyncio
async def test_upload_report_success(httpx_mock):
    # Mock the response for successful upload
    httpx_mock.add_response(method="POST", url="https://api.repricer.com/v1/repricers", json={"status": "success"})

    async with AsyncRepricers("user", "pass") as repricers:
        response = await repricers.upload_report(
            data=[{"sku": "123", "marketplace": "Amazon", "merchant_id": "1", "fba": "yes"}]
        )
        assert response == {"status": "success"}


@pytest.mark.asyncio
async def test_upload_report_missing_headers():
    async with AsyncRepricers("user", "pass") as repricers:
        with pytest.raises(ValueError):
            await repricers.upload_report(data=[{"sku": "123"}])


@pytest.mark.asyncio
async def test_upload_report_missing_data_and_file_path():
    async with AsyncRepricers("user", "pass") as repricers:
        with pytest.raises(ValueError):
            await repricers.upload_report()


@pytest.mark.asyncio
async def test_upload_report_provided_data_and_file_path():
    async with AsyncRepricers("user", "pass") as repricers:
        with pytest.raises(ValueError):
            await repricers.upload_report(data=[{"sku": "123"}], file_path="test.csv")


@pytest.mark.asyncio
async def test_upload_report_file_path(httpx_mock, tmp_path):
    # Create a temporary CSV file
    file_path = tmp_path / "report.csv"
    file_path.write_text("header1,header2\nvalue1,value2")
    # Mock the response for successful upload
    httpx_mock.add_response(method="POST", url="https://api.repricer.com/v1/repricers", json={"status": "success"})

    async with AsyncRepricers("user", "pass") as repricers:
        response = await repricers.upload_report(file_path=file_path)
        assert response == {"status": "success"}
