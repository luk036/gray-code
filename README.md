[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![Documentation Status](https://readthedocs.org/projects/gray-code/badge/?version=latest)](https://gray-code.readthedocs.io/en/latest/?badge=latest)
[![Coveralls](https://img.shields.io/coveralls/github/luk036/gray-code/main.svg)](https://coveralls.io/r/luk036/gray-code)
[![PyPI-Server](https://img.shields.io/pypi/v/gray-code.svg)](https://pypi.org/project/gray-code/)

# gray-code

> Gray code Generation

A Python library for generating Gray codes, useful for:
- **Error correction** - Only one bit changes between consecutive values
- **Digital communications** - Reduced switching noise
- **Karnaugh maps** - Simplifying boolean algebra

## Installation

```bash
pip install gray-code
```

## Quick Start

```python
from gray_code import fib

# Example: Calculate Fibonacci numbers
result = fib(10)  # Returns 55
```

## API Overview

### Core Functions

- `fib(n)` - Calculate the n-th Fibonacci number (example)

## See Also

- [gray-code-cpp](https://github.com/luk036/gray-code-cpp) - C++ implementation

## License

This project is licensed under the MIT license - see the LICENSE file for details.

## 👉 Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
