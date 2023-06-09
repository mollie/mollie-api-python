import pickle

from mollie.api.error import ResponseError


def test_pickle_response_error():
    error = ResponseError(
        {"detail": "some-detail", "status": "test-status", "field": "test-field"},
        idempotency_key="test-idempotency-key",
    )
    pickled = pickle.dumps(error)
    unpickled = pickle.loads(pickled)

    assert isinstance(unpickled, ResponseError)
    assert str(unpickled) == "some-detail"
    assert unpickled.status == "test-status"
    assert unpickled.field == "test-field"
    assert unpickled.idempotency_key == "test-idempotency-key"
