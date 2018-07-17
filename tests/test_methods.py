
def test_methods_all(client):
    methods = client.methods.all()
    assert methods.count > 0
    iterated = 0
    for method in methods:
        iterated += 1
        assert method.id is not None
        assert method.description is not None
        assert method.image_size1x is not None
    assert iterated == methods.count, 'List count does not match actual iterated methods'
