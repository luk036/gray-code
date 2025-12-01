from rect.rectangle import Rectangle


def test_rectangle_init() -> None:
    """Test the initialization of Rectangle."""
    rect = Rectangle()
    rect.init(10, 20, 30, 40)
    assert rect.nwest == 40, "The northwest coordinate was not set correctly."
    assert rect.neast == 10, "The northeast coordinate was not set correctly."
    assert rect.swest == 30, "The southwest coordinate was not set correctly."
    assert rect.seast == 20, "The southeast coordinate was not set correctly."
