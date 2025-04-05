import sys
import getopt
from typing import List, Tuple, Callable, Optional


class Vertex:
    def __init__(self, x: List[int]):
        assert len(x) % 2 == 1
        assert len(x) >= 3
        self.bits = x.copy()

    def __getitem__(self, i: int) -> int:
        return self.bits[i]

    def __setitem__(self, i: int, value: int):
        self.bits[i] = value

    def __len__(self) -> int:
        return len(self.bits)

    def __eq__(self, other: "Vertex") -> bool:
        return self.bits == other.bits

    def __str__(self) -> str:
        return "".join(map(str, self.bits))

    def rev_inv(self, left: Optional[int] = None, right: Optional[int] = None):
        if left is None and right is None:
            left = 0
            right = len(self.bits) - 2
        for i in range(left, right + 1):
            self.bits[i] = 1 - self.bits[i]
        self.bits[left : right + 1] = reversed(self.bits[left : right + 1])

    def first_touchdown(self, a: int) -> int:
        height = 0
        for i in range(a, len(self.bits) - 1):
            height += 2 * self.bits[i] - 1
            if height == 0:
                return i
        return -1

    def first_dive(self) -> int:
        height = 0
        for i in range(len(self.bits) - 1):
            height += 2 * self.bits[i] - 1
            if height == -1:
                return i
        return -1

    def steps_height(
        self,
    ) -> Tuple[List[List[int]], List[List[int]], List[List[int]], List[List[int]]]:
        usteps_neg = []
        usteps_pos = []
        dsteps_neg = []
        dsteps_pos = []
        height = 0
        min_height = 0
        max_height = 0

        for i in range(len(self.bits) - 1):
            if self.bits[i] == 0 and height <= 0:
                if height == min_height:
                    usteps_neg.append([])
                    dsteps_neg.append([])
                dsteps_neg[-height].append(i)

            if self.bits[i] == 1 and height >= 0:
                if height == max_height:
                    usteps_pos.append([])
                    dsteps_pos.append([])
                usteps_pos[height].append(i)

            height += 2 * self.bits[i] - 1
            min_height = min(height, min_height)
            max_height = max(height, max_height)

            if self.bits[i] == 0 and height >= 0:
                dsteps_pos[height].append(i)
                assert len(dsteps_pos[height]) == len(usteps_pos[height])

            if self.bits[i] == 1 and height <= 0:
                usteps_neg[-height].append(i)
                assert len(usteps_neg[-height]) == len(dsteps_neg[-height])

        assert len(usteps_neg) == len(dsteps_neg)
        return usteps_neg, usteps_pos, dsteps_neg, dsteps_pos

    def count_flaws(self) -> int:
        c = 0
        height = 0
        for i in range(len(self.bits) - 1):
            if height <= 0 and self.bits[i] == 0:
                c += 1
            height += 2 * self.bits[i] - 1
        return c

    def count_ones(self) -> int:
        return sum(self.bits[:-1])

    def is_first_vertex(self) -> bool:
        return self.count_flaws() == 0 and self.count_ones() == len(self.bits) // 2

    def is_last_vertex(self) -> bool:
        return self.count_flaws() == 1 and self.count_ones() == len(self.bits) // 2

    def to_first_vertex(self) -> int:
        if self.is_last_vertex():
            b = self.first_dive()
            self.bits[1 : b + 1] = self.bits[:b]
            self.bits[0] = 1
            self.bits[b + 1] = 0
            return 2 * b + 2
        else:
            usteps_neg, usteps_pos, dsteps_neg, dsteps_pos = self.steps_height()
            min_zero = len(usteps_neg) == 0
            unique_min = (
                len(usteps_pos[0]) == 1 if min_zero else len(usteps_neg[-1]) == 1
            )
            middle_level = 2 * self.count_ones() + 1 == len(self.bits)

            if (not unique_min and middle_level) or (unique_min and not middle_level):
                to = (usteps_pos[0][0] if min_zero else usteps_neg[-1][0]) - 1
            else:
                to = (usteps_pos[0][-1] if min_zero else usteps_neg[-1][-1]) - 1

            self.bits[1 : to + 2] = self.bits[: to + 1]
            self.bits[0] = 1

            for d in range(
                len(dsteps_neg) - (1 if (unique_min and middle_level) else 0)
            ):
                self.bits[dsteps_neg[d][0] + 1] = 1

            for d in range(
                len(usteps_neg) - (1 if (unique_min and not middle_level) else 0)
            ):
                self.bits[usteps_neg[d][-1]] = 0

            if not middle_level:
                for d in range(1 if (min_zero and unique_min) else 0, 2):
                    self.bits[usteps_pos[d][-1]] = 0

            return 2 * (to + 1) + (0 if middle_level else 1)

    def to_last_vertex(self) -> int:
        d = 0
        if not self.is_first_vertex():
            d = -self.to_first_vertex()
        assert self.is_first_vertex()

        b = self.first_touchdown(0)
        self.bits[: b - 1] = self.bits[1:b]
        self.bits[b - 1] = 0
        self.bits[b] = 1
        d += 2 * (b - 1) + 2
        return d

    def compute_flip_seq_0(self, flip: bool) -> List[int]:
        assert self.is_first_vertex()
        seq = []

        if not flip:
            b = self.first_touchdown(0)
            length = 2 * (b - 1) + 2
            seq = [0] * length
            next_step = [0] * (b + 1)
            self.aux_pointers(0, b, next_step)

            idx = 0
            seq[idx] = b
            idx += 1
            seq[idx] = 0
            idx += 1
            self.compute_flip_seq_0_rec(seq, idx, 1, b - 1, next_step)
            return seq

        assert flip
        assert self.bits[0] == 1

        if self.bits[1] == 1:
            assert self.bits[2] == 0
            return [2, 0]
        else:
            self.bits[1] = 1
            self.bits[2] = 0

            b = self.first_touchdown(0)
            length = 2 * (b - 1) + 2
            seq = [0] * length
            next_step = [0] * (b + 1)
            self.aux_pointers(0, b, next_step)

            idx = 0
            seq[idx] = b
            idx += 1
            seq[idx] = 0
            idx += 1
            self.compute_flip_seq_0_rec(seq, idx, 1, b - 1, next_step)

            self.bits[1] = 0
            self.bits[2] = 1

            assert (
                seq[0] == b
                and seq[1] == 0
                and seq[2] == 2
                and seq[3] == 1
                and seq[4] == 0
                and seq[5] == 2
            )
            seq[0] = b
            seq[1] = 0
            seq[2] = 1
            seq[3] = 2
            seq[4] = 0
            seq[5] = 1
            return seq

    def compute_flip_seq_0_rec(
        self, seq: List[int], idx: int, left: int, right: int, next_step: List[int]
    ):
        length = right - left + 1
        if length <= 0:
            return

        assert self.bits[left] == 1 and self.bits[right] == 0 and length % 2 == 0

        m = next_step[left]
        assert m <= right and self.bits[m] == 0
        seq[idx] = m
        idx += 1
        seq[idx] = left
        idx += 1
        self.compute_flip_seq_0_rec(seq, idx, left + 1, m - 1, next_step)
        seq[idx] = left - 1
        idx += 1
        seq[idx] = m
        idx += 1
        self.compute_flip_seq_0_rec(seq, idx, m + 1, right, next_step)

    def compute_flip_seq_1(self) -> List[int]:
        assert self.is_last_vertex()
        b = self.first_dive()
        length = 2 * ((len(self.bits) - 2) - (b + 2) + 1) + 2
        seq = [0] * length
        next_step = [0] * (len(self.bits) - 1)
        self.aux_pointers(b + 2, len(self.bits) - 2, next_step)

        idx = 0
        seq[idx] = b + 1
        idx += 1
        self.compute_flip_seq_1_rec(seq, idx, b + 2, len(self.bits) - 2, next_step)
        seq[idx] = b
        idx += 1
        return seq

    def compute_flip_seq_1_rec(
        self, seq: List[int], idx: int, left: int, right: int, next_step: List[int]
    ):
        length = right - left + 1
        if length <= 0:
            return

        assert self.bits[left] == 1 and self.bits[right] == 0 and length % 2 == 0

        m = next_step[left]
        seq[idx] = m
        idx += 1
        seq[idx] = left
        idx += 1
        self.compute_flip_seq_1_rec(seq, idx, left + 1, m - 1, next_step)
        seq[idx] = left - 1
        idx += 1
        seq[idx] = m
        idx += 1
        self.compute_flip_seq_1_rec(seq, idx, m + 1, right, next_step)

    def aux_pointers(self, a: int, b: int, next_step: List[int]):
        assert a == b + 1 or (self.bits[a] == 1 and self.bits[b] == 0)
        left_ustep_height = [0] * (b - a + 1)
        height = 0

        for i in range(a, b + 1):
            if self.bits[i] == 0:
                assert height >= 1
                left = left_ustep_height[height - 1]
                assert 0 <= left < i
                next_step[left] = i
                next_step[i] = left
            else:
                assert height >= 0
                left_ustep_height[height] = i
            height += 2 * self.bits[i] - 1
        assert height == 0


