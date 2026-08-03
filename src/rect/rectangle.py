class Rectangle:
    """
    Represents a rectangle with four boundaries defined by their coordinates.

    Attributes:
        nwest (int): The northwest coordinate.
        neast (int): The northeast coordinate.
        swest (int): The southwest coordinate.
        seast (int): The southeast coordinate.
    """

    def __init__(self) -> None:
        self.nwest = 0
        self.neast = 0
        self.swest = 0
        self.seast = 0

    def init(self, neast: int, seast: int, swest: int, nwest: int) -> None:
        """
        Initializes the rectangle with specified coordinates.

        Args:
            neast (int): The northeast coordinate.
            seast (int): The southeast coordinate.
            swest (int): The southwest coordinate.
            nwest (int): The northwest coordinate.
        """
        self.nwest = nwest
        self.neast = neast
        self.swest = swest
        self.seast = seast


# DocTest
if __name__ == "__main__":
    import doctest

    doctest.testmod()
