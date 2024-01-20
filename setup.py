import setuptools

from xsellco_api import info

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=info.__package_name__,
    version=info.__version__,
    author=info.__author__,
    author_email=info.__email__,
    description="Wrapper around Repricer.com API (aka Xsellco)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=info.__repo_url__,
    project_urls={"Bug Tracker": info.__bug_tracker__},
    license=info.__license__,
    install_requires=["requests>=2.30.0", "httpx>=0.18.0"],
    packages=["xsellco_api", "xsellco_api.api", "xsellco_api.sync", "xsellco_api.async_", "xsellco_api.common"],
    python_requires=">=3.9",
    keywords="xsellco, repricer",
)