class Tree:
    def __init__(self, x: Vertex):
        xv = x.bits.copy()
        assert len(xv) % 2 == 1

        self.root = 0
        self.num_vertices = (len(xv) - 1) // 2 + 1
        self.children = [[] for _ in range(self.num_vertices)]
        self.parent = [0] * self.num_vertices

        u = self.root
        n = 1
        height = 0

        for i in range(len(xv) - 1):
            if xv[i] == 1:
                self.children[u].append(n)
                self.parent[n] = u
                u = n
                n += 1
            else:
                u = self.parent[u]
            height += 2 * xv[i] - 1
            assert height >= 0
        assert n == self.num_vertices

    def deg(self, u: int) -> int:
        assert 0 <= u < self.num_vertices
        return len(self.children[u]) + (0 if u == self.root else 1)

    def num_children(self, u: int) -> int:
        assert 0 <= u < self.num_vertices
        return len(self.children[u])

    def ith_child(self, u: int, i: int) -> int:
        assert 0 <= u < self.num_vertices
        assert 0 <= i < self.num_children(u)
        return self.children[u][i]

    def is_tau_preimage(self) -> bool:
        if self.num_vertices < 3:
            return False
        u = self.ith_child(self.root, 0)
        if self.num_children(u) == 0:
            return False
        v = self.ith_child(u, 0)
        return self.num_children(v) == 0

    def is_tau_image(self) -> bool:
        return (
            self.num_vertices >= 3
            and self.num_children(self.root) >= 2
            and self.num_children(self.ith_child(self.root, 0)) == 0
        )

    def tau(self):
        assert self.is_tau_preimage()
        u = self.ith_child(self.root, 0)
        v = self.ith_child(u, 0)
        self.move_leaf(v, self.root, 0)

    def tau_inverse(self):
        assert self.is_tau_image()
        v = self.ith_child(self.root, 0)
        u = self.ith_child(self.root, 1)
        self.move_leaf(v, u, 0)

    def move_leaf(self, leaf: int, new_parent: int, pos: int):
        assert 0 <= leaf < self.num_vertices
        assert 0 <= new_parent < self.num_vertices
        assert 0 <= pos <= len(self.children[new_parent])
        assert self.num_children(leaf) == 0

        old_parent = self.parent[leaf]
        self.children[old_parent].remove(leaf)
        self.children[new_parent].insert(pos, leaf)
        self.parent[leaf] = new_parent

    def rotate(self):
        assert self.num_vertices >= 2
        u = self.ith_child(self.root, 0)
        self.parent[self.root] = u
        moved_child = self.children[self.root].pop(0)
        self.children[u].append(moved_child)
        self.children[u][-1] = self.root
        self.root = u

    def rotate_to_vertex(self, u: int):
        while self.root != u:
            self.rotate()

    def rotate_children(self, k: int = 1):
        self.children[self.root] = (
            self.children[self.root][k:] + self.children[self.root][:k]
        )

    def flip_tree(self) -> bool:
        if self.is_tau_preimage() and self.is_flip_tree_tau():
            self.tau()
            return True
        elif self.is_tau_image():
            self.tau_inverse()
            if self.is_flip_tree_tau():
                return True
            self.tau()
        return False

    def root_canonically(self):
        c1, c2 = self.compute_center()
        if c2 != -1:
            self.rotate_to_vertex(c1)
            while self.ith_child(self.root, 0) != c2:
                self.rotate_children()
            x1 = self.to_bitstring()

            self.rotate()
            self.rotate_children(self.num_children(self.root) - 1)
            assert self.root == c2 and self.ith_child(self.root, 0) == c1
            x2 = self.to_bitstring()

            if bitstrings_less_than(x1, x2, len(x1)):
                self.rotate()
                self.rotate_children(self.num_children(self.root) - 1)
                assert self.root == c1 and self.ith_child(self.root, 0) == c2
        else:
            self.rotate_to_vertex(c1)
            x = self.to_bitstring()
            subtree_count = [0] * len(x)
            c = 0
            depth = 0

            for i in range(len(x)):
                if x[i] == 1:
                    depth += 1
                else:
                    depth -= 1
                subtree_count[i] = c
                if depth == 0:
                    c += 1

            k = self.min_string_rotation(x)
            self.rotate_children(subtree_count[k])

    def compute_center(self) -> Tuple[int, int]:
        degs = [self.deg(i) for i in range(self.num_vertices)]
        leaves = [i for i in range(self.num_vertices) if degs[i] == 1]
        num_leaves = len(leaves)
        num_vertices_remaining = self.num_vertices
        num_new_leaves = 0

        while num_vertices_remaining > 2:
            for i in range(num_leaves):
                u = leaves[i]
                for child in self.children[u]:
                    degs[child] -= 1
                    if degs[child] == 1:
                        leaves[num_new_leaves] = child
                        num_new_leaves += 1
                if u != self.root:
                    degs[self.parent[u]] -= 1
                    if degs[self.parent[u]] == 1:
                        leaves[num_new_leaves] = self.parent[u]
                        num_new_leaves += 1
            num_vertices_remaining -= num_leaves
            num_leaves = num_new_leaves
            num_new_leaves = 0

        assert 1 <= num_leaves <= 2
        return (leaves[0], leaves[1] if num_leaves == 2 else -1)

    def is_flip_tree_tau(self) -> bool:
        if self.is_star():
            return False

        r = self.root
        u = self.ith_child(self.root, 0)
        num_bits = 2 * (self.num_vertices - 1)

        v = self.ith_child(self.root, 0)
        if self.num_children(v) == 1 and self.num_children(self.ith_child(v, 0)) == 0:
            this_bitstring = self.to_bitstring()
            self.root_canonically()
            v = self.ith_child(self.root, 0)
            while not (
                self.num_children(v) == 1
                and self.num_children(self.ith_child(v, 0)) == 0
            ):
                self.rotate()
                v = self.ith_child(self.root, 0)
            canon_bitstring = self.to_bitstring()
        else:
            if self.has_thin_leaf():
                return False
            v = self.ith_child(self.root, 0)
            c = self.count_pending_edges(v)
            if c < self.num_children(v) or c < 2 or self.is_light_dumbbell():
                return False
            this_bitstring = self.to_bitstring()
            self.root_canonically()
            v = self.ith_child(self.root, 0)
            c = self.count_pending_edges(v)
            while c < self.num_children(v) or c < 2:
                self.rotate()
                self.rotate_children(c)
                v = self.ith_child(self.root, 0)
                c = self.count_pending_edges(v)
            canon_bitstring = self.to_bitstring()

        self.rotate_to_vertex(r)
        while self.ith_child(self.root, 0) != u:
            self.rotate_children()

        return bitstrings_equal(this_bitstring, canon_bitstring)

    def is_star(self) -> bool:
        return (
            self.num_vertices <= 3
            or self.deg(self.root) == self.num_vertices - 1
            or self.deg(self.ith_child(self.root, 0)) == self.num_vertices - 1
        )

    def is_light_dumbbell(self) -> bool:
        if self.num_vertices < 5:
            return False
        u = self.ith_child(self.root, 0)
        k = self.num_children(u)
        l = self.num_children(self.root) - 1
        return k + l + 1 >= self.num_vertices - 1 and k > l

    def is_thin_leaf(self, u: int) -> bool:
        if self.deg(u) > 1:
            return False
        return (u == self.root and self.deg(self.ith_child(u, 0)) == 2) or (
            u != self.root and self.deg(self.parent[u]) == 2
        )

    def has_thin_leaf(self) -> bool:
        return any(self.is_thin_leaf(i) for i in range(self.num_vertices))

    def count_pending_edges(self, u: int) -> int:
        c = 0
        for i in range(self.num_children(u)):
            v = self.ith_child(u, i)
            if self.num_children(v) == 0:
                c += 1
            else:
                break
        return c

    def to_bitstring(self) -> List[int]:
        x = []
        self.to_bitstring_rec(x, self.root, 0)
        return x

    def to_bitstring_rec(self, x: List[int], u: int, pos: int):
        if self.num_children(u) == 0:
            return
        for child in self.children[u]:
            x.append(1)
            self.to_bitstring_rec(x, child, pos + 1)
            x.append(0)

    def min_string_rotation(self, x: List[int]) -> int:
        xx = x + x
        fail = [-1] * (2 * len(x))
        k = 0

        for j in range(1, 2 * len(x)):
            xj = xx[j]
            i = fail[j - k - 1]

            while i != -1 and xj != xx[k + i + 1]:
                if xj < xx[k + i + 1]:
                    k = j - i - 1
                i = fail[i]

            if xj != xx[k + i + 1]:
                if xj < xx[k]:
                    k = j
                fail[j - k] = -1
            else:
                fail[j - k] = i + 1
        return k


