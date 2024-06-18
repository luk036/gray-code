from rect.rectangle import Rectangle


def test_default():
    rect = Rectangle()
    assert rect.nwest == 0
    assert rect.neast == 0
    assert rect.swest == 0
    assert rect.seast == 0


def test_init():
    rect = Rectangle()
    rect.init(1, 2, 3, 4)
    assert rect.nwest == 4
    assert rect.neast == 1
    assert rect.swest == 3
    assert rect.seast == 2


# To run the tests, use the command: pytest <your_script_name>.py
