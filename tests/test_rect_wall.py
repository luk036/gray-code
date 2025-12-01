from rect.wall import Wall


def test_wall_initialization() -> None:
    """
    Ensures that the Wall's init method correctly sets the start and end points.
    """
    wall = Wall()
    wall.init(1, 10)
    assert wall.first_ == 1, "Start index not set correctly."
    assert wall.last_ == 10, "End index not set correctly."
