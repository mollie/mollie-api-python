from mollie.api.objects.issuer import Issuer
from mollie.api.objects.list import List


def test_get_issuers(client, response):
    """Get all the iDeal issuers via the include querystring parameter."""
    response.get('https://api.mollie.com/v2/methods/ideal?include=issuers', 'method_get_ideal_with_includes')

    issuers = client.methods.get('ideal', include='issuers').issuers
    assert isinstance(issuers, List)

    iterated = 0
    iterated_issuer_ids = []
    for issuer in issuers:
        assert isinstance(issuer, Issuer)
        assert issuer.id is not None
        iterated += 1
        iterated_issuer_ids.append(issuer.id)
    assert iterated == len(issuers), 'Unexpected amount of issuers retrieved'
    assert len(set(iterated_issuer_ids)) == len(issuers), 'Unexpected number of unique issuers'

    # check the last issuer
    assert issuer.image_svg == 'https://www.mollie.com/external/icons/ideal-issuers/FVLBNL22.svg'
    assert issuer.image_size1x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/FVLBNL22.png'
    assert issuer.image_size2x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/FVLBNL22.png'
    assert issuer.name == 'van Lanschot'
    assert issuer.resource == 'issuer'
    assert issuer.id == 'ideal_FVLBNL22'
