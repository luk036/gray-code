from collections import deque


def bitstrings_less_than(x, y):
    return any(a < b for a, b in zip(x, y))


def bitstrings_equal(x, y):
    return all(a == b for a, b in zip(x, y))


# Now, let's write some pytest tests for these functions.


# To run these tests, you would use the pytest command in your terminal:
# pytest <name_of_your_script>.py
class Tree:
    def __init__(self, xv):
        assert len(xv) % 2 == 1

        self.num_vertices = (len(xv) - 1) // 2 + 1
        self.root = 0
        self.children = [deque() for _ in range(self.num_vertices)]
        self.parent = [0] * self.num_vertices

        u = 0
        n = 1
        for i in range(len(xv) - 1):
            if xv[i] == 1:
                self.children[u].append(n)
                self.parent[n] = u
                u = n
                n += 1
            else:
                u = self.parent[u]
        assert n == self.num_vertices

    def deg(self, u):
        assert u < self.num_vertices
        return len(self.children[u]) + (u != self.root)

    def num_children(self, u):
        return len(self.children[u])

    def ith_child(self, u, i):
        return self.children[u][i]

    # ... Other methods such as is_tau_preimage, is_tau_image, tau, tau_inverse,
    # move_leaf, rotate, rotate_to_vertex, rotate_children_default, rotate_children,
    # flip_tree, root_canonically, compute_center, min_string_rotation, and
    # to_bitstring need to be implemented with consideration for Pythonic practices
    # and possibly utilizing external libraries or custom implementations for
    # functionalities like bitstring comparisons.

    def is_tau_preimage(self):
        if self.num_vertices < 3:
            return False
        u = self.ith_child(self.root, 0)
        if self.num_children(u) == 0:
            return False
        v = self.ith_child(u, 0)
        if self.num_children(v) != 0:
            return False
        return True

    def is_tau_image(self):
        if (
            self.num_vertices < 3
            or self.num_children(self.root) < 2
            or self.num_children(self.ith_child(self.root, 0)) > 0
        ):
            return False
        return True

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

    def move_leaf(self, leaf, new_parent, pos):
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
        first = self.children[self.root].popleft()
        if first is not None:
            self.children[u].append(first)
        self.children[u].append(self.root)
        self.root = u

    def rotate_to_vertex(self, u):
        while self.root != u:
            self.rotate()

    def rotate_children_default(self):
        self.rotate_children(1)

    def rotate_children(self, k):
        queue = deque(self.children[self.root])
        for _ in range(k):
            if queue:
                front = queue.popleft()
                queue.append(front)
        self.children[self.root] = queue

    def flip_tree(self):
        if self.is_tau_preimage() and self.is_flip_tree_tau():
            self.tau()
            return True
        elif self.is_tau_image():
            self.tau_inverse()
            if self.is_flip_tree_tau():
                self.tau()  # undo tau^{-1}
                return False
            return True
        return False

    # The following methods (ith_child, num_children) need to be implemented based on specific logic
    # since their implementations are not provided in the original Rust code.

    @staticmethod
    def is_flip_tree_tau(tree):
        # Static method implementation depending on specific conditions
        pass

    def root_canonically(self):
        c1, c2 = self.compute_center()
        if c2 is not None:  # centers are different
            num_bits = 2 * (self.num_vertices - 1)
            x1 = [0] * num_bits
            x2 = [0] * num_bits
            self.rotate_to_vertex(c1)
            while self.ith_child(self.root, 0) != c2:
                self.rotate_children_default()
            self.to_bitstring(x1)

            self.rotate()
            self.rotate_children(self.num_children(self.root) - 1)
            assert self.root == c2 and self.ith_child(self.root, 0) == c1
            self.to_bitstring(x2)

            if bitstrings_less_than(x1[:num_bits], x2[:num_bits]):
                self.rotate()
                self.rotate_children(self.num_children(self.root) - 1)
                assert self.root == c1 and self.ith_child(self.root, 0) == c2

        else:  # centers are the same
            num_bits = 2 * (self.num_vertices - 1)
            x = [0] * num_bits
            self.rotate_to_vertex(c1)
            self.to_bitstring(x)

            subtree_count = [0] * num_bits
            c, depth = 0, 0
            for i in range(num_bits):
                if x[i] == 1:
                    depth += 1
                else:
                    depth -= 1
                subtree_count[i] = c
                if depth == 0:
                    c += 1
            assert c == self.num_children(self.root), "Inconsistent subtree count"

            k = self.min_string_rotation(x, num_bits)
            self.rotate_children(subtree_count[k])

    def min_string_rotation(self, x, length):
        # Placeholder for finding minimum string rotation logic
        pass

    def compute_center(self):
        degs = [0] * self.num_vertices
        leaves = deque()

        for i in range(self.num_vertices):
            degs[i] = self.deg(i)
            if degs[i] == 1:
                leaves.append(i)

        num_vertices_remaining = self.num_vertices

        while num_vertices_remaining > 2:
            for _ in range(len(leaves)):
                u = leaves.popleft()
                for child in self.children[u]:
                    degs[child] -= 1
                    if degs[child] == 1:
                        leaves.append(child)
                if u != self.root:
                    parent = self.parent[u]
                    degs[parent] -= 1
                    if degs[parent] == 1:
                        leaves.append(parent)
            num_vertices_remaining -= len(leaves)

        assert 1 <= len(leaves) <= 2

        c1 = leaves.popleft()
        c2 = leaves.popleft() if leaves else None
        return c1, c2


# pytest test function example
def test_tree_operations():
    # Initialize a test Tree instance with dummy values and test root_canonically method
    pass  # Implement test cases here
