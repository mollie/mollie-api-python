
def test_methods_all(client, response):
    response.get('https://api.mollie.com/v2/methods', 'methods_multiple')

    methods = client.methods.all()
    assert methods.count == 11
    iterated = 0
    iterated_methods_ids = []
    for method in methods:
        iterated += 1
        assert method.id is not None
        iterated_methods_ids.append(method.id)
        assert method.description is not None
        assert method.image_size1x is not None
    assert iterated == 11
    assert len(set(iterated_methods_ids)) == 11, 'Unexpected number of unique methods'
