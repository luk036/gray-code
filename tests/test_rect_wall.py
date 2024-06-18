from rect.wall import Wall


def test_wall_default():
    wall = Wall()
    assert wall.first == 0
    assert wall.last == 0


def test_wall_init():
    wall = Wall()
    wall.init(3, 5)
    assert wall.first == 3
    assert wall.last == 5
