import setuptools

from xsellco_api import info

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=info.__package_name__,
    version=info.__version__,
    author=info.__author__,
    author_email=info.__email__,
    description="Testing installation of Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=info.__repo_url__,
    project_urls={"Bug Tracker": info.__bug_tracker__},
    license=info.__license__,
    packages=[info.__package_name__],
    install_requires=["requests"],
)
