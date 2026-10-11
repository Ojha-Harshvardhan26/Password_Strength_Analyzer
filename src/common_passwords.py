"""Loads the local common-password list. Fails closed if it cannot be used."""

from pathlib import Path


class CommonListError(Exception):
    """Raised when the common-password list is missing, unreadable or empty."""


def load_common_passwords(path: str | Path) -> frozenset[str]:
    """Read one lowercase entry per line; blank lines are ignored."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise CommonListError("Common-password list could not be read.") from error
    entries = frozenset(line.strip().casefold() for line in text.splitlines() if line.strip())
    if not entries:
        raise CommonListError("Common-password list is empty.")
    return entries