def bitstrings_less_than(x: List[int], y: List[int], length: int) -> bool:
    for i in range(length):
        if x[i] < y[i]:
            return True
        elif x[i] > y[i]:
            return False
    return False


def bitstrings_equal(x: List[int], y: List[int], length: int) -> bool:
    return all(x[i] == y[i] for i in range(length))


class HamCycle:
    def __init__(
        self, x: Vertex, limit: int, visit_f: Callable[[List[int], int], None]
    ):
        assert len(x) % 2 == 1
        n = len(x) // 2

        xs = Vertex(x.bits.copy())
        skip = 0

        if xs[2 * n] == 1:
            xs.rev_inv()
            skip += xs.to_last_vertex()
            xs.rev_inv()
            xs[2 * n] = 0
            skip += 1

        skip += xs.to_first_vertex()
        assert xs.is_first_vertex()

        self.y_ = Vertex(xs.bits.copy())
        y_tree = Tree(self.y_)

        if skip > 0 and y_tree.flip_tree():
            if xs[1] == 1 and skip <= 5:
                skip = 6 - skip
            y_string = y_tree.to_bitstring()
            y_vec = y_string + [0]
            xs = Vertex(y_vec)
            self.y_ = Vertex(xs.bits.copy())

        self.length_ = 0
        self.limit_ = limit
        seq01 = [2 * n]
        dist_to_start = skip
        final_path = False

        while True:
            flip = y_tree.flip_tree()
            y_tree.rotate()

            seq = self.y_.compute_flip_seq_0(flip)
            if self.flip_seq(seq, dist_to_start, final_path, visit_f):
                break
            assert self.y_.is_last_vertex()

            if self.flip_seq(seq01, dist_to_start, final_path, visit_f):
                break
            assert self.y_[2 * n] == 1

            seq = self.y_.compute_flip_seq_1()
            if self.flip_seq(seq, dist_to_start, final_path, visit_f):
                break
            assert self.y_.is_first_vertex()

            if self.flip_seq(seq01, dist_to_start, final_path, visit_f):
                break
            assert self.y_[2 * n] == 0

            if self.y_ == xs:
                final_path = True
                dist_to_start = skip

    def flip_seq(
        self,
        seq: List[int],
        dist_to_start: int,
        final_path: bool,
        visit_f: Callable[[List[int], int], None],
    ) -> bool:
        if (
            dist_to_start > 0
            or final_path
            or (self.length_ + len(seq) >= self.limit_ if self.limit_ >= 0 else False)
        ):
            for i in seq:
                if (final_path and dist_to_start == 0) or (
                    self.limit_ >= 0 and self.length_ == self.limit_
                ):
                    return True

                self.y_[i] = 1 - self.y_[i]
                visit_f(self.y_.bits, i)
                self.length_ += 1

                if dist_to_start > 0:
                    dist_to_start -= 1
        else:
            for i in seq:
                self.y_[i] = 1 - self.y_[i]
                visit_f(self.y_.bits, i)
            self.length_ += len(seq)
        return False


