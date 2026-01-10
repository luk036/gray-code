import getopt
import sys
from enum import Enum, auto
from typing import List


class EdgeDir(Enum):
    Hor = auto()
    Ver = auto()
    None_ = auto()


class VertexType(Enum):
    corner = auto()
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()
    None_ = auto()


class RectangulationType(Enum):
    generic = auto()
    baligned = auto()
    diagonal = auto()


class RectangulationDirection(Enum):
    left = auto()
    right = auto()
    None_ = auto()


class RectangulationPattern(Enum):
    wmill_clockwise = auto()
    wmill_counterclockwise = auto()
    brick_leftright = auto()
    brick_rightleft = auto()
    brick_topbottom = auto()
    brick_bottomtop = auto()
    H_vertical = auto()
    H_horizontal = auto()


class Edge:
    def __init__(self):
        self.dir_: EdgeDir = EdgeDir.None_
        self.tail_: int = 0
        self.head_: int = 0
        self.prev_: int = 0
        self.next_: int = 0
        self.left_: int = 0
        self.right_: int = 0
        self.wall_: int = 0

    def init(
        self,
        dir_: EdgeDir,
        tail: int,
        head: int,
        prev: int,
        next_: int,
        left: int,
        right: int,
        wall: int,
    ):
        self.dir_ = dir_
        self.tail_ = tail
        self.head_ = head
        self.left_ = left
        self.right_ = right
        self.wall_ = wall
        self.prev_ = prev
        self.next_ = next_


class Vertex:
    def __init__(self):
        self.north_: int = 0
        self.east_: int = 0
        self.south_: int = 0
        self.west_: int = 0
        self.type_: VertexType = VertexType.None_

    def init(self, north: int, east: int, south: int, west: int):
        self.north_ = north
        self.east_ = east
        self.south_ = south
        self.west_ = west
        zeros = (
            int(self.north_ == 0)
            + int(self.south_ == 0)
            + int(self.west_ == 0)
            + int(self.east_ == 0)
        )
        if zeros >= 3 or zeros <= 0:
            self.type_ = VertexType.None_
        elif zeros == 2:
            self.type_ = VertexType.corner
        elif self.south_ == 0:
            self.type_ = VertexType.top
        elif self.north_ == 0:
            self.type_ = VertexType.bottom
        elif self.east_ == 0:
            self.type_ = VertexType.left
        elif self.west_ == 0:
            self.type_ = VertexType.right


class Wall:
    def __init__(self):
        self.first_: int = 0
        self.last_: int = 0

    def init(self, first: int, last: int):
        self.first_ = first
        self.last_ = last


class Rectangle:
    def __init__(self):
        self.nwest_: int = 0
        self.neast_: int = 0
        self.swest_: int = 0
        self.seast_: int = 0

    def init(self, neast: int, seast: int, swest: int, nwest: int):
        self.nwest_ = nwest
        self.neast_ = neast
        self.swest_ = swest
        self.seast_ = seast


