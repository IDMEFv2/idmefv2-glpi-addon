from .process import NullProcessor

def test_null():
    message = {'foo': 1, 'bar': 2}
    p = NullProcessor()
    assert p.process(message) is message