def help():
    print("""./middle [options]  compute middle levels Gray code from [Muetze,Nummenpalo]
-h                  display this help
-n{1,2,...}         list bitstrings of length 2n+1 with weight n or n+1
-l{-1,0,1,2,...}    number of bitstrings to list; -1 for full cycle
-v{0,1}^{2n+1}      initial bitstring (length 2n+1, weight n or n+1)
-s{0,1}             store and print all visited bitstrings (no=0, yes=1)
-p{0,1}             print the flip positions instead of bitstrings (no=0, yes=1)
examples:  ./middle -n2
           ./middle -n2 -v01010
           ./middle -n2 -p1
           ./middle -n10 -l50
           ./middle -n12 -s0""")


def opt_n_missing():
    print("option -n is mandatory and must come before -v", file=sys.stderr)


def opt_v_error():
    print(
        "option -v must be followed by a bitstring of length 2n+1 with weight n or n+1",
        file=sys.stderr,
    )


def visit_f_empty(y: List[int], i: int):
    pass


flip_seq_ = []


def visit_f_log(y: List[int], i: int):
    flip_seq_.append(i)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:l:v:s:p:")
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        help()
        sys.exit(1)

    n = None
    n_set = False
    limit = -1
    v = []
    v_set = False
    store_vertices = True
    print_flip_pos = False

    for o, a in opts:
        if o == "-h":
            help()
            sys.exit(0)
        elif o == "-n":
            try:
                n = int(a)
                if n < 1:
                    raise ValueError
            except ValueError:
                print(
                    "option -n must be followed by an integer from {1,2,...}",
                    file=sys.stderr,
                )
                sys.exit(1)
            v = [0] * (2 * n + 1)
            n_set = True
        elif o == "-l":
            try:
                limit = int(a)
                if limit < -1:
                    raise ValueError
            except ValueError:
                print(
                    "option -l must be followed by an integer from {-1,0,1,2,...}",
                    file=sys.stderr,
                )
                sys.exit(1)
        elif o == "-v":
            if not n_set:
                opt_n_missing()
                help()
                sys.exit(1)
            try:
                xv = list(map(int, a))
                if len(xv) != 2 * n + 1:
                    raise ValueError
                num_ones = sum(xv)
                if num_ones not in {n, n + 1}:
                    raise ValueError
            except ValueError:
                opt_v_error()
                sys.exit(1)
            v = xv
            v_set = True
        elif o == "-s":
            try:
                store_vertices = bool(int(a))
            except ValueError:
                print("option -s must be followed by 0 or 1", file=sys.stderr)
                sys.exit(1)
        elif o == "-p":
            try:
                print_flip_pos = bool(int(a))
            except ValueError:
                print("option -p must be followed by 0 or 1", file=sys.stderr)
                sys.exit(1)

    if not n_set:
        opt_n_missing()
        help()
        sys.exit(1)

    if not v_set:
        v = [1] * n + [0] * (n + 1)

    x = Vertex(v)
    visit_f = visit_f_log if store_vertices else visit_f_empty
    flip_seq_.clear()

    hc = HamCycle(x, limit, visit_f)

    if store_vertices:
        if limit != 0:
            print(x)
        for i in flip_seq_[:-1]:
            x[i] = 1 - x[i]
            print(i if print_flip_pos else x)
        if limit == len(flip_seq_):
            print("output limit reached")


if __name__ == "__main__":
    main()
