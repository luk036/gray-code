class Wall:
    """
    Represents a wall with a start and end point.

    Attributes:
        first_ (int): The starting index of the wall.
        last_ (int): The ending index of the wall.
    """

    def __init__(self):
        """
        Initializes a new instance of `Wall` with default values.

        Example:
            >>> wall = Wall()
            >>> wall.first_, wall.last_
            (0, 0)
        """
        self.first_ = 0
        self.last_ = 0

    def init(self, first, last):
        """
        Initializes the wall with specified start and end points.

        Args:
            first (int): The starting index of the wall.
            last (int): The ending index of the wall.

        Example:
            >>> wall = Wall()
            >>> wall.init(1, 10)
            >>> wall.first_, wall.last_
            (1, 10)
        """
        self.first_ = first
        self.last_ = last


# If you're running this script directly and want to execute the test,
# uncomment the following line. However, it's recommended to run tests
# using pytest in a separate command for better practice.
# pytest.main([__file__])
