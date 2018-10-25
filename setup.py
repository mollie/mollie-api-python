from setuptools import find_packages, setup

setup(
    name='mollie-api-python',
    version='2.0.2',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    description='Mollie API client for Python',
    author='Mollie B.V.',
    author_email='info@mollie.nl',
    keywords=['mollie', 'payment', 'service', 'ideal', 'creditcard', 'mistercash', 'bancontact', 'sofort',
              'sofortbanking', 'sepa', 'bitcoin', 'paypal', 'paysafecard', 'podiumcadeaukaart', 'banktransfer',
              'direct debit', 'belfius', 'belfius direct net', 'kbc', 'cbc', 'refunds', 'payments', 'gateway',
              'gift cards', 'intersolve', 'fashioncheque', 'podium cadeaukaart', 'yourgift', 'vvv giftcard',
              'webshop giftcard', 'nationale entertainment card', 'ing homepay'],
    url='https://github.com/mollie/mollie-api-python',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    setup_requires=["pytest-runner", ],
    tests_require=["pytest", ],

)
