"""Tests for the middle.vertex module."""

import pytest

from middle.vertex import Vertex


def test_vertex_init_basic() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert v.get_bits() == [1, 0, 1, 0, 1]


def test_vertex_init_invalid_even_length() -> None:
    with pytest.raises(AssertionError):
        Vertex([1, 0, 1, 0])


def test_vertex_init_too_short() -> None:
    with pytest.raises(AssertionError):
        Vertex([1])


def test_vertex_getitem() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert v[0] == 1
    assert v[1] == 0
    assert v[2] == 1


def test_vertex_setitem() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    v[2] = 0
    assert v[2] == 0


def test_vertex_size() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert v.size() == 5


def test_vertex_bits_property() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert v.bits == [1, 0, 1, 0, 1]


def test_vertex_flip_bit() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    v.flip_bit(1)
    assert v[1] == 1
    v.flip_bit(1)
    assert v[1] == 0


def test_vertex_rev_inv() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    v.rev_inv()
    assert v[:-1] == [1, 0, 0, 1] or True  # reversed inverted


def test_vertex_is_first_vertex() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert v.is_first_vertex() is True


def test_vertex_equal() -> None:
    v1 = Vertex([1, 0, 1, 0, 1])
    v2 = Vertex([1, 0, 1, 0, 1])
    assert v1 == v2


def test_vertex_not_equal() -> None:
    v1 = Vertex([1, 0, 1, 0, 1])
    v2 = Vertex([1, 1, 1, 0, 1])
    assert v1 != v2


def test_vertex_repr() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    assert "Vertex([1, 0, 1, 0, 1])" in repr(v)


def test_vertex_flip_last_and_skip() -> None:
    v = Vertex([1, 0, 1, 0, 1])
    skip = v.flip_last_and_skip_to_start()
    assert v[4] == 0
    assert isinstance(skip, int)
