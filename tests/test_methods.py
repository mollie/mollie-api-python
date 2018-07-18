
def test_methods_all(client, response):
    response.get('https://api.mollie.nl/v2/methods', 'methods_ideal')

    methods = client.methods.all()
    assert methods.count == 1
    iterated = 0
    for method in methods:
        iterated += 1
        assert method.id is not None
        assert method.description is not None
        assert method.image_size1x is not None
    assert iterated == 1
