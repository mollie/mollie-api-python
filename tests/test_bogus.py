import Mollie

def test_bogus():
    mollie = Mollie.API.Client()
    assert mollie
