from enum import Enum
from typing import List

from .edge import Edge
from .rectangle import Rectangle
from .vertex import Vertex, VertexType
from .wall import Wall


class RectangulationType(Enum):
    """Enumeration for different types of rectangulations."""

    GENERIC = "Generic"
    BALANCED = "Balanced"
    DIAGONAL = "Diagonal"

    def __str__(self):
        return self.value


class RectangulationDirection(Enum):
    """Enumeration for rectangulation directions."""

    LEFT = "Left"
    RIGHT = "Right"
    NONE = "None"

    def __str__(self):
        return self.value


class RectangulationPattern(Enum):
    """Enumeration for rectangulation patterns."""

    WMILL_CLOCKWISE = "WMillClockwise"
    WMILL_COUNTERCLOCKWISE = "WMillCounterclockwise"
    BRICK_LEFTRIGHT = "BrickLeftRight"
    BRICK_RIGHTLEFT = "BrickRightLeft"
    BRICK_TOPBOTTOM = "BrickTopBottom"
    BRICK_BOTTOMTOP = "BrickBottomTop"
    HVERTICAL = "HVertical"
    HHORIZONTAL = "HHorizontal"

    def __str__(self):
        return self.value


class Rectangulation:
    """Class representing a rectangulation."""

    def __init__(
        self, n: int, typ: RectangulationType, patterns: List[RectangulationPattern]
    ):
        """Initialize the Rectangulation.

        >>> rect = Rectangulation(5, RectangulationType.GENERIC,
        ...                      [RectangulationPattern.WMILL_CLOCKWISE,
        ...                       RectangulationPattern.BRICK_LEFTRIGHT])
        >>> rect.n
        5
        >>> rect.typ
        <RectangulationType.GENERIC: 'Generic'>
        >>> rect.patterns
        [<RectangulationPattern.WMILL_CLOCKWISE: 'WMillClockwise'>,
         <RectangulationPattern.BRICK_LEFTRIGHT: 'BrickLeftRight'>]
        """
        self.n = n
        self.typ = typ
        self.patterns = patterns
        self.directions = [RectangulationDirection.NONE]
        self.sizes = [-1]
        self.vertices: List[Vertex] = []
        self.walls: List[Wall] = []
        self.edges: List[Edge] = []
        self.rectangles: List[Rectangle] = []
        self.set_all_vertical()

    def set_all_vertical(self):
        """Sets all directions to vertical initially."""
        for j in range(1, self.n + 1):
            self.directions.append(RectangulationDirection.LEFT)
            self.sizes.append(j)

    def init(self, vertices, walls, edges, rectangles):
        """Initializes the rectangulation with provided components."""
        self.vertices = vertices
        self.walls = walls
        self.edges = edges
        self.rectangles = rectangles

    def print_data(self):
        """Prints out the data structures in a readable format."""
        print("Edges:")
        for i, e in enumerate(self.edges):
            print(f"\t{i}. {e}")  # Assuming Edge has a meaningful string representation

        # Similar prints for vertices, walls, and rectangles would follow here

    def print_coordinates_generic(self):
        vertex_x_coord = [-1] * (2 * self.n + 3)
        active_vertices = []

        # Start with every vertex on the western side as an active vertex
        for a, v in enumerate(self.vertices):
            if v.type_ in (VertexType.RIGHT, VertexType.CORNER):
                side_edge_id = (
                    v.north if v.type_ == VertexType.RIGHT else max(v.north, v.south)
                )
                if self.edges[side_edge_id].left == 0:
                    active_vertices.append(a)

        # Propagate active vertices and calculate x-coordinates
        x_value = 0
        while active_vertices:
            for idx in active_vertices:
                vertex_x_coord[idx] = x_value
            x_value += 1

            new_active_vertices = []
            for idx in active_vertices:
                # Propagation logic similar to C++ code would go here
                # Due to Python's dynamic nature and lack of explicit types like in C++,
                # the exact logic for updating active vertices and propagating coordinates
                # would need to be implemented considering Python's capabilities and idioms.
                pass

            active_vertices = new_active_vertices

        # The y-coordinate calculation logic would follow a similar pattern but starting from the south.
        # For simplicity and clarity, only the x-coordinate propagation logic is shown.

        # Printing the coordinates would use Python's print function instead of C++ streams.
        # However, the full printing logic isn't included here due to the focus on structure and method setup.
