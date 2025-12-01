from middle.tree import bitstrings_less_than, bitstrings_equal


def test_bitstrings_less_than() -> None:
    assert bitstrings_less_than([0, 1, 0], [0, 1, 1]) is True
    assert bitstrings_less_than([0, 1, 1], [0, 1, 0]) is False


def test_bitstrings_equal() -> None:
    assert bitstrings_equal([0, 1, 0], [0, 1, 0]) is True
    assert bitstrings_equal([0, 1, 0], [0, 1, 1]) is False
