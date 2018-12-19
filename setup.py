import os.path
import re

from setuptools import find_packages, setup

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    try:
        readme = open(os.path.join(ROOT_DIR, 'README.md'), encoding='utf-8')
    except TypeError:
        # support python 2
        readme = open(os.path.join(ROOT_DIR, 'README.md'))
    long_description = readme.read()
    return long_description


def get_version():
    """
    Read the version from a file (mollie/api/version.py) in the repository.

    We can't import here since we might import from an installed version.
    """
    try:
        version_file = open(os.path.join(ROOT_DIR, 'mollie', 'api', 'version.py'), encoding='utf=8')
    except TypeError:
        # support python 2
        version_file = open(os.path.join(ROOT_DIR, 'mollie', 'api', 'version.py'))
    contents = version_file.read()
    match = re.search(r'VERSION = [\'"]([^\'"]+)', contents)
    if match:
        return match.group(1)
    else:
        raise RuntimeError("Can't determine package version")


setup(
    name='mollie-api-python',
    version=get_version(),
    license='BSD',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    description='Mollie API client for Python',
    author='Mollie B.V.',
    author_email='info@mollie.com',
    maintainer='Four Digits B.V.',
    maintainer_email='info@fourdigits.nl',
    keywords=['mollie', 'payment', 'service', 'ideal', 'creditcard', 'mistercash', 'bancontact', 'sofort',
              'sofortbanking', 'sepa', 'bitcoin', 'paypal', 'paysafecard', 'podiumcadeaukaart', 'banktransfer',
              'direct debit', 'belfius', 'belfius direct net', 'kbc', 'cbc', 'refunds', 'payments', 'gateway',
              'gift cards', 'intersolve', 'fashioncheque', 'podium cadeaukaart', 'yourgift', 'vvv giftcard',
              'webshop giftcard', 'nationale entertainment card', 'ing homepay', 'klarna pay later',
              'klarna slice it'],
    url='https://github.com/mollie/mollie-api-python',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business :: Financial',
    ],
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],

)
