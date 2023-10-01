# XSELLCO-API Python Wrapper

[![CodeFactor](https://www.codefactor.io/repository/github/yberezkin/xsellco-api/badge)](https://www.codefactor.io/repository/github/yberezkin/xsellco-api)
[![codecov](https://codecov.io/gh/yberezkin/xsellco-api/graph/badge.svg?token=ZVJIDL2T54)](https://codecov.io/gh/yberezkin/xsellco-api)

This project provides a Python wrapper for interacting with the [repricer.com](https://www.repricer.com/) (aka xsellco) API, allowing developers to easily integrate the API's functionality into their Python applications.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Installing
[![Badge](https://img.shields.io/pypi/v/xsellco-api?style=for-the-badge)](https://pypi.org/project/xsellco-api/)

    pip install xsellco_api

---

### Usage

```python
from xsellco_api.api import Repricers

# repricer reports API
repricer_data = Repricers(user_name='your_username', password='your_password').get_report()
print(repricer_data)  # list of dictionaries
# or
cli = Repricers(user_name='your_username', password='your_password')
repricer_data = cli.get_report()
print(repricer_data)
```

## License

![License](https://img.shields.io/github/license/yberezkin/xsellco-api?style=for-the-badge)
