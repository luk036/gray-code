# AGENTS.md - Agent Guidelines for gray-code

## Build, Lint, and Test Commands

### Testing
```bash
# Run all tests (coverage + verbose enabled by default in setup.cfg)
pytest

# Run a single test file
pytest tests/test_skeleton.py

# Run a single test function
pytest tests/test_skeleton.py::test_fib

# With explicit coverage
pytest --cov gray_code --cov-report term-missing
```

### Linting and Formatting
```bash
# Run all pre-commit hooks (recommended before committing)
pre-commit run --all-files

# Individual tools
black src/ tests/    # Format code
isort src/ tests/    # Sort imports (black profile)
flake8 src/ tests/   # Lint (max line length: 256)
mypy src/            # Type check (Python 3.12 target)
```

### Build
```bash
tox -e build          # Build sdist + wheel
tox -e clean          # Remove build artifacts
```

### Documentation
```bash
tox -e docs           # Build HTML docs
tox -e doctests       # Run doctests
tox -e linkcheck      # Check broken links
```

## Code Style Guidelines

### Imports
- **Order**: stdlib → third-party → local (enforced by isort)
- **Tooling**: isort with Black profile (`.isort.cfg`, `known_first_party = gray_code`)
- **Local imports**: Use relative imports for subpackages (e.g., `from .edge import Edge`)
- **Future annotations**: `from __future__ import annotations` for modern `list[str]` syntax

### Formatting
- **Formatter**: Black (23.7.0)
- **Line length**: 256 characters (configured in setup.cfg)
- **Linting**: flake8 ignores E203, W503 (Black-compatible)
- **Pre-commit**: Enforced via `.pre-commit-config.yaml`

### Type Hints
- **Required**: All function parameters and return types
- **Style**: `param: type`, `-> ReturnType`; modern syntax with `from __future__ import annotations`
- **Check**: mypy with Python 3.12 target

### Naming Conventions
- **Classes**: PascalCase (e.g., `Rectangulation`, `HamCycle`, `Vertex`)
- **Enums**: PascalCase with UPPER_CASE members (e.g., `RectangulationType.GENERIC`)
- **Functions/Methods**: snake_case (e.g., `fib`, `parse_args`, `compute_ham_cycle`)
- **Private members**: Single underscore prefix

### Docstrings
- **Style**: Google-style with `Args:` / `Returns:` sections (skeleton.py) and `Examples:` doctests
- **Module docs**: Describe the module's purpose and usage
```python
def fib(n: int) -> int:
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a
```

### Error Handling
- **Preconditions**: Use `assert` for input validation (e.g., `assert n > 0`)
- **Testing**: Test error conditions with `pytest.raises`

### Testing Patterns
- **Framework**: pytest (coverage and verbose on by default in setup.cfg)
- **Coverage**: `.coveragerc` with branch coverage; `skeleton.py` omitted from coverage
- **Naming**: `test_*` prefix, descriptive names (`test_fib`, `test_main`)
- **CLI tests**: Use `capsys` fixture to assert stdout

### Pre-commit Hooks
- trailing-whitespace, check-added-large-files, check-ast, check-json,
  check-merge-conflict, check-xml, check-yaml, debug-statements,
  end-of-file-fixer, requirements-txt-fixer, mixed-line-ending,
  isort (5.12.0), black (23.7.0), flake8 (6.1.0)

### Configuration Files
- `setup.cfg`: Package metadata, pytest options, flake8 settings
- `pyproject.toml`: Build system (setuptools_scm)
- `tox.ini`: Test environments (default, build, clean, docs, doctests, linkcheck, publish)
- `.isort.cfg`: Import sorting (Black profile, `known_first_party = gray_code`)
- `mypy.ini`: Type checking (Python 3.12)
- `.coveragerc`: Branch coverage config (omits `skeleton.py`)

## Key Project Context

gray-code is a Gray code generation library:
- **Public API**: `fib(n)` — re-exported from `gray_code/__init__.py` (`from gray_code import fib`); implemented in `gray_code/skeleton.py` (also provides a `python -m gray_code.skeleton` CLI)
- **Rectangulation**: `src/rect/` package with `Rectangulation`, `Vertex`, `Edge`, `Rectangle`, `Wall` for rectangulation enumeration
- **Hamiltonian cycles**: `src/middle/` package with `HamCycle`, `Tree`, `Vertex` for flip-sequence/rotation based cycle generation
- **Key dependencies**: None at runtime (stdlib only); `importlib-metadata` fallback for Python < 3.8
- **Related**: [gray-code-cpp](https://github.com/luk036/gray-code-cpp) C++ implementation
