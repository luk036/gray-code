"""
Fibonacci Sequence
==================

Plot of the first 20 Fibonacci numbers.
"""
from gray_code.skeleton import fib
import matplotlib.pyplot as plt

n_vals = list(range(1, 21))
fib_vals = [fib(n) for n in n_vals]

plt.figure(figsize=(7, 5))
plt.plot(n_vals, fib_vals, 'bo-', linewidth=2, markersize=6)
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('F(n)')
plt.title('First 20 Fibonacci Numbers (log scale)')
plt.grid(True, alpha=0.3)
