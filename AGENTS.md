# Agent Notes: stoch-ode (SIAM Chapter 17)

Repository for one chapter of a multi-author SIAM undergraduate textbook plus its
companion Python library. Only this chapter and its code are editable.

## Documentation standards (publisher, in force 2026-06-19)

These bind every pseudocode figure and every Python listing in `latex/`.

1. Each pseudocode figure has a body `\ref` to it and a concise, language-neutral
   prose explanation. The explanation touches every line of the block. The figure
   caption summarizes the pseudocode's purpose.
2. Every Python code block implements a pseudocode block.
3. Each Python block has a body `\ref`, placed soon after the matching pseudocode
   `\ref`, pointing to both the pseudocode figure and its explanation. Pattern:
   "In Figure \ref{fig:foo_pc}, find a function in pseudocode that inputs x and
   outputs y. It works by ... . In Figure \ref{fig:foo_py}, find the Python
   implementation."
4. When the Python diverges from the pseudocode for language-specific reasons, the
   prose explains the divergence. That explanation is not language-neutral.

Label convention: pseudocode figures end `_pc`, Python figures end `_py`.

## Pseudocode style

Ground truth is the `\procedure` templates in `latex/sections/sec_algorithm.tex`.
Pseudocode states intent abstractly with symbolic variables and named subroutine
calls, in place of a Python transliteration. The `/pseudocode/` and
`latex/pseudocode/` folders are negative examples. Treat them as a catalog of what
to do differently, and write fresh figures.

## Build and test

- LaTeX: `latexmk` from `latex/`. A change is complete once it compiles cleanly,
  with only harmless warnings.
- Python: `python -m pytest -q` (baseline passes, two slow tests deselected).
- Regenerate Python macros after renaming or adding public functions:
  `python scripts/generate_macros.py`.
