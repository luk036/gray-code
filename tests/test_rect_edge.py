from rect.edge import Edge, EdgeDir


def test_edge_init():
    edge = Edge()
    edge.init(EdgeDir.HOR, 1, 2, 3, 4, 5, 6, 7)

    assert edge.dir == EdgeDir.HOR
    assert edge.tail == 1
    assert edge.head == 2
    assert edge.prev == 3
    assert edge.next == 4
    assert edge.left == 5
    assert edge.right == 6
    assert edge.wall == 7


# Run the tests with: pytest <your_script_name>.py
