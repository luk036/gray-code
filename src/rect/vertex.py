from enum import Enum


class VertexType(Enum):
    """Enum to represent the type of a vertex."""

    CORNER = "Corner"
    TOP = "Top"
    BOTTOM = "Bottom"
    LEFT = "Left"
    RIGHT = "Right"
    NONE = "None"


class Vertex:
    """Represents a vertex in a rectangulation.

    A vertex has four boundary indices (north, east, south, west) that define
    its position relative to walls in the rectangulation. The vertex type
    is determined based on which boundaries are at the origin (0).

    Attributes:
        north: The index of the north wall (0 if on southern boundary).
        east: The index of the east wall (0 if on western boundary).
        south: The index of the south wall (0 if on northern boundary).
        west: The index of the west wall (0 if on eastern boundary).
        type: The type of the vertex (Corner, Top, Bottom, Left, Right, or None).

    Examples:
        >>> vertex = Vertex()
        >>> vertex.init(0, 1, 9, 8)
        >>> vertex.type
        <VertexType.BOTTOM: 'Bottom'>

        >>> vertex = Vertex()
        >>> vertex.init(0, 1, 0, 8)
        >>> vertex.type
        <VertexType.CORNER: 'Corner'>

        >>> vertex = Vertex()
        >>> vertex.type
        <VertexType.NONE: 'None'>
    """

    def __init__(self):
        """Constructor for Vertex with default type None."""
        self.north = 0
        self.east = 0
        self.south = 0
        self.west = 0
        self.type = VertexType.NONE

    def init(self, north, east, south, west):
        """Initialize the vertex with given coordinates and determine its type.

        Args:
            north: The index of the north wall (0 if on southern boundary).
            east: The index of the east wall (0 if on western boundary).
            south: The index of the south wall (0 if on northern boundary).
            west: The index of the west wall (0 if on eastern boundary).
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        zeros = (
            (self.north == 0) + (self.south == 0) + (self.west == 0) + (self.east == 0)
        )
        if 3 <= zeros or zeros == 0:
            self.type = VertexType.NONE
        elif zeros == 2:
            self.type = VertexType.CORNER
        elif self.south == 0:
            self.type = VertexType.TOP
        elif self.north == 0:
            self.type = VertexType.BOTTOM
        elif self.east == 0:
            self.type = VertexType.LEFT
        elif self.west == 0:
            self.type = VertexType.RIGHT
        else:
            raise AssertionError(
                "Unexpected condition encountered in determining vertex type."
            )
