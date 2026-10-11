"""Score calculation and classification (TRD sections 12-13)."""

from typing import NamedTuple

from src import config


class ScoreResult(NamedTuple):
    """raw = points minus penalties before clamping; applied_caps lists caps that lowered the score."""

    raw: int
    score: int
    applied_caps: tuple[str, ...]


def length_points(length: int) -> int:
    """Points for length: POINTS_PER_CHARACTER per character, up to LENGTH_SCORING_CAP characters."""
    return config.POINTS_PER_CHARACTER * min(length, config.LENGTH_SCORING_CAP)


def class_points(class_count: int) -> int:
    """Points for the number of character classes present."""
    return config.POINTS_PER_CLASS * class_count


def repeat_penalty(runs: int) -> int:
    """Penalty for repeated-character runs, limited to MAX_PENALTY_REPEAT."""
    return min(config.PENALTY_PER_RUN * runs, config.MAX_PENALTY_REPEAT)


def sequence_penalty(runs: int) -> int:
    """Penalty for sequence runs, limited to MAX_PENALTY_SEQUENCE."""
    return min(config.PENALTY_PER_RUN * runs, config.MAX_PENALTY_SEQUENCE)


def common_penalty(common_match: str) -> int:
    """Only a base-word match is penalized; an exact match is handled by a cap."""
    return config.PENALTY_COMMON_BASE if common_match == "base" else 0


def compute_score(
    length: int, class_count: int, repeat_runs: int, sequence_runs: int, common_match: str
) -> ScoreResult:
    """Penalties first, then clamp to 0-100, then the lowest applicable cap."""
    raw = (
        length_points(length)
        + class_points(class_count)
        - repeat_penalty(repeat_runs)
        - sequence_penalty(sequence_runs)
        - common_penalty(common_match)
    )
    clamped = max(config.MIN_SCORE, min(config.MAX_SCORE, raw))

    caps = []
    if length < config.WEAK_LENGTH_THRESHOLD:
        caps.append(("CAP_SHORT", config.CAP_SHORT))
    if class_count == 1:
        caps.append(("CAP_SINGLE_CLASS", config.CAP_SINGLE_CLASS))
    if common_match == "exact":
        caps.append(("CAP_COMMON_EXACT", config.CAP_COMMON_EXACT))

    score = min([clamped] + [limit for _, limit in caps])
    applied = tuple(cap_id for cap_id, limit in caps if clamped > limit)
    return ScoreResult(raw, score, applied)


def classify(score: int) -> str:
    """Map a 0-100 score to its category."""
    if not config.MIN_SCORE <= score <= config.MAX_SCORE:
        raise ValueError("Score out of range.")
    for lower_bound, name in config.CATEGORY_BANDS:
        if score >= lower_bound:
            return name
    raise ValueError("Score out of range.")
