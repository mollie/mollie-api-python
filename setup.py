import os.path
import re

from setuptools import find_packages, setup

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    return open(os.path.join(ROOT_DIR, "README.md"), encoding="utf-8").read()


def get_version():
    """Read the version from a file (mollie/api/version.py) in the repository.

    We can't import here since we might import from an installed version.
    """
    version_file = open(os.path.join(ROOT_DIR, "mollie", "api", "version.py"), encoding="utf=8")
    contents = version_file.read()
    match = re.search(r'VERSION = [\'"]([^\'"]+)', contents)
    if match:
        return match.group(1)
    else:
        raise RuntimeError("Can't determine package version")


setup(
    name="mollie-api-python",
    version=get_version(),
    license="BSD",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    description="Mollie API client for Python",
    author="Mollie B.V.",
    author_email="info@mollie.com",
    maintainer="Four Digits B.V.",
    maintainer_email="info@fourdigits.nl",
    keywords=[
        "mollie",
        "payment",
        "service",
        "ideal",
        "creditcard",
        "mistercash",
        "bancontact",
        "sofort",
        "sofortbanking",
        "sepa",
        "paypal",
        "paysafecard",
        "podiumcadeaukaart",
        "banktransfer",
        "direct debit",
        "belfius",
        "belfius direct net",
        "kbc",
        "cbc",
        "refunds",
        "payments",
        "gateway",
        "gift cards",
        "intersolve",
        "fashioncheque",
        "podium cadeaukaart",
        "yourgift",
        "vvv giftcard",
        "webshop giftcard",
        "nationale entertainment card",
        "klarna pay later",
        "klarna pay now",
        "klarna slice it",
        "przelewy24",
    ],
    url="https://github.com/mollie/mollie-api-python",
    install_requires=[
        "requests",
        "urllib3",
        "requests_oauthlib",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Office/Business :: Financial",
    ],
)
