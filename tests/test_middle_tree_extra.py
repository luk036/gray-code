"""Additional tests for the middle.tree module covering the Tree class."""

from middle.tree import Tree


def test_tree_init_simple() -> None:
    xv = [1, 0, 1, 0, 1]
    tree = Tree(xv)
    assert tree.num_vertices == 3
    assert tree.root == 0


def test_tree_init_larger() -> None:
    xv = [1, 1, 0, 1, 0, 0, 1]
    tree = Tree(xv)
    assert tree.num_vertices == 4


def test_tree_deg_root() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    assert tree.deg(0) == len(tree.children[0])  # root has no parent


def test_tree_num_children() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    for i in range(tree.num_vertices):
        assert tree.num_children(i) == len(tree.children[i])


def test_tree_ith_child() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    if tree.num_children(0) > 0:
        child = tree.ith_child(0, 0)
        assert 0 <= child < tree.num_vertices


def test_tree_compute_center_single() -> None:
    xv = [1, 0, 1, 0, 1]
    tree = Tree(xv)
    c1, c2 = tree.compute_center()
    assert c1 is not None
    assert c1 < tree.num_vertices


def test_tree_is_tau_preimage() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    result = tree.is_tau_preimage()
    assert isinstance(result, bool)


def test_tree_is_tau_image() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    result = tree.is_tau_image()
    assert isinstance(result, bool)


def test_tree_flip_tree() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    result = tree.flip_tree()
    assert isinstance(result, bool)


def test_tree_rotate_children() -> None:
    xv = [1, 1, 1, 0, 0, 0, 1]
    tree = Tree(xv)
    tree.rotate_children(1)
    assert True  # no exception raised


def test_tree_rotate_children_default() -> None:
    xv = [1, 1, 0, 0, 1]
    tree = Tree(xv)
    tree.rotate_children_default()
    assert True  # no exception raised
