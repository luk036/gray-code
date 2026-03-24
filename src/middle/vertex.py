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

    def __init__(self, x):
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

    def get_bits(self):
        """Return the bitstring representation of the vertex."""
        return self.bits_

    def __getitem__(self, i):
        """Allow accessing bits directly by index.

        Args:
            i: The index of the bit to access.

        Returns:
            The bit value (0 or 1) at the specified index.
        """
        return self.bits_[i]

    def __setitem__(self, i, value):
        """Allow setting bits directly by index.

        Args:
            i: The index of the bit to set.
            value: The value (0 or 1) to set.
        """
        self.bits_[i] = value

    def size(self):
        """Return the size of the bit vector representing the vertex."""
        return len(self.bits_)

    @property
    def bits(self):
        """Property to access bits_ as bits for compatibility."""
        return self.bits_

    def flip_bit(self, i):
        """Flip the bit at position i.

        Args:
            i: The index of the bit to flip (0 to 1 or 1 to 0).
        """
        self.bits_[i] = 1 - self.bits_[i]

    def rev_inv(self):
        """Reverse and invert the bitstring, ignoring the last bit.

        This operation reverses the bitstring (excluding the last bit)
        and then inverts each bit (0 becomes 1, 1 becomes 0).
        """
        self.bits_[:-1] = self.bits_[:-1][::-1]
        self.bits_[:-1] = [1 - bit for bit in self.bits_[:-1]]

    def is_first_vertex(self):
        """Check if the vertex is the first vertex on a path."""
        # Placeholder for actual logic
        pass

    def is_last_vertex(self):
        """Check if the vertex is the last vertex on a path."""
        # Placeholder for actual logic
        pass

    def to_first_vertex(self):
        """Move to the first vertex on a path."""
        # Placeholder for actual logic
        pass

    def to_last_vertex(self):
        """Move to the last vertex on a path."""
        # Placeholder for actual logic
        pass

    def compute_flip_seq_0(self, seq, flip):
        """Compute flip sequence 0."""
        # Placeholder for actual logic
        pass

    def compute_flip_seq_1(self, seq):
        """Compute flip sequence 1."""
        # Placeholder for actual logic
        pass

    # Additional private methods and helper functions would be defined similarly
    # ...

    # Overloading equality and inequality operators are not directly possible in Python
    # as they are in C++, but you can define __eq__ and __ne__ methods.

    def __eq__(self, other):
        """Check if two vertices are equal by comparing their bitstrings.

        Args:
            other: Another Vertex instance to compare with.

        Returns:
            True if the bitstrings are equal, False otherwise.
        """
        return self.bits_ == other.bits_

    def __ne__(self, other):
        """Check if two vertices are not equal.

        Args:
            other: Another Vertex instance to compare with.

        Returns:
            True if the bitstrings are not equal, False otherwise.
        """
        return not self.__eq__(other)

    # For output representation, you can define the __str__ or __repr__ method.
    def __repr__(self):
        """Represent the Vertex as a string."""
        return f"Vertex({self.bits_})"

    def flip_last_and_skip_to_start(self):
        """Flip the last bit and skip to the first vertex (placeholder)."""
        self.bits_[-1] = 1 - self.bits_[-1]
        return self.skip_to_first_vertex()

    def skip_to_first_vertex(self):
        """Skip to the first vertex (placeholder)."""
        return 0


# The bitstring comparison functions (bitstrings_less_than, bitstrings_equal)
# and other utility functions would also be translated similarly.
