from setuptools import setup, find_packages
setup(
    name = 'mollie-api-python',
    version = '1.0.2',
    license = 'BSD',
    packages = find_packages(), 
    include_package_data = True,
    description = 'Mollie API client for Python',
    author = 'Mollie B.V.',
    author_email = 'info@mollie.nl',
    keywords = ['mollie', 'payment', 'service', 'ideal', 'creditcard', 'mistercash', 'bancontact', 'sofort', 'sofortbanking', 'sepa', 'bitcoin', 'paypal', 'paysafecard', 'banktransfer', 'direct debit', 'belfius', 'belfius direct net', 'refunds', 'payments', 'gateway'],
    url = 'https://github.com/mollie/mollie-api-python',
    install_requires=['requests'],
)
