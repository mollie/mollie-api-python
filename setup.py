import os.path

from setuptools import find_packages, setup


def get_long_description():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    try:
        readme = open(os.path.join(root_dir, 'README.md'), encoding='utf-8')
    except TypeError:
        # support python 2
        readme = open(os.path.join(root_dir, 'README.md'))
    long_description = readme.read()
    return long_description


setup(
    name='mollie-api-python',
    version='2.0.5',
    license='BSD',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    description='Mollie API client for Python',
    author='Mollie B.V.',
    author_email='info@mollie.com',
    maintainer='Four Digits B.V.',
    mainatiner_email='info@fourdigits.nl',
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
