
def test_methods_all(client, response):
    """Retrieve a list of available payment methods."""
    response.get('https://api.mollie.com/v2/methods', 'methods_multiple')

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
        assert method.description is not None
        assert method.image_size1x is not None
    assert iterated == 11
    assert len(set(iterated_method_ids)) == 11, 'Unexpected number of unique methods'


def test_method_get(client, response):
    """Retrieve a single payment method by ID."""
    response.get('https://api.mollie.com/v2/methods/ideal', 'method_get_ideal')

    method = client.methods.get('ideal')
    assert method.__class__.__name__ == 'Method'
    assert method.id == 'ideal'


def test_method_get_with_includes(client, response):
    """Retrieve a single payment method with includes."""
    response.get('https://api.mollie.com/v2/methods/ideal', 'method_get_ideal_with_includes')

    method = client.methods.get('ideal', include='issuers')
    assert len(method.issuers) == 11
    iterated_issuer_ids = []
    for issuer in method.issuers:
        # TODO adapt code below when we refactor Issuer
        assert issuer['id'] is not None
        iterated_issuer_ids.append(issuer['id'])

    assert len(set(iterated_issuer_ids)) == 11, 'Unexpected number of unique issuers'
