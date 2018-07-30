
def test_get_issuers(client, response):
    """Get all the iDeal issuers via the include querystring parameter."""
    response.get('https://api.mollie.com/v2/methods/ideal?include=issuers', 'method_get_ideal_with_includes')

    issuers = client.methods.get('ideal', include='issuers').issuers
    assert issuers.__class__.__name__ == 'List'
    assert len(issuers) == 11

    iterated = 0
    iterated_issuer_ids = []
    for issuer in issuers:
        assert issuer.__class__.__name__ == 'Issuer'
        iterated += 1
        assert issuer.id is not None
        iterated_issuer_ids.append(issuer.id)
    assert iterated == len(issuers), 'Unexpected amount of issuers retrieved'
    assert len(set(iterated_issuer_ids)) == len(issuers), 'Unexpected number of unique issuers'

    iterated = 0
    for issuer in issuers:
        if iterated == 1:
            break
        assert issuer.image_size1x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/ABNANL2A.png'
        assert issuer.image_size2x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/ABNANL2A.png'
        assert issuer.name == 'ABN AMRO'
        assert issuer.resource == 'issuer'
        assert issuer.id == 'ideal_ABNANL2A'
        iterated += 1
