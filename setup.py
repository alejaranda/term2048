import re
from pathlib import Path

from setuptools import find_packages, setup

ROOT_DIR = Path(__file__).parent
version_path = ROOT_DIR / "src" / "__init__.py"
version_file = version_path.read_text(encoding="utf-8")
version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', version_file)
if not version_match:
    raise RuntimeError("Version string not found in src/__init__.py")
version = version_match.group(1)

setup(
    name="term2048",
    version=version,
    description="2048 game playable in terminal",
    author_email="alejandro.arancibia.aranda@gmail.com",
    url="https://github.com/alejyoo/term2048",
    packages=find_packages(where="src"),
    py_modules=["board", "game", "cli"],
    package_dir={"": "src"},
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "term2048=cli:main",
        ],
    },
)
