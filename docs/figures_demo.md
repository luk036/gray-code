# Figures Demo

Auto-generated figures demonstrating gray-code functionality.

## Fibonacci Sequence

```{plot} examples/plot_fibonacci.py
```

## Gray Code Sequence

```{plot} examples/plot_gray_code.py
```

### Inline Plot Example

```{plot}
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Simple Sine Wave")
plt.grid(True, alpha=0.3)
```
