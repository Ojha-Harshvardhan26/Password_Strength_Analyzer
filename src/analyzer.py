"""Orchestrates checks, scoring and feedback for one password."""

from src import config, scoring
from src.checks import (
    check_common,
    count_character_classes,
    count_repeat_runs,
    count_sequence_runs,
)
from src.feedback import build_findings, build_recommendations
from src.models import AnalysisResult
from src.validation import validate_password


def analyze_password(password: str, common_set: frozenset[str]) -> AnalysisResult:
    """Analyze a valid password. Raises ValueError (without input details) if invalid."""
    if not validate_password(password).is_valid:
        raise ValueError("Invalid password input.")

    length = len(password)
    classes = count_character_classes(password)
    class_count = sum(classes.values())
    repeat_runs = count_repeat_runs(password)
    sequence_runs = count_sequence_runs(password)
    common_match = check_common(password, common_set)

    points = {
        "LEN": scoring.length_points(length),
        "LOWER": config.POINTS_PER_CLASS if classes["lowercase"] else 0,
        "UPPER": config.POINTS_PER_CLASS if classes["uppercase"] else 0,
        "DIGIT": config.POINTS_PER_CLASS if classes["digit"] else 0,
        "SPECIAL": config.POINTS_PER_CLASS if classes["special"] else 0,
        "REPEAT": -scoring.repeat_penalty(repeat_runs),
        "SEQUENCE": -scoring.sequence_penalty(sequence_runs),
        "COMMON": -scoring.common_penalty(common_match),
    }
    result = scoring.compute_score(length, class_count, repeat_runs, sequence_runs, common_match)
    return AnalysisResult(
        score=result.score,
        category=scoring.classify(result.score),
        findings=build_findings(length, classes, repeat_runs, sequence_runs, common_match, points),
        recommendations=build_recommendations(length, classes, repeat_runs, sequence_runs, common_match),
        applied_caps=result.applied_caps,
    )
