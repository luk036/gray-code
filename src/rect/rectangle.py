from dataclasses import dataclass


@dataclass
class Rectangle:
    nwest: int = 0
    neast: int = 0
    swest: int = 0
    seast: int = 0

    def init(self, neast: int, seast: int, swest: int, nwest: int):
        self.nwest = nwest
        self.neast = neast
        self.swest = swest
        self.seast = seast
