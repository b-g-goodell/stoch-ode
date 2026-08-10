# stoch-ode

Python code for simulating ordinary differential equations as discrete, random, step-by-step events.

New to Python, git, and GitHub? Start here.

## 0. Put on music

Put on music. It helps.

## 1. Get the tools

Install two programs. Pick your operating system, click, accept defaults.

- Python 3.12 or newer: https://www.python.org/downloads/
  On Windows, check the box "Add Python to PATH".
- Git: https://git-scm.com/downloads

Open a terminal. Windows: "PowerShell". Mac/Linux: "Terminal".
Test both:

    python --version
    git --version

Numbers print? Good. Error? Reinstall, reopen terminal, try again.

## 2. Copy the repo to your machine

"Clone" means copy. Run:

    git clone https://github.com/b-g-goodell/stoch-ode.git
    cd stoch-ode

Now you sit inside the repo.

## 3. Install the Python parts

The code needs three add-ons. Get them:

    python -m pip install numpy matplotlib pytest

## 4. Run something

Scripts live in `scripts/`. Each draws a figure. Run one:

    python scripts/radioactive_decay.py

A PDF lands in `latex/figures/`. Open it. That is the code working.

Try the others: `logistic_growth.py`, `epidemiology.py`, `saline_tank.py`,
`allee_effect.py`.

## 5. Check the code is healthy

Tests prove the code still works. Run them all:

    python -m pytest -q

Green means good.

## What lives where

    scripts/                 small programs that make book figures
    simulation_frameworks/   the example models (decay, growth, disease, ...)
    tools/                   the simulation engine and plotting code
    tests/                   automatic checks
    latex/                   the book chapter text

## The book (optional)

The chapter is written in LaTeX. To build the PDF you need a LaTeX
install (TeX Live or MiKTeX). Then:

    cd latex
    latexmk -pdf main.tex

Out comes `main.pdf`. Skip this if you only want the code.

## Words you just met

- repo: a project folder tracked by git.
- clone: copy a repo to your computer.
- terminal: a window where you type commands.
- script: a file of Python you run.
- test: code that checks other code.

## Learn the basics

- Python: https://docs.python.org/3/tutorial/
- git: https://git-scm.com/book/en/v2 (read chapters 1 and 2)
- GitHub: https://docs.github.com/en/get-started

Read a little. Run the code. Read more. Repeat. Life is good, or at least tolerable.

## When commands break

Two common problems.
 - `python` says "command not found"? On Mac and Linux the name is often `python3` or `python3.12` for our version. Same for pip: `python3 -m pip ...` or `python3.12 -m pip ...`.
 - `pip install` says "externally-managed-environment"? Your system wants you to play in a sandbox. Use `python -m venv .venv` to make a sandbox. To turn it on in Windows PowerShell, use `.venv\Scripts\Activate.ps1`, in Mac/Linux, use `source .venv/bin/activate`. If `(.venv)` is at the line start, the sandbox is on. Then redo step 3 above. 

New terminal forgets the sandbox. Turn it on again before you work.