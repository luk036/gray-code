from middle.tree import bitstrings_less_than, bitstrings_equal


def test_bitstrings_less_than():
    assert bitstrings_less_than([0, 1, 0], [0, 1, 1]) == True
    assert bitstrings_less_than([0, 1, 1], [0, 1, 0]) == False


def test_bitstrings_equal():
    assert bitstrings_equal([0, 1, 0], [0, 1, 0]) == True
    assert bitstrings_equal([0, 1, 0], [0, 1, 1]) == False
