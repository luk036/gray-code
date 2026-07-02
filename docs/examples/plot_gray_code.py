"""
Gray Code Sequence
==================

Visualization of 4-bit binary reflected Gray code sequence.
"""
import matplotlib.pyplot as plt


def gray_code(n):
    """Generate n-bit Gray code sequence."""
    return [i ^ (i >> 1) for i in range(1 << n)]


n_bits = 4
codes = gray_code(n_bits)

plt.figure(figsize=(8, 5))
for i, code in enumerate(codes):
    bits = [(code >> j) & 1 for j in range(n_bits - 1, -1, -1)]
    for j, b in enumerate(bits):
        if b:
            plt.plot([i, i], [j, j + 0.8], 'b-', linewidth=2)
            plt.plot(i, j + 0.4, 'bo', markersize=4)

plt.xlabel('Sequence Index')
plt.ylabel('Bit Position')
plt.yticks(range(n_bits), [f'Bit {n_bits-1-i}' for i in range(n_bits)])
plt.title(f'{n_bits}-bit Gray Code Sequence')
plt.xlim(-0.5, len(codes) - 0.5)
plt.grid(True, alpha=0.3)
