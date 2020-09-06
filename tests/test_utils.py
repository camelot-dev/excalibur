from excalibur.utils.file import allowed_filename


def test_allowed_filename():
    assert not allowed_filename("foo.bar")
    assert allowed_filename("foo.pdf")
