
def test_methods_all(client, response):
    """Retrieve a list of available payment methods."""
    response.get('https://api.mollie.com/v2/methods', 'methods_list')

    methods = client.methods.all()
    assert methods.__class__.__name__ == 'List'
    assert methods.count == 11

    iterated = 0
    iterated_method_ids = []
    for method in methods:
        assert method.__class__.__name__ == 'Method'
        iterated += 1
        assert method.id is not None
        iterated_method_ids.append(method.id)
    assert iterated == methods.count
    assert len(set(iterated_method_ids)) == methods.count, 'Unexpected number of unique methods'


def test_method_get(client, response):
    """Retrieve a single payment method by ID."""
    response.get('https://api.mollie.com/v2/methods/ideal', 'method_get_ideal')

    method = client.methods.get('ideal')
    assert method.__class__.__name__ == 'Method'
    assert method.id == 'ideal'
    assert method.description == 'iDEAL'
    assert method.image_size1x == 'https://www.mollie.com/images/payscreen/methods/ideal.png'
    assert method.image_size2x == 'https://www.mollie.com/images/payscreen/methods/ideal%402x.png'
