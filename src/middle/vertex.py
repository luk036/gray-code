from typing import List


class Vertex:
    """Represents a vertex in a binary tree encoded as a bitstring.

    The bitstring has odd length (at least 3) and encodes the structure
    of a rooted binary tree where 1 represents moving to a child and
    0 represents moving back to the parent.

    Attributes:
        bits_: The bitstring representing the vertex/tree structure.

    Examples:
        >>> v = Vertex([1, 0, 1, 0, 1])
        >>> v.get_bits()
        [1, 0, 1, 0, 1]
    """

    def __init__(self, x: List[int]) -> None:
        """Initialize a Vertex instance with a bitstring.

        Args:
            x: A bitstring (list of 0s and 1s) with odd length (at least 3).

        Raises:
            AssertionError: If bitstring length is not odd or less than 3.

        Example:
            >>> v = Vertex([1, 0, 1, 0, 1])
            >>> v.get_bits()
            [1, 0, 1, 0, 1]
        """
        assert len(x) % 2 == 1, "Bitstring length must be odd."
        assert len(x) >= 3, "Bitstring length must be at least 3."
        self.bits_ = x

    def get_bits(self) -> List[int]:
        return self.bits_

    def __getitem__(self, i: int) -> int:
        """Allow accessing bits directly by index.

        Args:
            i: The index of the bit to access.

        Returns:
            The bit value (0 or 1) at the specified index.
        """
        return self.bits_[i]

    def __setitem__(self, i: int, value: int) -> None:
        """Allow setting bits directly by index.

        Args:
            i: The index of the bit to set.
            value: The value (0 or 1) to set.
        """
        self.bits_[i] = value

    def size(self) -> int:
        return len(self.bits_)

    @property
    def bits(self) -> List[int]:
        """Property to access the internal bitstring for compatibility."""
        return self.bits_

    def flip_bit(self, i: int) -> None:
        """Flip the bit at position i.

        Args:
            i: The index of the bit to flip (0 to 1 or 1 to 0).
        """
        self.bits_[i] = 1 - self.bits_[i]

    def rev_inv(self) -> None:
        """Reverse and invert the bitstring, ignoring the last bit.

        This operation reverses the bitstring (excluding the last bit)
        and then inverts each bit (0 becomes 1, 1 becomes 0).
        """
        self.bits_[:-1] = self.bits_[:-1][::-1]
        self.bits_[:-1] = [1 - bit for bit in self.bits_[:-1]]

    def is_first_vertex(self) -> bool:
        """Check if the vertex is the first vertex on a path."""
        return True

    def is_last_vertex(self) -> None:
        """Check if the vertex is the last vertex on a path."""
        # Placeholder for actual logic
        pass

    def to_first_vertex(self) -> None:
        """Move to the first vertex on a path."""
        # Placeholder for actual logic
        pass

    def to_last_vertex(self) -> None:
        """Move to the last vertex on a path."""
        # Placeholder for actual logic
        pass

    def compute_flip_seq_0(self, seq: List[int], flip: bool) -> None:
        """Compute flip sequence 0."""
        # Placeholder for actual logic
        pass

    def compute_flip_seq_1(self, seq: List[int]) -> None:
        """Compute flip sequence 1."""
        # Placeholder for actual logic
        pass

    # Additional private methods and helper functions would be defined similarly
    # ...

    # Overloading equality and inequality operators are not directly possible in Python
    # as they are in C++, but you can define __eq__ and __ne__ methods.

    def __eq__(self, other: object) -> bool:
        """Check if two vertices are equal by comparing their bitstrings.

        Args:
            other: Another Vertex instance to compare with.

        Returns:
            True if the bitstrings are equal, False otherwise.
        """
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.bits_ == other.bits_

    def __ne__(self, other: object) -> bool:
        """Check if two vertices are not equal.

        Args:
            other: Another Vertex instance to compare with.

        Returns:
            True if the bitstrings are not equal, False otherwise.
        """
        return not self.__eq__(other)

    # For output representation, you can define the __str__ or __repr__ method.
    def __repr__(self) -> str:
        """Represent the Vertex as a string."""
        return f"Vertex({self.bits_})"

    def flip_last_and_skip_to_start(self) -> int:
        """Flip the last bit and skip to the first vertex (placeholder)."""
        self.bits_[-1] = 1 - self.bits_[-1]
        return self.skip_to_first_vertex()

    def skip_to_first_vertex(self) -> int:
        """Skip to the first vertex (placeholder)."""
        return 0


# The bitstring comparison functions (bitstrings_less_than, bitstrings_equal)
# and other utility functions would also be translated similarly.
