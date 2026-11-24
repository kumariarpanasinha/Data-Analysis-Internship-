"""Verify Python environment and required data analytics libraries."""

import importlib
import sys

REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "plotly",
    "sqlalchemy",
    "jupyter",
]


def main() -> int:
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(pkg)
            version = getattr(mod, "__version__", "installed")
            print(f"[OK] {pkg}: {version}")
        except ImportError as exc:
            print(f"[MISSING] {pkg}: {exc}")
            missing.append(pkg)

    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        return 1

    print("\nAll required packages are installed and ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

