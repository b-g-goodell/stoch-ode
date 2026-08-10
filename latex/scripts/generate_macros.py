import ast
import sys
from pathlib import Path

SCAN_DIRS = ["simulation_frameworks", "tools", "scripts"]
SKIP_FILES = {"__init__.py"}
SKIP_SUFFIX = "_red.py"
SKIP_NAMES = {"main"}
OUTPUT = Path("latex/python_macros.tex")


def to_macro_name(snake):
    return "".join(word.capitalize() for word in snake.split("_"))


def extract_functions(py_file):
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        print(f"warning: skipping {py_file} ({exc})", file=sys.stderr)
        return []
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and not node.name.startswith("_")
        and node.name not in SKIP_NAMES
    ]


def main():
    root = Path(__file__).resolve().parent.parent
    seen = {}
    lines = [
        "% Auto-generated. Do not edit manually.\n",
        "% Regenerate: python scripts/generate_macros.py\n",
    ]
    for dirname in SCAN_DIRS:
        scan_path = root / dirname
        if not scan_path.exists():
            continue
        for py_file in sorted(scan_path.rglob("*.py")):
            if py_file.name in SKIP_FILES or py_file.name.endswith(SKIP_SUFFIX):
                continue
            for func_name in extract_functions(py_file):
                macro = to_macro_name(func_name)
                if macro in seen:
                    if seen[macro] != str(py_file):
                        print(f"warning: duplicate macro \\{macro} from {py_file} "
                              f"(first seen in {seen[macro]})", file=sys.stderr)
                    continue
                seen[macro] = str(py_file)
                escaped = func_name.replace("_", "\\_")
                lines.append(f"\\newcommand{{\\{macro}}}{{${{\\tt {escaped}}}$}}\n")
    output_path = root / OUTPUT
    output_path.write_text("".join(lines), encoding="utf-8")
    print(f"wrote {len(seen)} macros to {output_path}")


if __name__ == "__main__":
    main()
