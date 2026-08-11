# stoch-ode

Python code for simulating ordinary differential equations as discrete, random, step-by-step events.

New to Python, git, and GitHub? Start here. Do the steps in order. Each step says what success looks like. Nothing below assumes you have done any of this before.

## 0. Put on music

Put on music. It helps.

## 1. Open a terminal

A terminal is a window where you type commands and the computer answers in text. All the commands below get typed there, one line at a time, each followed by the Enter key.

- Windows: press the Windows key, type `powershell`, press Enter. A window titled "Windows PowerShell" opens.
- Mac: press Command+Space, type `terminal`, press Enter.
- Linux: press Ctrl+Alt+T, or find "Terminal" in the applications menu.

Keep it open. When a step below says "run" something, it means: type it in this window, press Enter, and wait for the blinking prompt to come back.

## 2. Get the tools

Install two programs. On each page, pick your operating system, download, run the installer, accept the defaults.

- Python 3.12 or newer: https://www.python.org/downloads/
  On Windows, one exception to "accept the defaults": on the installer's first screen, check the box "Add python.exe to PATH".
- Git: https://git-scm.com/downloads

Installs are only visible to terminals opened after them. So close your terminal, open a new one (step 1 again), and test both tools:

    python --version
    git --version

Each prints a version number? Good. An error like "not recognized" or "command not found"? See "When commands break" at the bottom.

## 3. Copy the repo to your machine

A "repo" (repository) is a project folder tracked by git, and "clone" means copy it to your machine. Run:

    git clone https://github.com/b-g-goodell/stoch-ode.git
    cd stoch-ode

The first command creates a folder named `stoch-ode` and downloads the project into it. The second moves your terminal inside that folder. Every later step happens inside it.

## 4. Install the Python parts

The code needs three add-ons. Get them:

    python -m pip install numpy matplotlib pytest

A lot of text scrolls by. That is normal. It finishes and the prompt comes back without red error text? Good.

## 5. Run something

Small programs live in `scripts/`. Five of them draw figures from the book chapter. (The sixth file there, `generate_macros.py`, is plumbing for the book build. Ignore it.) Run one:

    python scripts/radioactive_decay.py

It prints nothing and finishes in a few seconds. When the prompt comes back, open the folder `stoch-ode/latex/figures` in your file browser (Windows: File Explorer, Mac: Finder). A file `radioactive_decay.pdf` sits there with a fresh timestamp. Open it and look at it. That is the code working.

Try the others the same way: `logistic_growth.py`, `epidemiology.py`, `saline_tank.py`, `allee_effect.py`. Each also prints nothing and finishes in seconds, and some write two or three PDFs into `latex/figures` at once.

## 6. Check the code is healthy

Tests are code that checks the other code still works. Run them all, from the `stoch-ode` folder:

    python -m pytest -q

A short wait, then a green line like "55 passed, 2 deselected". "Passed" means healthy, and a "deselected" count is fine: those tests are skipped on purpose. Red "failed" lines mean something is wrong. Nothing to fix right now either way. This command is how you check.

## What lives where

    scripts/                 small programs that make the book figures
    simulation_frameworks/   the example models (growth, disease, tank mixing, ...)
    tools/                   the simulation engine and plotting code
    tests/                   automatic checks
    latex/                   the book chapter: LaTeX text, figures, build files

## The book (optional)

The chapter is written in LaTeX, a typesetting system that turns text files into a PDF. Inside the publisher's book, `latex/main.tex` is a fragment the book builds for itself, so to read the chapter you build it yourself. First install LaTeX. It is a large install, gigabytes, and takes a while.

- Windows or Mac: MiKTeX, from https://miktex.org/download
- Linux: TeX Live. On Ubuntu or Debian: `sudo apt install texlive-full`

Close your terminal, open a new one, and from the `stoch-ode` folder run:

    cd latex
    latexmk -pdf standalone.tex

The first build takes a few minutes and prints walls of text. MiKTeX may ask permission to install missing packages: let it. When the prompt comes back, the file `standalone.pdf` sits in the `latex` folder: the whole chapter. Run `cd ..` to move back up to the `stoch-ode` folder. Skip this whole section if you only want the code.

## Words you just met

- repo: a project folder tracked by git.
- clone: copy a repo to your computer.
- terminal: a window where you type commands.
- prompt: the line the terminal shows when it is ready for a command.
- script: a file of Python you run.
- test: code that checks other code.

## Learn the basics

- Python: https://docs.python.org/3/tutorial/
- git: https://git-scm.com/book/en/v2 (read chapters 1 and 2)
- GitHub: https://docs.github.com/en/get-started

Read a little. Run the code. Read more. Repeat. Life is good, or at least tolerable.

## When commands break

Three common problems.

- `python` says "command not found" or "not recognized"? On Windows, rerun the Python installer and check the "Add python.exe to PATH" box. On Mac and Linux the name is often `python3`, so try `python3 --version` and, if that works, type `python3` wherever this file says `python` (and `python3 -m pip ...` for pip).
- You opened a new terminal and it forgot everything? Terminals forget the folder they were in. Run `cd stoch-ode` (or `cd` followed by wherever you cloned it) to get back inside the repo.
- `pip install` says "externally-managed-environment"? Your system wants you to play in a sandbox. Run `python -m venv .venv` once to make one. Turn it on with `.venv\Scripts\Activate.ps1` (Windows PowerShell) or `source .venv/bin/activate` (Mac/Linux). If `(.venv)` appears at the start of the line, the sandbox is on. Redo step 4. A new terminal forgets the sandbox: turn it on again before you work.
## Notes on this copy (for the editorial round trip, not for students)

Everything above this section describes the public GitHub repository as
students use it, and its paths are that repository's paths. This copy
differs from it in two deliberate ways, both so the chapter compiles
inside the book:

- The Python packages (scripts, simulation_frameworks, tools) live under
  latex/, where the book build can reach them for the code listings.
- Every path LaTeX compiles (section inputs, figures, listing sources)
  is written from the book root: 17StochasticODEs/stoch-ode/latex/....
  The student copy spells the same paths relative to its latex/ folder.

Two maintainer scripts, kept outside the repository, keep the two copies
honest:

- A checker compares this copy against the student copy. The LaTeX must
  match apart from comments and the path spellings above, and every
  Python file under latex/ must be byte-identical to its student-side
  twin. The listings quote line ranges, so a drifted copy silently
  prints the wrong lines.
- A porter rewrites the path spellings mechanically in either direction,
  so an edit made on one copy lands on the other without hand-editing
  paths.

Content edits start on the student side and are ported here. Edits from
the editor land here first and are ported back.
