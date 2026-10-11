"""Pure detection functions (TRD sections 9-11). No I/O, no scoring."""

from itertools import groupby

from src.config import REPEAT_RUN_MIN, SEQUENCE_RUN_MIN


def _is_ascii_letter(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z"


def _is_ascii_digit(char: str) -> bool:
    return "0" <= char <= "9"


def count_character_classes(password: str) -> dict[str, bool]:
    """Report which classes are present. 'special' is anything not a-z, A-Z or 0-9."""
    return {
        "lowercase": any("a" <= c <= "z" for c in password),
        "uppercase": any("A" <= c <= "Z" for c in password),
        "digit": any(_is_ascii_digit(c) for c in password),
        "special": any(not (_is_ascii_letter(c) or _is_ascii_digit(c)) for c in password),
    }


def count_repeat_runs(password: str) -> int:
    """Count maximal runs of at least REPEAT_RUN_MIN identical characters (case-sensitive)."""
    return sum(1 for _, group in groupby(password) if len(list(group)) >= REPEAT_RUN_MIN)


def _step(previous: str, current: str) -> int | None:
    """Return +1/-1 if two characters are consecutive digits or ASCII letters, else None."""
    if _is_ascii_digit(previous) and _is_ascii_digit(current):
        difference = ord(current) - ord(previous)
    elif _is_ascii_letter(previous) and _is_ascii_letter(current):
        difference = ord(current.lower()) - ord(previous.lower())
    else:
        return None
    return difference if difference in (1, -1) else None


def count_sequence_runs(password: str) -> int:
    """Count maximal ascending or descending runs of at least SEQUENCE_RUN_MIN characters."""
    runs = 0
    length = 1
    direction = 0
    for previous, current in zip(password, password[1:]):
        step = _step(previous, current)
        if step is not None and step == direction:
            length += 1
            continue
        if length >= SEQUENCE_RUN_MIN:
            runs += 1
        if step is None:
            length, direction = 1, 0
        else:
            length, direction = 2, step
    if length >= SEQUENCE_RUN_MIN:
        runs += 1
    return runs


def check_common(password: str, common_set: frozenset[str]) -> str:
    """Return 'exact', 'base' (after removing trailing non-letters) or 'none'."""
    folded = password.casefold()
    if folded in common_set:
        return "exact"
    end = len(password)
    while end > 0 and not password[end - 1].isalpha():
        end -= 1
    base = password[:end].casefold()
    if base and base in common_set:
        return "base"
    return "none"
