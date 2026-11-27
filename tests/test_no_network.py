"""Guard test for hard rule 1: the app code must never touch the network.

Scans every .py file under src/ and fails if it finds a network import, a
urlopen call, or a string literal that starts with http:// or https://.
Comments are ignored, so a comment may mention a URL or an import.
"""

import ast
import io
import tokenize
from pathlib import Path

# The folder we protect: src/ next to this tests/ folder.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"

# Plain text that must not appear in executable code.
FORBIDDEN_SNIPPETS = (
    "import requests",
    "import urllib",
    "import http.client",
    "import socket",
    "urlopen",
)


def python_files():
    """Every .py file under src/, skipping Python's cache folders."""
    return sorted(
        path for path in SRC_DIR.rglob("*.py") if "__pycache__" not in path.parts
    )


def strip_comments(text):
    """Return (lines, string_tokens) with comments blanked out.

    Line numbers are preserved, so a failure can point at the exact line.
    """
    lines = text.splitlines()
    string_tokens = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.COMMENT:
                row, start_col = token.start
                _, end_col = token.end
                line = lines[row - 1]
                lines[row - 1] = line[:start_col] + line[end_col:]
            elif token.type == tokenize.STRING:
                string_tokens.append(token)
    except (tokenize.TokenError, IndentationError):
        # Source that does not tokenize is still scanned line by line.
        pass
    return lines, string_tokens


def string_literal_starts_with_url(token_text):
    """True if this string literal's value begins with http:// or https://."""
    try:
        value = ast.literal_eval(token_text)
    except (ValueError, SyntaxError):
        # e.g. an f-string; fall back to a plain text check after the quote.
        return 'http://' in token_text or 'https://' in token_text
    if not isinstance(value, str):
        return False
    return value.lower().startswith(("http://", "https://"))


def test_src_folder_is_scanned():
    """Make sure the scan is not passing simply because it found no files."""
    assert python_files(), f"no .py files found under {SRC_DIR}"


def test_no_network_code_in_src():
    """No network import, urlopen, or hard-coded URL in any src/ Python file."""
    problems = []

    for path in python_files():
        text = path.read_text(encoding="utf-8")
        lines, string_tokens = strip_comments(text)

        for line_number, line in enumerate(lines, start=1):
            for snippet in FORBIDDEN_SNIPPETS:
                if snippet in line:
                    problems.append(
                        f"{path}:{line_number}: found {snippet!r}"
                    )

        for token in string_tokens:
            if string_literal_starts_with_url(token.string):
                problems.append(
                    f"{path}:{token.start[0]}: URL string literal "
                    f"{token.string.strip()!r} (URLs are allowed in comments only)"
                )

    assert not problems, "Network code found in src/:\n" + "\n".join(problems)
