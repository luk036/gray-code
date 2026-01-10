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
    """
    Represents an Edge with various properties.

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
        """Initializes the Edge with provided parameters."""
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
