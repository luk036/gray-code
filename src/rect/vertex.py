from enum import Enum


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
    """
    Class for the Vertex.

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
        """
        Method to initialize the vertex with given coordinates and determine its type.
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
