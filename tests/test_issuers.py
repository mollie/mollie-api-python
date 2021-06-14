from mollie.api.objects.issuer import Issuer

from .utils import assert_list_object


def test_get_issuers(client, response):
    """Get all the iDeal issuers via the include querystring parameter."""
    response.get("https://api.mollie.com/v2/methods/ideal?include=issuers", "method_get_ideal_with_includes")

    issuers = client.methods.get("ideal", include="issuers").issuers
    assert_list_object(issuers, Issuer)

    # check a single retrieved issuer
    issuer = next(issuers)
    assert issuer.image_svg == "https://www.mollie.com/external/icons/ideal-issuers/ABNANL2A.svg"
    assert issuer.image_size1x == "https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/ABNANL2A.png"
    assert issuer.image_size2x == "https://www.mollie.com/images/checkout/v2/ideal-issuer-icons/ABNANL2A%402x.png"
    assert issuer.name == "ABN AMRO"
    assert issuer.resource == "issuer"
    assert issuer.id == "ideal_ABNANL2A"
