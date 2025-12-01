from rect.vertex import Vertex, VertexType


def test_vertex_init_corner() -> None:
    vertex = Vertex()
    vertex.init(0, 1, 9, 8)
    assert vertex.type == VertexType.BOTTOM


def test_vertex_init_top() -> None:
    vertex = Vertex()
    vertex.init(0, 1, 0, 8)
    assert vertex.type == VertexType.CORNER


def test_vertex_init_default() -> None:
    vertex = Vertex()
    assert vertex.type == VertexType.NONE
