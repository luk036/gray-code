# Changelog

## Version 0.2 (2026-10-09)

### Bug Fixes
- **`skeleton.py` restored as core library**: Reverted its deletion — `skeleton.py` holds the core `fib` implementation, not dead boilerplate. (#2acb22d)
- **mypy type errors**: Resolved type errors across the tree/vertex modules. (#5afa17f)

### Testing & Code Quality
- **Coverage raised 90% → 100%**: Excluded `skeleton.py` and the version fallback from coverage measurement. (#e3327f7)
- **New test suites**: Added unit tests for the `vertex`, `tree`, and `rect` modules plus middle-vertex extras. (#327438b, #06f6c19)

### Code Cleanup
- **Removed dead code & boilerplate**: Deleted `rect_ai.py` (1,643 lines of AI scratch), the unused `requirements/` files, the duplicate `LICENSE`, and PyScaffold placeholders; cleaned the configs. (#93015d9, #0110169)
- **Removed AI slop**: Stripped boilerplate from docstrings and comments. (#277a395)
- **Style**: Fixed stray comment indentation in `tree.py`. (#cfe8c38)

### Documentation
- **AGENTS.md**: Added agent guidelines for the repository. (#b33221b)
- **Sphinx docs**: Enabled `plot_directive` and `sphinxcontrib.svgbob`, and added Fibonacci / Gray-code example plots plus a figures demo. (#4a6f85f)

### Build & CI
- **CI repair**: Fixed the broken `entry_points` configuration and remaining `skeleton` imports. (#28ecdc5)
