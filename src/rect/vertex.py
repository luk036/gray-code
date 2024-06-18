from enum import Enum


class VertexType(Enum):
    Corner = 1
    Top = 2
    Bottom = 3
    Left = 4
    Right = 5
    None_ = 6


class Vertex:
    def __init__(self):
        self.north = 0
        self.east = 0
        self.south = 0
        self.west = 0
        self.type_ = VertexType.None_

    def init(self, north: int, east: int, south: int, west: int):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        zeros = (
            (self.north == 0) + (self.south == 0) + (self.west == 0) + (self.east == 0)
        )

        if zeros >= 3 or zeros <= 0:
            self.type_ = VertexType.None_
        elif zeros == 2:
            self.type_ = VertexType.Corner
        elif self.south == 0:
            self.type_ = VertexType.Top
        elif self.north == 0:
            self.type_ = VertexType.Bottom
        elif self.east == 0:
            self.type_ = VertexType.Left
        elif self.west == 0:
            self.type_ = VertexType.Right
