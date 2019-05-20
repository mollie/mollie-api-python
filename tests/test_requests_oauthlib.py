def test_requests_oauthlib_is_installed():
    from oauthlib.oauth2 import BackendApplicationClient
    _ = BackendApplicationClient  # Silence pyflakes