class Rectangulation:
    def __init__(
        self, n: int, type_: RectangulationType, patterns: List[RectangulationPattern]
    ):
        self.n_ = n
        self.type_ = type_
        self.patterns_ = patterns
        self.o_: List[RectangulationDirection] = []
        self.s_: List[int] = []
        self.vertices_: List[Vertex] = []
        self.walls_: List[Wall] = []
        self.edges_: List[Edge] = []
        self.rectangles_: List[Rectangle] = []
        self.set_all_vertical()
        self.o_.append(RectangulationDirection.None_)
        self.s_.append(-1)
        for j in range(1, n + 1):
            self.o_.append(RectangulationDirection.left)
            self.s_.append(j)

    def set_all_vertical(self):
        edges = [Edge() for _ in range(3 * self.n_ + 2)]
        vertices = [Vertex() for _ in range(2 * self.n_ + 3)]
        rectangles = [Rectangle() for _ in range(self.n_ + 1)]
        walls = [Wall() for _ in range(self.n_ + 4)]

        edges[0].init(EdgeDir.None_, 0, 0, 0, 0, 0, 0, 0)
        vertices[0].init(0, 0, 0, 0)
        rectangles[0].init(0, 0, 0, 0)
        walls[0].init(0, 0)

        for i in range(1, self.n_):
            edges[i].init(EdgeDir.Hor, i, i + 1, i - 1, i + 1, 0, i, 1)
        edges[self.n_].init(
            EdgeDir.Hor, self.n_, self.n_ + 1, self.n_ - 1, 0, 0, self.n_, 1
        )

        vertices[1].init(0, 1, 2 * self.n_ + 1, 0)
        vertices[self.n_ + 1].init(0, 0, 3 * self.n_ + 1, self.n_)
        for i in range(2, self.n_ + 1):
            vertices[i].init(0, i, 2 * self.n_ + i, i - 1)

        for i in range(2, self.n_):
            edges[self.n_ + i].init(
                EdgeDir.Hor,
                self.n_ + i + 1,
                self.n_ + i + 2,
                self.n_ + i - 1,
                self.n_ + i + 1,
                i,
                0,
                2,
            )
        edges[self.n_ + 1].init(
            EdgeDir.Hor, self.n_ + 2, self.n_ + 3, 0, self.n_ + 2, 1, 0, 2
        )
        edges[2 * self.n_].init(
            EdgeDir.Hor,
            2 * self.n_ + 1,
            2 * self.n_ + 2,
            2 * self.n_ - 1,
            0,
            self.n_,
            0,
            2,
        )

        vertices[self.n_ + 2].init(2 * self.n_ + 1, self.n_ + 1, 0, 0)
        vertices[2 * self.n_ + 2].init(3 * self.n_ + 1, 0, 0, 2 * self.n_)
        for i in range(2, self.n_ + 1):
            vertices[self.n_ + i + 1].init(
                2 * self.n_ + i, self.n_ + i, 0, self.n_ + i - 1
            )

        edges[2 * self.n_ + 1].init(EdgeDir.Ver, self.n_ + 2, 1, 0, 0, 0, 1, 3)
        edges[3 * self.n_ + 1].init(
            EdgeDir.Ver, 2 * self.n_ + 2, self.n_ + 1, 0, 0, self.n_, 0, self.n_ + 3
        )
        for i in range(2, self.n_ + 1):
            edges[2 * self.n_ + i].init(
                EdgeDir.Ver, self.n_ + i + 1, i, 0, 0, i - 1, i, i + 2
            )

        for i in range(1, self.n_ + 1):
            rectangles[i].init(i + 1, self.n_ + i + 2, self.n_ + i + 1, i)

        walls[1].init(1, self.n_ + 1)
        walls[2].init(self.n_ + 2, 2 * self.n_ + 2)
        for i in range(1, self.n_ + 2):
            walls[i + 2].init(self.n_ + i + 1, i)

        self.init(vertices, walls, edges, rectangles)

    def init(
        self,
        vertices: List[Vertex],
        walls: List[Wall],
        edges: List[Edge],
        rectangles: List[Rectangle],
    ):
        self.edges_ = edges
        self.vertices_ = vertices
        self.walls_ = walls
        self.rectangles_ = rectangles

    def print_data(self):
        print("edges:")
        for i, e in enumerate(self.edges_):
            dir_str = (
                "Hor "
                if e.dir_ == EdgeDir.Hor
                else "Ver "
                if e.dir_ == EdgeDir.Ver
                else "None "
            )
            print(
                f"\t{i}. {dir_str}{e.tail_} {e.head_} {e.prev_} {e.next_} {e.left_} {e.right_} {e.wall_}"
            )

        print("vertices:")
        for i, v in enumerate(self.vertices_):
            type_str = (
                "None"
                if v.type_ == VertexType.None_
                else (
                    "corner"
                    if v.type_ == VertexType.corner
                    else (
                        "bottom"
                        if v.type_ == VertexType.bottom
                        else (
                            "top"
                            if v.type_ == VertexType.top
                            else "left"
                            if v.type_ == VertexType.left
                            else "right"
                        )
                    )
                )
            )
            print(f"\t{i}. {v.north_} {v.east_} {v.south_} {v.west_} {type_str}")

        print("walls:")
        for i, w in enumerate(self.walls_):
            print(f"\t{i}. {w.first_} {w.last_}")

        print("rectangles:")
        for i, r in enumerate(self.rectangles_):
            print(f"\t{i}. {r.neast_} {r.seast_} {r.swest_} {r.nwest_}")

    def print_coordinates(self):
        if self.type_ == RectangulationType.generic:
            self.print_coordinates_generic()
        elif self.type_ in [RectangulationType.diagonal, RectangulationType.baligned]:
            self.print_coordinates_diagonal()

    def print_coordinates_generic(self):
        active_vertices = []
        vertex_x_coord = [-1] * (2 * self.n_ + 3)

        for a, v in enumerate(self.vertices_):
            side_edge_id = 0
            if v.type_ == VertexType.right:
                side_edge_id = v.north_
            elif v.type_ == VertexType.corner:
                side_edge_id = max(v.north_, v.south_)
            else:
                continue

            if self.edges_[side_edge_id].left_ == 0:
                active_vertices.append(a)

        x_value = 0
        while active_vertices:
            for idx in active_vertices:
                vertex_x_coord[idx] = x_value
            x_value += 1

            new_active_vertices = []
            for idx in active_vertices:
                if self.vertices_[idx].east_ != 0:
                    alpha = self.vertices_[idx].east_
                    new_active_vertices.append(self.edges_[alpha].head_)

            new_active_vertices_copy = new_active_vertices.copy()
            for idx in new_active_vertices_copy:
                propagate_from = self.vertices_[idx]
                while propagate_from.north_ != 0:
                    e = self.edges_[propagate_from.north_]
                    propagate_from = self.vertices_[e.head_]
                    new_active_vertices.append(e.head_)

                propagate_from = self.vertices_[idx]
                while propagate_from.south_ != 0:
                    e = self.edges_[propagate_from.south_]
                    propagate_from = self.vertices_[e.tail_]
                    new_active_vertices.append(e.tail_)

            active_vertices = new_active_vertices

        active_vertices = []
        vertex_y_coord = [-1] * (2 * self.n_ + 3)

        for a, v in enumerate(self.vertices_):
            side_edge_id = 0
            if v.type_ == VertexType.top:
                side_edge_id = v.east_
            elif v.type_ == VertexType.corner:
                side_edge_id = max(v.east_, v.west_)
            else:
                continue

            if self.edges_[side_edge_id].right_ == 0:
                active_vertices.append(a)

        y_value = 0
        while active_vertices:
            for idx in active_vertices:
                vertex_y_coord[idx] = y_value
            y_value += 1

            new_active_vertices = []
            for idx in active_vertices:
                if self.vertices_[idx].north_ != 0:
                    alpha = self.vertices_[idx].north_
                    new_active_vertices.append(self.edges_[alpha].head_)

            new_active_vertices_copy = new_active_vertices.copy()
            for idx in new_active_vertices_copy:
                propagate_from = self.vertices_[idx]
                while propagate_from.east_ != 0:
                    e = self.edges_[propagate_from.east_]
                    propagate_from = self.vertices_[e.head_]
                    new_active_vertices.append(e.head_)

                propagate_from = self.vertices_[idx]
                while propagate_from.west_ != 0:
                    e = self.edges_[propagate_from.west_]
                    propagate_from = self.vertices_[e.tail_]
                    new_active_vertices.append(e.tail_)

            active_vertices = new_active_vertices

        output = []
        is_first = True
        for r in self.rectangles_:
            if is_first:
                is_first = False
                continue
            swest_x = vertex_x_coord[r.swest_]
            swest_y = vertex_y_coord[r.swest_]
            neast_x = vertex_x_coord[r.neast_]
            neast_y = vertex_y_coord[r.neast_]
            output.append(f"{swest_x} {swest_y} {neast_x} {neast_y}")

        print(" | ".join(output))

    def DFS_BL(
        self,
        vertex_id: int,
        val: int,
        vertex_x_coord: List[int],
        vertex_y_coord: List[int],
    ):
        v = self.vertices_[vertex_id]
        top_vertex = self.edges_[v.north_].head_
        right_vertex = self.edges_[v.east_].head_

        if self.vertices_[top_vertex].type_ in [
            VertexType.corner,
            VertexType.bottom,
            VertexType.left,
        ]:
            vertex_x_coord[vertex_id] = val
            val += 1
        else:
            self.DFS_BL(top_vertex, val, vertex_x_coord, vertex_y_coord)
            vertex_x_coord[vertex_id] = vertex_x_coord[top_vertex]

        if self.vertices_[right_vertex].type_ in [
            VertexType.corner,
            VertexType.bottom,
            VertexType.left,
        ]:
            vertex_y_coord[vertex_id] = self.n_ - val
            val += 1
        else:
            self.DFS_BL(right_vertex, val, vertex_x_coord, vertex_y_coord)
            vertex_y_coord[vertex_id] = vertex_y_coord[right_vertex]

    def DFS_TR(
        self,
        vertex_id: int,
        val: int,
        vertex_x_coord: List[int],
        vertex_y_coord: List[int],
    ):
        v = self.vertices_[vertex_id]
        left_vertex = self.edges_[v.west_].tail_
        bottom_vertex = self.edges_[v.south_].tail_

        if self.vertices_[bottom_vertex].type_ in [
            VertexType.corner,
            VertexType.right,
            VertexType.top,
        ]:
            vertex_x_coord[vertex_id] = self.n_ - val
            val += 1
        else:
            self.DFS_TR(bottom_vertex, val, vertex_x_coord, vertex_y_coord)
            vertex_x_coord[vertex_id] = vertex_x_coord[bottom_vertex]

        if self.vertices_[left_vertex].type_ in [
            VertexType.corner,
            VertexType.right,
            VertexType.top,
        ]:
            vertex_y_coord[vertex_id] = val
            val += 1
        else:
            self.DFS_TR(left_vertex, val, vertex_x_coord, vertex_y_coord)
            vertex_y_coord[vertex_id] = vertex_y_coord[left_vertex]

    def print_coordinates_diagonal(self):
        vertex_x_coord = [-1] * (2 * self.n_ + 3)
        vertex_y_coord = [-1] * (2 * self.n_ + 3)

        BL = -1
        TR = -1
        for i in range(1, 2 * self.n_ + 3):
            v = self.vertices_[i]
            if v.north_ == 0 and v.east_ == 0 and v.type_ == VertexType.corner:
                TR = i
            elif v.south_ == 0 and v.west_ == 0 and v.type_ == VertexType.corner:
                BL = i

        assert BL != -1 and TR != -1

        val = 0
        self.DFS_BL(BL, val, vertex_x_coord, vertex_y_coord)
        val = 0
        self.DFS_TR(TR, val, vertex_x_coord, vertex_y_coord)

        output = []
        is_first = True
        for r in self.rectangles_:
            if is_first:
                is_first = False
                continue
            swest_x = vertex_x_coord[r.swest_]
            swest_y = vertex_y_coord[r.swest_]
            neast_x = vertex_x_coord[r.neast_]
            neast_y = vertex_y_coord[r.neast_]
            output.append(f"{swest_x} {swest_y} {neast_x} {neast_y}")

        print(" | ".join(output))

    def next(self) -> bool:
        j = self.s_[self.n_]
        if (j == 1) or ((self.n_ == 2) and (self.type_ == RectangulationType.baligned)):
            return False

        if self.type_ == RectangulationType.generic:
            self.next_generic(j, self.o_[j])
            while self.contains_pattern(j):
                self.next_generic(j, self.o_[j])
        elif self.type_ == RectangulationType.diagonal:
            self.next_diagonal(j, self.o_[j])
            while self.contains_pattern(j):
                self.next_diagonal(j, self.o_[j])
        elif self.type_ == RectangulationType.baligned:
            self.next_baligned(j, self.o_[j])
            while self.contains_pattern(j):
                self.next_baligned(j, self.o_[j])

        self.s_[self.n_] = self.n_

        if (
            (self.type_ == RectangulationType.baligned)
            and (self.o_[j - 1] == RectangulationDirection.left)
            and self.is_bottom_based(j - 1)
        ):
            self.o_[j - 1] = RectangulationDirection.right
            self.s_[j - 1] = self.s_[j - 2]
            self.s_[j - 2] = j - 2

        if (self.o_[j] == RectangulationDirection.left) and self.is_bottom_based(j):
            self.o_[j] = RectangulationDirection.right
            self.s_[j] = self.s_[j - 1]
            self.s_[j - 1] = j - 1

        if (
            (self.type_ == RectangulationType.baligned)
            and (self.o_[j - 1] == RectangulationDirection.right)
            and self.is_right_based(j - 1)
        ):
            self.o_[j - 1] = RectangulationDirection.left
            self.s_[j - 1] = self.s_[j - 2]
            self.s_[j - 2] = j - 2

        if (self.o_[j] == RectangulationDirection.right) and self.is_right_based(j):
            self.o_[j] = RectangulationDirection.left
            self.s_[j] = self.s_[j - 1]
            self.s_[j - 1] = j - 1

        return True

    def is_bottom_based(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        alpha = self.vertices_[a].south_
        b = self.rectangles_[j].swest_

        if self.edges_[alpha].left_ == 0:
            return True

        if (
            self.type_ == RectangulationType.baligned
            and a == self.rectangles_[j - 1].neast_
            and b == self.rectangles_[j - 1].seast_
        ):
            c = self.rectangles_[j - 1].nwest_
            gamma = self.vertices_[c].south_
            if self.edges_[gamma].left_ == 0:
                return True

        return False

    def is_right_based(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        alpha = self.vertices_[a].east_
        b = self.rectangles_[j].neast_

        if self.edges_[alpha].left_ == 0:
            return True

        if (
            self.type_ == RectangulationType.baligned
            and a == self.rectangles_[j - 1].swest_
            and b == self.rectangles_[j - 1].seast_
        ):
            c = self.rectangles_[j].nwest_
            gamma = self.vertices_[c].east_
            if self.edges_[gamma].left_ == 0:
                return True

        return False

    def remHead(self, beta: int):
        alpha = self.edges_[beta].prev_
        gamma = self.edges_[beta].next_
        a = self.edges_[beta].tail_

        if alpha != 0:
            self.edges_[alpha].next_ = gamma
        if gamma != 0:
            self.edges_[gamma].prev_ = alpha
        self.edges_[gamma].tail_ = a

        if self.edges_[beta].dir_ == EdgeDir.Hor:
            self.vertices_[a].east_ = gamma
        else:
            self.vertices_[a].north_ = gamma

        x = self.edges_[beta].wall_
        if self.edges_[beta].head_ == self.walls_[x].last_:
            self.walls_[x].last_ = a

    def remTail(self, beta: int):
        alpha = self.edges_[beta].prev_
        gamma = self.edges_[beta].next_
        a = self.edges_[beta].head_

        if alpha != 0:
            self.edges_[alpha].next_ = gamma
        if gamma != 0:
            self.edges_[gamma].prev_ = alpha
        self.edges_[alpha].head_ = a

        if self.edges_[beta].dir_ == EdgeDir.Hor:
            self.vertices_[a].west_ = alpha
        else:
            self.vertices_[a].south_ = alpha

        x = self.edges_[beta].wall_
        if self.edges_[beta].tail_ == self.walls_[x].first_:
            self.walls_[x].first_ = a

    def insBefore(self, beta: int, a: int, gamma: int):
        alpha = self.edges_[gamma].prev_
        b = self.edges_[gamma].tail_

        self.edges_[beta].tail_ = b
        self.edges_[beta].head_ = a
        self.edges_[beta].prev_ = alpha
        self.edges_[beta].next_ = gamma
        self.edges_[gamma].tail_ = a
        self.edges_[gamma].prev_ = beta

        if alpha != 0:
            self.edges_[alpha].next_ = beta

        if self.edges_[gamma].dir_ == EdgeDir.Hor:
            self.edges_[beta].dir_ = EdgeDir.Hor
            self.vertices_[a].west_ = beta
            self.vertices_[a].east_ = gamma
            self.vertices_[b].east_ = beta
        else:
            self.edges_[beta].dir_ = EdgeDir.Ver
            self.vertices_[a].south_ = beta
            self.vertices_[a].north_ = gamma
            self.vertices_[b].north_ = beta

        self.edges_[beta].wall_ = self.edges_[gamma].wall_

    def insAfter(self, alpha: int, a: int, beta: int):
        gamma = self.edges_[alpha].next_
        b = self.edges_[alpha].head_

        self.edges_[beta].tail_ = a
        self.edges_[beta].head_ = b
        self.edges_[beta].prev_ = alpha
        self.edges_[beta].next_ = gamma
        self.edges_[alpha].head_ = a
        self.edges_[alpha].next_ = beta

        if gamma != 0:
            self.edges_[gamma].prev_ = beta

        if self.edges_[alpha].dir_ == EdgeDir.Hor:
            self.edges_[beta].dir_ = EdgeDir.Hor
            self.vertices_[a].west_ = alpha
            self.vertices_[a].east_ = beta
            self.vertices_[b].west_ = beta
        else:
            self.edges_[beta].dir_ = EdgeDir.Ver
            self.vertices_[a].south_ = alpha
            self.vertices_[a].north_ = beta
            self.vertices_[b].south_ = beta

        self.edges_[beta].wall_ = self.edges_[alpha].wall_

    def Wjump_hor(self, j: int, dir_: RectangulationDirection, alpha: int):
        if dir_ == RectangulationDirection.left:
            a = self.rectangles_[j].nwest_
            beta = self.vertices_[a].west_
            assert alpha == self.edges_[beta].prev_
            k = self.edges_[alpha].left_

            self.remHead(beta)
            self.insAfter(alpha, a, beta)
            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = j
        else:
            a = self.rectangles_[j].nwest_
            beta = self.vertices_[a].east_
            assert alpha == self.edges_[beta].next_
            k = self.edges_[alpha].left_
            alpha_prime = self.edges_[beta].prev_
            l = self.edges_[alpha_prime].right_

            self.remTail(beta)
            self.insBefore(beta, a, alpha)
            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = l

    def Wjump_ver(self, j: int, dir_: RectangulationDirection, alpha: int):
        if dir_ == RectangulationDirection.right:
            a = self.rectangles_[j].nwest_
            beta = self.vertices_[a].north_
            assert alpha == self.edges_[beta].next_
            k = self.edges_[alpha].left_

            self.remTail(beta)
            self.insBefore(beta, a, alpha)
            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = j
        else:
            a = self.rectangles_[j].nwest_
            beta = self.vertices_[a].south_
            assert alpha == self.edges_[beta].prev_
            k = self.edges_[alpha].left_
            alpha_prime = self.edges_[beta].next_
            l = self.edges_[alpha_prime].right_

            self.remHead(beta)
            self.insAfter(alpha, a, beta)
            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = l

    def Sjump(self, j: int, d: RectangulationDirection, alpha: int):
        if d == RectangulationDirection.left:
            a = self.rectangles_[j].nwest_
            b = self.rectangles_[j].swest_
            c = self.rectangles_[j].neast_
            alpha_prime = self.vertices_[a].west_
            beta = self.vertices_[a].east_
            beta_prime = self.vertices_[b].west_
            gamma = self.vertices_[c].south_
            delta = self.vertices_[a].south_
            c_prime = self.edges_[beta_prime].tail_
            k = self.edges_[alpha].left_
            l = self.edges_[gamma].right_
            x = self.edges_[delta].wall_

            self.remTail(beta)
            self.remHead(beta_prime)
            self.insBefore(beta, a, alpha)
            self.insAfter(gamma, b, beta_prime)

            self.edges_[delta].dir_ = EdgeDir.Hor
            self.edges_[delta].tail_ = a
            self.edges_[delta].head_ = b
            self.vertices_[a].east_ = delta
            self.vertices_[a].west_ = 0
            self.vertices_[a].type_ = VertexType.right
            self.vertices_[b].east_ = 0
            self.vertices_[b].west_ = delta
            self.vertices_[b].type_ = VertexType.left
            self.walls_[x].first_ = a
            self.walls_[x].last_ = b

            self.rectangles_[j].neast_ = b
            self.rectangles_[j].swest_ = c_prime
            self.rectangles_[j - 1].neast_ = c
            self.rectangles_[j - 1].swest_ = a

            nu = self.vertices_[c].west_
            while nu != alpha_prime:
                self.edges_[nu].right_ = j - 1
                nu = self.edges_[nu].prev_

            nu = self.vertices_[c_prime].north_
            while nu != alpha:
                self.edges_[nu].right_ = j
                nu = self.edges_[nu].next_

            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = j
            self.edges_[beta_prime].left_ = j - 1
            self.edges_[beta_prime].right_ = l
        else:
            a = self.rectangles_[j].nwest_
            b = self.rectangles_[j].neast_
            c = self.rectangles_[j].swest_
            alpha_prime = self.vertices_[a].north_
            beta = self.vertices_[a].south_
            beta_prime = self.vertices_[b].north_
            gamma = self.vertices_[c].east_
            delta = self.vertices_[a].east_
            c_prime = self.edges_[beta_prime].head_
            k = self.edges_[alpha].left_
            l = self.edges_[gamma].right_
            x = self.edges_[delta].wall_

            self.remHead(beta)
            self.remTail(beta_prime)
            self.insAfter(alpha, a, beta)
            self.insBefore(beta_prime, b, gamma)

            self.edges_[delta].dir_ = EdgeDir.Ver
            self.edges_[delta].head_ = a
            self.edges_[delta].tail_ = b
            self.vertices_[a].south_ = delta
            self.vertices_[a].north_ = 0
            self.vertices_[a].type_ = VertexType.bottom
            self.vertices_[b].south_ = 0
            self.vertices_[b].north_ = delta
            self.vertices_[b].type_ = VertexType.top
            self.walls_[x].last_ = a
            self.walls_[x].first_ = b

            self.rectangles_[j].swest_ = b
            self.rectangles_[j].neast_ = c_prime
            self.rectangles_[j - 1].swest_ = c
            self.rectangles_[j - 1].neast_ = a

            nu = self.vertices_[c].north_
            while nu != alpha_prime:
                self.edges_[nu].right_ = j - 1
                nu = self.edges_[nu].next_

            nu = self.vertices_[c_prime].west_
            while nu != alpha:
                self.edges_[nu].right_ = j
                nu = self.edges_[nu].prev_

            self.edges_[beta].left_ = k
            self.edges_[beta].right_ = j
            self.edges_[beta_prime].left_ = j - 1
            self.edges_[beta_prime].right_ = l

    def Tjump_hor(self, j: int, dir_: RectangulationDirection, alpha: int):
        if dir_ == RectangulationDirection.left:
            a = self.rectangles_[j].nwest_
            b = self.edges_[alpha].head_
            c = self.rectangles_[j].neast_
            alpha_prime = self.vertices_[a].west_
            beta = self.vertices_[a].east_
            beta_prime = self.vertices_[a].south_
            gamma = self.vertices_[c].south_
            gamma_prime = self.vertices_[b].south_
            k = self.edges_[beta_prime].left_
            l = self.edges_[gamma].right_
            m = self.edges_[alpha].right_
            x = self.edges_[alpha].wall_
            y = self.edges_[gamma_prime].wall_

            self.remTail(beta)
            self.remTail(beta_prime)
            self.insAfter(alpha, a, beta)
            self.insAfter(gamma, b, beta_prime)

            self.edges_[beta].head_ = b
            self.edges_[gamma_prime].head_ = a
            self.vertices_[a].south_ = gamma_prime
            self.vertices_[b].west_ = beta
            self.walls_[x].last_ = b
            self.walls_[y].last_ = a

            self.rectangles_[j].neast_ = b
            self.rectangles_[k].neast_ = c
            self.rectangles_[m].neast_ = a

            nu = self.vertices_[c].west_
            while nu != alpha_prime:
                self.edges_[nu].right_ = k
                nu = self.edges_[nu].prev_

            self.edges_[beta].left_ = k
            self.edges_[beta_prime].right_ = l
        else:
            a = self.rectangles_[j].nwest_
            b = self.rectangles_[j].neast_
            alpha_prime = self.vertices_[a].west_
            gamma_prime = self.vertices_[a].south_
            beta = self.vertices_[a].east_
            beta_prime = self.vertices_[b].north_
            c = self.edges_[beta_prime].head_
            k = self.edges_[beta].left_
            l = self.edges_[alpha].left_
            m = self.edges_[alpha_prime].right_
            x = self.edges_[alpha_prime].wall_
            y = self.edges_[gamma_prime].wall_

            self.remTail(beta)
            self.remTail(beta_prime)
            self.insAfter(alpha, a, beta)
            self.insAfter(gamma_prime, b, beta_prime)

            self.edges_[alpha_prime].head_ = b
            self.edges_[beta_prime].head_ = a
            self.vertices_[a].south_ = beta_prime
            self.vertices_[b].west_ = alpha_prime
            self.walls_[x].last_ = b
            self.walls_[y].last_ = a

            self.rectangles_[j].neast_ = c
            self.rectangles_[k].neast_ = a
            self.rectangles_[m].neast_ = b

            nu = self.vertices_[c].west_
            while nu != alpha:
                self.edges_[nu].right_ = j
                nu = self.edges_[nu].prev_

            self.edges_[beta].left_ = l
            self.edges_[beta_prime].right_ = j

    def Tjump_ver(self, j: int, dir_: RectangulationDirection, alpha: int):
        if dir_ == RectangulationDirection.right:
            a = self.rectangles_[j].nwest_
            b = self.edges_[alpha].tail_
            c = self.rectangles_[j].swest_
            alpha_prime = self.vertices_[a].north_
            beta = self.vertices_[a].south_
            beta_prime = self.vertices_[a].east_
            gamma = self.vertices_[c].east_
            gamma_prime = self.vertices_[b].east_
            k = self.edges_[beta_prime].left_
            l = self.edges_[gamma].right_
            m = self.edges_[alpha].right_
            x = self.edges_[alpha].wall_
            y = self.edges_[gamma_prime].wall_

            self.remHead(beta)
            self.remHead(beta_prime)
            self.insBefore(beta, a, alpha)
            self.insBefore(beta_prime, b, gamma)

            self.edges_[beta].tail_ = b
            self.edges_[gamma_prime].tail_ = a
            self.vertices_[a].east_ = gamma_prime
            self.vertices_[a].type_ = VertexType.right
            self.vertices_[b].north_ = beta
            self.vertices_[b].type_ = VertexType.top
            self.walls_[x].first_ = b
            self.walls_[y].first_ = a

            self.rectangles_[j].swest_ = b
            self.rectangles_[k].swest_ = c
            self.rectangles_[m].swest_ = a

            nu = self.vertices_[c].north_
            while nu != alpha_prime:
                self.edges_[nu].right_ = k
                nu = self.edges_[nu].next_

            self.edges_[beta].left_ = k
            self.edges_[beta_prime].right_ = l
        else:
            a = self.rectangles_[j].nwest_
            b = self.rectangles_[j].swest_
            alpha_prime = self.vertices_[a].north_
            gamma_prime = self.vertices_[a].east_
            beta = self.vertices_[a].south_
            beta_prime = self.vertices_[b].west_
            c = self.edges_[beta_prime].tail_
            k = self.edges_[beta].left_
            l = self.edges_[alpha].left_
            m = self.edges_[alpha_prime].right_
            x = self.edges_[alpha_prime].wall_
            y = self.edges_[gamma_prime].wall_

            self.remHead(beta)
            self.remHead(beta_prime)
            self.insBefore(beta, a, alpha)
            self.insBefore(beta_prime, b, gamma_prime)

            self.edges_[alpha_prime].tail_ = b
            self.edges_[beta_prime].tail_ = a
            self.vertices_[a].east_ = beta_prime
            self.vertices_[a].type_ = VertexType.right
            self.vertices_[b].north_ = alpha_prime
            self.vertices_[b].type_ = VertexType.top
            self.walls_[x].first_ = b
            self.walls_[y].first_ = a

            self.rectangles_[j].swest_ = c
            self.rectangles_[k].swest_ = a
            self.rectangles_[m].swest_ = b

            nu = self.vertices_[c].north_
            while nu != alpha:
                self.edges_[nu].right_ = j
                nu = self.edges_[nu].next_

            self.edges_[beta].left_ = l
            self.edges_[beta_prime].right_ = j

    def next_generic(self, j: int, dir_: RectangulationDirection):
        a = self.rectangles_[j].nwest_

        if (
            dir_ == RectangulationDirection.left
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].west_
            beta = self.vertices_[a].south_
            b = self.edges_[beta].tail_
            c = self.edges_[alpha].tail_

            if self.vertices_[c].type_ == VertexType.top:
                gamma = self.vertices_[c].west_
                self.Wjump_hor(j, RectangulationDirection.left, gamma)
            elif self.vertices_[b].type_ == VertexType.left:
                gamma = self.vertices_[b].west_
                self.Tjump_hor(j, RectangulationDirection.left, gamma)
            else:
                gamma = self.vertices_[c].south_
                self.Sjump(j, RectangulationDirection.left, gamma)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].east_
            b = self.edges_[alpha].head_

            if self.vertices_[b].type_ == VertexType.top:
                gamma = self.vertices_[b].east_
                self.Wjump_hor(j, RectangulationDirection.right, gamma)
            else:
                k = self.edges_[alpha].left_
                c = self.rectangles_[k].nwest_
                gamma = self.vertices_[c].east_
                self.Tjump_hor(j, RectangulationDirection.right, gamma)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.right
        ):
            alpha = self.vertices_[a].north_
            beta = self.vertices_[a].east_
            b = self.edges_[beta].head_
            c = self.edges_[alpha].head_

            if self.vertices_[c].type_ == VertexType.left:
                gamma = self.vertices_[c].north_
                self.Wjump_ver(j, RectangulationDirection.right, gamma)
            elif self.vertices_[b].type_ == VertexType.top:
                gamma = self.vertices_[b].north_
                self.Tjump_ver(j, RectangulationDirection.right, gamma)
            else:
                gamma = self.vertices_[c].east_
                self.Sjump(j, RectangulationDirection.right, gamma)

        else:
            alpha = self.vertices_[a].south_
            b = self.edges_[alpha].tail_

            if self.vertices_[b].type_ == VertexType.left:
                gamma = self.vertices_[b].south_
                self.Wjump_ver(j, RectangulationDirection.left, gamma)
            else:
                k = self.edges_[alpha].left_
                c = self.rectangles_[k].nwest_
                gamma = self.vertices_[c].south_
                self.Tjump_ver(j, RectangulationDirection.left, gamma)

    def next_diagonal(self, j: int, dir_: RectangulationDirection):
        a = self.rectangles_[j].nwest_

        if (
            dir_ == RectangulationDirection.left
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].south_
            b = self.edges_[alpha].tail_

            if self.vertices_[b].type_ == VertexType.left:
                gamma = self.vertices_[b].west_
                self.Tjump_hor(j, RectangulationDirection.left, gamma)
            else:
                c = self.rectangles_[j - 1].swest_
                gamma = self.vertices_[c].north_
                self.Sjump(j, RectangulationDirection.left, gamma)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].east_
            k = self.edges_[alpha].left_
            b = self.rectangles_[k].neast_
            gamma = self.vertices_[b].west_
            self.Tjump_hor(j, RectangulationDirection.right, gamma)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.right
        ):
            alpha = self.vertices_[a].east_
            b = self.edges_[alpha].head_

            if self.vertices_[b].type_ == VertexType.top:
                gamma = self.vertices_[b].north_
                self.Tjump_ver(j, RectangulationDirection.right, gamma)
            else:
                c = self.rectangles_[j - 1].neast_
                gamma = self.vertices_[c].west_
                self.Sjump(j, RectangulationDirection.right, gamma)

        else:
            alpha = self.vertices_[a].south_
            k = self.edges_[alpha].left_
            b = self.rectangles_[k].swest_
            gamma = self.vertices_[b].north_
            self.Tjump_ver(j, RectangulationDirection.left, gamma)

    def next_baligned(self, j: int, dir_: RectangulationDirection):
        a = self.rectangles_[j].nwest_
        self.unlock(j, dir_)

        if (
            dir_ == RectangulationDirection.left
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].south_
            b = self.edges_[alpha].tail_

            if self.vertices_[b].type_ == VertexType.left:
                gamma = self.vertices_[b].west_
                self.Tjump_hor(j, RectangulationDirection.left, gamma)
                a = self.rectangles_[j].nwest_
                alpha = self.vertices_[a].south_
                b = self.edges_[alpha].tail_
                c = self.rectangles_[j - 1].swest_
                gamma = self.vertices_[c].north_
                c_prime = self.rectangles_[j].seast_

                if self.vertices_[b].type_ == VertexType.top and (
                    self.vertices_[c_prime].type_ == VertexType.left
                    or (j == self.n_ and self.edges_[gamma].left_ == 0)
                ):
                    self.Sjump(j, RectangulationDirection.left, gamma)

                self.lock(j, EdgeDir.Hor)
            else:
                c = self.rectangles_[j - 1].swest_
                gamma = self.vertices_[c].north_
                self.Sjump(j, RectangulationDirection.left, gamma)
                gamma = self.vertices_[c].north_
                k = self.edges_[gamma].left_
                c_prime = self.rectangles_[k].swest_
                gamma_prime = self.vertices_[c_prime].north_
                self.Tjump_ver(j, RectangulationDirection.left, gamma_prime)
                c = self.rectangles_[j - 1].swest_
                gamma = self.vertices_[c].north_
                a = self.edges_[gamma].head_

                if self.vertices_[a].type_ == VertexType.bottom:
                    c_prime = self.rectangles_[j - 2].swest_
                    gamma_prime = self.vertices_[c_prime].north_
                    self.Sjump(j - 1, RectangulationDirection.left, gamma_prime)

                self.lock(j - 1, EdgeDir.Hor)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.bottom
        ):
            alpha = self.vertices_[a].east_
            k = self.edges_[alpha].left_
            b = self.rectangles_[k].neast_
            gamma = self.vertices_[b].west_
            self.Tjump_hor(j, RectangulationDirection.right, gamma)
            a = self.rectangles_[j].nwest_
            alpha = self.vertices_[a].south_
            b = self.edges_[alpha].tail_
            beta = self.vertices_[b].south_
            gamma = self.vertices_[b].west_
            c = self.edges_[beta].tail_
            c_prime = self.edges_[gamma].tail_

            if (
                self.vertices_[c].type_ == VertexType.top
                and self.vertices_[c_prime].type_ == VertexType.right
            ):
                gamma_prime = self.vertices_[a].west_
                self.Sjump(j - 1, RectangulationDirection.right, gamma_prime)

            self.lock(j, EdgeDir.Ver)

        elif (
            dir_ == RectangulationDirection.right
            and self.vertices_[a].type_ == VertexType.right
        ):
            alpha = self.vertices_[a].east_
            b = self.edges_[alpha].head_

            if self.vertices_[b].type_ == VertexType.top:
                gamma = self.vertices_[b].north_
                self.Tjump_ver(j, RectangulationDirection.right, gamma)
                a = self.rectangles_[j].nwest_
                alpha = self.vertices_[a].east_
                b = self.edges_[alpha].head_
                c = self.rectangles_[j - 1].neast_
                gamma = self.vertices_[c].west_
                c_prime = self.rectangles_[j].seast_
                e = self.rectangles_[j - 1].nwest_

                if self.vertices_[b].type_ == VertexType.left and (
                    self.vertices_[c_prime].type_ == VertexType.top
                    or (
                        j == self.n_
                        and not (
                            self.vertices_[e].type_ == VertexType.right
                            and self.edges_[gamma].tail_ == e
                        )
                    )
                ):
                    self.Sjump(j, RectangulationDirection.right, gamma)

                self.lock(j, EdgeDir.Ver)
            else:
                c = self.rectangles_[j - 1].neast_
                gamma = self.vertices_[c].west_
                self.Sjump(j, RectangulationDirection.right, gamma)
                gamma = self.vertices_[c].west_
                k = self.edges_[gamma].left_
                c_prime = self.rectangles_[k].neast_
                gamma_prime = self.vertices_[c_prime].west_
                self.Tjump_hor(j, RectangulationDirection.right, gamma_prime)
                c = self.rectangles_[j - 1].neast_
                gamma = self.vertices_[c].west_
                a = self.edges_[gamma].tail_

                if self.vertices_[a].type_ == VertexType.right:
                    c_prime = self.rectangles_[j - 2].neast_
                    gamma_prime = self.vertices_[c_prime].west_
                    self.Sjump(j - 1, RectangulationDirection.right, gamma_prime)

                self.lock(j - 1, EdgeDir.Ver)

        else:
            alpha = self.vertices_[a].south_
            k = self.edges_[alpha].left_
            b = self.rectangles_[k].swest_
            gamma = self.vertices_[b].north_
            self.Tjump_ver(j, RectangulationDirection.left, gamma)
            a = self.rectangles_[j].nwest_
            alpha = self.vertices_[a].east_
            b = self.edges_[alpha].head_
            beta = self.vertices_[b].east_
            gamma = self.vertices_[b].north_
            c = self.edges_[beta].head_
            c_prime = self.edges_[gamma].head_

            if (
                self.vertices_[c].type_ == VertexType.left
                and self.vertices_[c_prime].type_ == VertexType.bottom
            ):
                gamma_prime = self.vertices_[a].north_
                self.Sjump(j - 1, RectangulationDirection.left, gamma_prime)

            self.lock(j, EdgeDir.Hor)

    def lock(self, j: int, dir_: EdgeDir):
        if dir_ == EdgeDir.Hor:
            a = self.rectangles_[j].neast_
            b = self.rectangles_[j].swest_
            c = self.rectangles_[j].seast_
            alpha = self.vertices_[a].west_
            beta = self.vertices_[b].east_

            if (
                (self.vertices_[b].type_ != VertexType.right)
                or (self.vertices_[c].type_ != VertexType.left)
                or (self.edges_[beta].head_ != c)
            ):
                return

            d = self.rectangles_[j + 1].seast_
            if self.vertices_[d].type_ == VertexType.top:
                self.Sjump(j + 1, RectangulationDirection.right, alpha)
        else:
            a = self.rectangles_[j].swest_
            b = self.rectangles_[j].neast_
            c = self.rectangles_[j].seast_
            alpha = self.vertices_[a].north_
            beta = self.vertices_[b].south_

            if (
                (self.vertices_[b].type_ != VertexType.bottom)
                or (self.vertices_[c].type_ != VertexType.top)
                or (self.edges_[beta].tail_ != c)
            ):
                return

            d = self.rectangles_[j + 1].seast_
            if self.vertices_[d].type_ == VertexType.left:
                self.Sjump(j + 1, RectangulationDirection.left, alpha)

    def unlock(self, j: int, dir_: RectangulationDirection):
        if dir_ == RectangulationDirection.right:
            a = self.rectangles_[j].neast_
            b = self.rectangles_[j].seast_
            c = self.rectangles_[j].swest_
            gamma = self.vertices_[c].north_

            if (
                self.vertices_[a].type_ == VertexType.bottom
                and self.vertices_[b].type_ == VertexType.top
            ):
                self.Sjump(j + 1, RectangulationDirection.left, gamma)
        else:
            a = self.rectangles_[j].swest_
            b = self.rectangles_[j].seast_
            c = self.rectangles_[j].neast_
            gamma = self.vertices_[c].west_

            if (
                self.vertices_[a].type_ == VertexType.right
                and self.vertices_[b].type_ == VertexType.left
            ):
                self.Sjump(j + 1, RectangulationDirection.right, gamma)

    def contains_pattern(self, j: int) -> bool:
        for p in self.patterns_:
            if (
                p == RectangulationPattern.brick_leftright
                and self.contains_brick_leftright(j)
            ):
                return True
            elif (
                p == RectangulationPattern.brick_rightleft
                and self.contains_brick_rightleft(j)
            ):
                return True
            elif (
                p == RectangulationPattern.brick_bottomtop
                and self.contains_brick_bottomtop(j)
            ):
                return True
            elif (
                p == RectangulationPattern.brick_topbottom
                and self.contains_brick_topbottom(j)
            ):
                return True
            elif (
                p == RectangulationPattern.wmill_clockwise
                and self.contains_wmill_clockwise(j)
            ):
                return True
            elif (
                p == RectangulationPattern.wmill_counterclockwise
                and self.contains_wmill_counterclockwise(j)
            ):
                return True
            elif p == RectangulationPattern.H_vertical and self.contains_H_vertical(j):
                return True
            elif p == RectangulationPattern.H_horizontal and self.contains_H_horizontal(
                j
            ):
                return True
        return False

    def contains_brick_leftright(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.bottom:
            return False

        alpha = self.vertices_[a].south_
        b = self.edges_[alpha].tail_
        return self.vertices_[b].type_ == VertexType.left

    def contains_brick_rightleft(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.bottom:
            return False

        alpha = self.vertices_[a].north_
        b = self.edges_[alpha].head_
        return self.vertices_[b].type_ == VertexType.left

    def contains_brick_bottomtop(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.right:
            return False

        alpha = self.vertices_[a].east_
        b = self.edges_[alpha].head_
        return self.vertices_[b].type_ == VertexType.top

    def contains_brick_topbottom(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.right:
            return False

        alpha = self.vertices_[a].west_
        b = self.edges_[alpha].tail_
        return self.vertices_[b].type_ == VertexType.top

    def contains_wmill_clockwise(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.bottom:
            return False

        alpha = self.vertices_[a].north_
        x = self.edges_[alpha].wall_
        b = self.walls_[x].last_
        beta = self.vertices_[b].east_
        y = self.edges_[beta].wall_
        c = self.walls_[y].last_
        gamma = self.vertices_[c].south_
        z = self.edges_[gamma].wall_
        d = self.walls_[z].first_
        delta = self.vertices_[d].west_
        return self.edges_[delta].right_ == j

    def contains_wmill_counterclockwise(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.right:
            return False

        alpha = self.vertices_[a].west_
        x = self.edges_[alpha].wall_
        b = self.walls_[x].first_
        beta = self.vertices_[b].south_
        y = self.edges_[beta].wall_
        c = self.walls_[y].first_
        gamma = self.vertices_[c].east_
        z = self.edges_[gamma].wall_
        d = self.walls_[z].last_
        delta = self.vertices_[d].north_
        return self.edges_[delta].right_ == j

    def contains_H_vertical(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.bottom:
            return False

        b = self.rectangles_[j].swest_

        while (
            self.vertices_[b].type_ != VertexType.bottom
            and self.vertices_[b].type_ != VertexType.corner
        ):
            c = b
            while (
                self.vertices_[c].type_ != VertexType.right
                and self.vertices_[c].type_ != VertexType.corner
            ):
                if self.vertices_[c].type_ == VertexType.top:
                    d = c
                    while (
                        d != b
                        and self.vertices_[d].type_ != VertexType.bottom
                        and self.vertices_[d].type_ != VertexType.corner
                    ):
                        if self.vertices_[d].type_ == VertexType.left:
                            return True
                        delta = self.vertices_[d].north_
                        d = self.edges_[delta].head_
                gamma = self.vertices_[c].west_
                c = self.edges_[gamma].tail_
            beta = self.vertices_[b].north_
            b = self.edges_[beta].head_

        return False

    def contains_H_horizontal(self, j: int) -> bool:
        a = self.rectangles_[j].nwest_
        if self.vertices_[a].type_ == VertexType.right:
            return False

        b = self.rectangles_[j].neast_

        while (
            self.vertices_[b].type_ != VertexType.right
            and self.vertices_[b].type_ != VertexType.corner
        ):
            c = b
            while (
                self.vertices_[c].type_ != VertexType.bottom
                and self.vertices_[c].type_ != VertexType.corner
            ):
                if self.vertices_[c].type_ == VertexType.left:
                    d = c
                    while (
                        d != b
                        and self.vertices_[d].type_ != VertexType.right
                        and self.vertices_[d].type_ != VertexType.corner
                    ):
                        if self.vertices_[d].type_ == VertexType.top:
                            return True
                        delta = self.vertices_[d].west_
                        d = self.edges_[delta].tail_
                gamma = self.vertices_[c].north_
                c = self.edges_[gamma].head_
            beta = self.vertices_[b].west_
            b = self.edges_[beta].tail_

        return False


def help():
    print(
        "./rect [options]   generate various classes of rectangulations as described in [Merino,Muetze]"
    )
    print("-h                 display this help")
    print("-n{1,2,...}        number of rectangles")
    print(
        "-t{1,2,3}          base type of rectangulations: *1=generic, 2=diagonal, 3=block-aligned"
    )
    print(
        "-p{1,2,..,8}       forbidden patterns: 1=cw windmill, 2=ccw windmill, 3=left/right brick,"
    )
    print(
        "                     4=bottom/top brick, 5=right/left brick, 6=top/bottom brick, 7=vertical H,"
    )
    print(
        "                     8=horizontal H (see the paper for definitions; -p3,...,-p8 unavailable for -t3)"
    )
    print("-l{-1,0,1,2,...}   number of rectangulations to list; *-1 for all")
    print("-q                 quiet output")
    print("-c                 output number of rectangles")
    print("examples:  ./rect -n5 -c")
    print("           ./rect -n5 -t2 -c")
    print("           ./rect -n5 -p3456 -c")
    print("           ./rect -n10 -t3 -l30")
    print("           ./rect -n10 -q -c")


def main():
    n = 0
    n_set = False
    t = 0
    steps = -1
    quiet = False
    output_counts = False
    patterns3to8 = False
    type_ = RectangulationType.generic
    patterns = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:t:p:l:qc")
    except getopt.GetoptError:
        help()
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit(0)
        elif opt == "-n":
            n = int(arg)
            if n < 1:
                print(
                    "option -n must be followed by an integer from {1,2,...}",
                    file=sys.stderr,
                )
                sys.exit(1)
            n_set = True
        elif opt == "-t":
            t = int(arg)
            if t < 1 or t > 3:
                print(
                    "option -t must be followed by an integer from {1,2,3}",
                    file=sys.stderr,
                )
                sys.exit(1)
            if t == 1:
                type_ = RectangulationType.generic
            elif t == 2:
                type_ = RectangulationType.diagonal
            elif t == 3:
                type_ = RectangulationType.baligned
        elif opt == "-p":
            for c in arg:
                p = int(c)
                if p < 1 or p > 8:
                    print(
                        "option -p must be followed by an integer from {1,2,...,8}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                if p == 1:
                    patterns.append(RectangulationPattern.wmill_clockwise)
                elif p == 2:
                    patterns.append(RectangulationPattern.wmill_counterclockwise)
                elif p == 3:
                    patterns.append(RectangulationPattern.brick_leftright)
                    patterns3to8 = True
                elif p == 4:
                    patterns.append(RectangulationPattern.brick_bottomtop)
                    patterns3to8 = True
                elif p == 5:
                    patterns.append(RectangulationPattern.brick_rightleft)
                    patterns3to8 = True
                elif p == 6:
                    patterns.append(RectangulationPattern.brick_topbottom)
                    patterns3to8 = True
                elif p == 7:
                    patterns.append(RectangulationPattern.H_vertical)
                    patterns3to8 = True
                elif p == 8:
                    patterns.append(RectangulationPattern.H_horizontal)
                    patterns3to8 = True
        elif opt == "-l":
            steps = int(arg)
            if steps < -1:
                print(
                    "option -l must be followed by an integer from {-1,0,1,2,...}",
                    file=sys.stderr,
                )
                sys.exit(1)
        elif opt == "-q":
            quiet = True
        elif opt == "-c":
            output_counts = True

    if not n_set:
        print("option -n is mandatory", file=sys.stderr)
        help()
        sys.exit(1)

    if type_ == RectangulationType.baligned and patterns3to8:
        print("patterns -p3 to -p8 unavailable for -t3", file=sys.stderr)
        sys.exit(1)

    num_rectangulations = 0
    rect = Rectangulation(n, type_, patterns)

    if steps == 0:
        print("output limit reached")
        sys.exit(0)

    while True:
        num_rectangulations += 1
        if not quiet:
            rect.print_coordinates()
        elif num_rectangulations % 10000000 == 0:
            print(".", end="", flush=True)

        if not rect.next():
            break

        if steps >= 0 and num_rectangulations >= steps:
            print("output limit reached")
            break

    if output_counts:
        if quiet and num_rectangulations >= 10000000:
            print()
        print(f"number of rectangulations: {num_rectangulations}")


if __name__ == "__main__":
    main()
