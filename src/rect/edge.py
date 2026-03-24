import doctest
from dataclasses import dataclass
from enum import Enum


class EdgeDir(Enum):
    """Enum representing the direction of an edge."""

    HOR = "Horizontal"
    VER = "Vertical"
    NONE = "None"


@dataclass
class Edge:
    """Represents an edge in a rectangulation.

    An edge is a line segment connecting two vertices in the rectangulation.
    It has a direction (horizontal, vertical, or none), endpoints (tail and head),
    references to previous and next edges, left and right adjacent edges, and
    an associated wall.

    Attributes:
        dir: The direction of the edge (horizontal, vertical, or none).
        tail: The starting vertex index of the edge.
        head: The ending vertex index of the edge.
        prev: The index of the previous edge in the sequence.
        next: The index of the next edge in the sequence.
        left: The index of the edge to the left of this edge.
        right: The index of the edge to the right of this edge.
        wall: The index of the wall associated with this edge.

    Examples:
        >>> edge = Edge()
        >>> edge.init(EdgeDir.HOR, 1, 2, 3, 4, 5, 6, 7)
        >>> edge.dir == EdgeDir.HOR
        True
        >>> edge.tail == 1
        True
    """

    def __init__(self):
        self.init(EdgeDir.NONE, 0, 0, 0, 0, 0, 0, 0)

    def init(self, dir, tail, head, prev, next, left, right, wall):
        """Initialize the Edge with provided parameters.

        Args:
            dir: The direction of the edge (EdgeDir enum).
            tail: The starting vertex index of the edge.
            head: The ending vertex index of the edge.
            prev: The index of the previous edge in the sequence.
            next: The index of the next edge in the sequence.
            left: The index of the edge to the left of this edge.
            right: The index of the edge to the right of this edge.
            wall: The index of the wall associated with this edge.
        """
        self.dir = dir
        self.tail = tail
        self.head = head
        self.prev = prev
        self.next = next
        self.left = left
        self.right = right
        self.wall = wall


if __name__ == "__main__":
    doctest.testmod()
