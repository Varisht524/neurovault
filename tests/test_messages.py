"""Tests for src/messages.py: no banned words anywhere in user-facing text."""

import re

import src.messages as messages

# Whole-word, case-insensitive match, as required by the brief.
BANNED_WORDS = ("diagnosis", "risk", "normal", "abnormal", "better", "worse")
BANNED_PATTERN = re.compile(
    r"\b(" + "|".join(BANNED_WORDS) + r")\b",
    flags=re.IGNORECASE,
)

# The one string that may contain "diagnosis", and only exactly as written.
ALLOWED_FIXED_NOTE = (
    "This tool is not a diagnosis. If you are worried about memory changes, "
    "talk to a doctor."
)


def string_constants():
    """Return (name, value) for every module-level uppercase string in messages.py."""
    found = []
    for name in dir(messages):
        if not name.isupper():
            continue
        value = getattr(messages, name)
        if isinstance(value, str):
            found.append((name, value))
    return found


def test_no_banned_words_in_messages():
    """Every string constant is free of banned words except the agreed FIXED_NOTE."""
    strings = string_constants()
    # Guard against a course that quietly finds nothing and passes for free.
    assert len(strings) >= 6, "expected at least the six required message constants"

    problems = []
    for name, value in strings:
        for match in BANNED_PATTERN.finditer(value):
            word = match.group(0).lower()
            is_allowed = (
                name == "FIXED_NOTE"
                and word == "diagnosis"
                and value == ALLOWED_FIXED_NOTE
            )
            if not is_allowed:
                problems.append(f"{name}: found {word!r} in {value!r}")

    assert not problems, "Banned words in user-facing text:\n" + "\n".join(problems)


def test_fixed_note_is_exactly_the_agreed_text():
    """The only allowed exception stays word-for-word, so the test cannot drift."""
    assert messages.FIXED_NOTE == ALLOWED_FIXED_NOTE
