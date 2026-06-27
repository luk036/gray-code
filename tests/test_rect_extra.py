"""Additional tests for rect module components."""

from rect.edge import Edge, EdgeDir
from rect.rectangle import Rectangle
from rect.rectangulation import (
    Rectangulation,
    RectangulationDirection,
    RectangulationPattern,
    RectangulationType,
)
from rect.vertex import Vertex, VertexType
from rect.wall import Wall


def test_edge_default_init() -> None:
    edge = Edge()
    assert edge.dir == EdgeDir.NONE
    assert edge.tail == 0
    assert edge.head == 0


def test_edge_dir_enum_values() -> None:
    assert EdgeDir.HOR.value == "Horizontal"
    assert EdgeDir.VER.value == "Vertical"
    assert EdgeDir.NONE.value == "None"


def test_rectangle_default_init() -> None:
    rect = Rectangle()
    assert rect.nwest == 0
    assert rect.neast == 0
    assert rect.swest == 0
    assert rect.seast == 0


def test_vertex_type_enum() -> None:
    assert VertexType.CORNER.value == "Corner"
    assert VertexType.TOP.value == "Top"
    assert VertexType.BOTTOM.value == "Bottom"
    assert VertexType.LEFT.value == "Left"
    assert VertexType.RIGHT.value == "Right"
    assert VertexType.NONE.value == "None"


def test_vertex_init_top() -> None:
    v = Vertex()
    v.init(1, 0, 2, 0)  # east=0, west=0 -> CORNER
    assert v.type == VertexType.CORNER


def test_vertex_init_left() -> None:
    v = Vertex()
    v.init(1, 0, 2, 3)  # east=0 -> LEFT
    assert v.type == VertexType.LEFT


def test_vertex_init_right() -> None:
    v = Vertex()
    v.init(1, 2, 3, 0)  # west=0 -> RIGHT
    assert v.type == VertexType.RIGHT


def test_vertex_init_none_three_zeros() -> None:
    v = Vertex()
    v.init(0, 1, 0, 0)  # 3 zeros -> NONE
    assert v.type == VertexType.NONE


def test_vertex_init_none_zero_zeros() -> None:
    v = Vertex()
    v.init(1, 2, 3, 4)  # 0 zeros -> NONE
    assert v.type == VertexType.NONE


def test_wall_default_init() -> None:
    wall = Wall()
    assert wall.first_ == 0
    assert wall.last_ == 0


def test_rectangulation_init() -> None:
    rect = Rectangulation(
        5,
        RectangulationType.GENERIC,
        [RectangulationPattern.WMILL_CLOCKWISE],
    )
    assert rect.n == 5
    assert rect.typ == RectangulationType.GENERIC
    assert rect.patterns == [RectangulationPattern.WMILL_CLOCKWISE]


def test_rectangulation_enum_values() -> None:
    assert str(RectangulationType.BALANCED) == "Balanced"
    assert str(RectangulationType.DIAGONAL) == "Diagonal"
    assert str(RectangulationDirection.LEFT) == "Left"
    assert str(RectangulationDirection.RIGHT) == "Right"


def test_rectangulation_pattern_values() -> None:
    assert "WMillClockwise" in str(RectangulationPattern.WMILL_CLOCKWISE)
    assert "BrickLeftRight" in str(RectangulationPattern.BRICK_LEFTRIGHT)
    assert "HVertical" in str(RectangulationPattern.HVERTICAL)


def test_rectangulation_set_all_vertical() -> None:
    rect = Rectangulation(3, RectangulationType.BALANCED, [])
    assert len(rect.directions) == 4  # 1 + n
    assert rect.directions[1] == RectangulationDirection.LEFT
    assert rect.sizes[1] == 1


def test_rectangulation_init_with_components() -> None:
    rect = Rectangulation(2, RectangulationType.GENERIC, [])
    vertices = [Vertex(), Vertex()]
    walls = [Wall(), Wall()]
    edges = [Edge(), Edge()]
    rectangles = [Rectangle(), Rectangle()]
    rect.init(vertices, walls, edges, rectangles)
    assert len(rect.vertices) == 2
    assert len(rect.walls) == 2
    assert len(rect.edges) == 2
    assert len(rect.rectangles) == 2
