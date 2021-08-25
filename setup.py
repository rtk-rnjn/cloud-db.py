from re import MULTILINE, search

from setuptools import setup  # type: ignore

with open("README.md") as f:
    readme = f.read()

# source: https://github.com/Rapptz/discord.py/blob/master/setup.py

with open("cloud_db/__init__.py") as f:
    content = f.read()
    version = search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE
        ).group(1)
    author = search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE).group(
        1
        )
    _license = search(
        r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', content, MULTILINE
        ).group(1)

setup(
    name = "cloud-db.py",
    description = "An easy-to-use Wrapper for the Cloud-DB API.",
    long_description = readme,
    long_description_content_type = "text/markdown",
    version = version,
    packages = ["cloud_db"],
    url = "https://github.com/Soheab/cloud-db.py",
    download_url = f"https://github.com/Soheab/cloud-db.py/archive/v{version}.tar.gz",
    license = _license,
    author = author,
    install_requires = ["aiohttp"],
    keywords = [
        "database",
        "discord",
        "cloud",
        "cloud database",
        "db",
        "online db",
        "discord.py",
        "api",
        "wrapper"
        ],
    project_urls = {
        "Discord": "https://discord.gg/nEtTMS934g",
        },
    python_requires = ">=3.8",
    )