from dataclasses import dataclass
from enum import Enum


class EdgeDir(Enum):
    HOR = "Hor"
    VER = "Ver"
    NONE = "None"


@dataclass
class Edge:
    dir: EdgeDir = EdgeDir.NONE
    tail: int = 0
    head: int = 0
    prev: int = 0
    next: int = 0
    left: int = 0
    right: int = 0
    wall: int = 0

    def init(
        self,
        dir: EdgeDir,
        tail: int,
        head: int,
        prev: int,
        next: int,
        left: int,
        right: int,
        wall: int,
    ):
        self.dir = dir
        self.tail = tail
        self.head = head
        self.prev = prev
        self.next = next
        self.left = left
        self.right = right
        self.wall = wall
