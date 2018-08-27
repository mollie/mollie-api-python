from mollie.api.objects.issuer import Issuer

from .utils import assert_list_object


def test_get_issuers(client, response):
    """Get all the iDeal issuers via the include querystring parameter."""
    response.get('https://api.mollie.com/v2/methods/ideal?include=issuers', 'method_get_ideal_with_includes')

    issuers = client.methods.get('ideal', include='issuers').issuers
    assert_list_object(issuers, Issuer)

    # check the last issuer
    assert issuer.image_svg == 'https://www.mollie.com/external/icons/ideal-issuers/FVLBNL22.svg'
    assert issuer.image_size1x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/FVLBNL22.png'
    assert issuer.image_size2x == 'https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/FVLBNL22.png'
    assert issuer.name == 'van Lanschot'
    assert issuer.resource == 'issuer'
    assert issuer.id == 'ideal_FVLBNL22'
