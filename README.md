# XSELLCO-API Python Wrapper

[![CodeFactor](https://www.codefactor.io/repository/github/yberezkin/xsellco-api/badge)](https://www.codefactor.io/repository/github/yberezkin/xsellco-api)
[![pytest](https://github.com/yberezkin/xsellco-api/actions/workflows/python-pytest.yml/badge.svg)](https://github.com/yberezkin/xsellco-api/actions/workflows/python-pytest.yml)
[![codecov](https://codecov.io/gh/yberezkin/xsellco-api/graph/badge.svg?token=ZVJIDL2T54)](https://codecov.io/gh/yberezkin/xsellco-api)


This project provides a Python wrapper for interacting with the [Repricer.com](https://www.repricer.com/) (aka Xsellco) API, simplifying the integration of Repricer.com's API features into Python applications. It offers both synchronous and asynchronous support to accommodate different programming needs, thanks in part to the [httpx library](https://github.com/encode/httpx). Detailed API documentation can be found at [eDesk Developers](https://developers.edesk.com/).
Also new API documentation because of separation of Repricer.com and eDesk API can be found at [repricer api](https://developers.repricer.com/reference).

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Installing
[![Badge](https://img.shields.io/pypi/v/xsellco-api?style=for-the-badge)](https://pypi.org/project/xsellco-api/)

    pip install xsellco_api

### For Developing:
Clone the repository and install `requirements-dev.txt`:

---

### Usage

The library provides both synchronous (sync) and asynchronous (async_) interfaces for interacting with the Repricer.com API. Below are examples of how to use each interface:

#### Synchronous Usage
```python
from xsellco_api.sync import Repricers

repricer = Repricers(user_name='your_username', password='your_password')
repricer_data = repricer.get_report()
print(repricer_data)  # list of dictionaries

# or
# All classes support context manager usage
with Repricers(user_name='your_username', password='your_password') as repricer:
    repricer_data = repricer.get_report()
    print(repricer_data)  # list of dictionaries
```
#### Asynchronous Usage
```python
import asyncio
from xsellco_api.async_ import AsyncRepricers

async def main():
    async with AsyncRepricers(user_name='your_username', password='your_password') as repricer:
        repricer_data = await repricer.get_report()
        print(repricer_data)

asyncio.run(main())
```

### Deprecation Notice
Please note that the xsellco_api.api module is deprecated and will be removed in future versions. Users are encouraged to switch to the sync or async_ modules for continued support.


## License

![License](https://img.shields.io/github/license/yberezkin/xsellco-api?style=for-the-badge)
