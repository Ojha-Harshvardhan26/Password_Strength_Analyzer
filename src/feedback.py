"""Static explanation and recommendation text. Nothing here uses password content."""

from src import config
from src.models import Finding

_CLASS_ORDER = (
    ("LOWER", "lowercase", "Contains lowercase letters.", "No lowercase letters."),
    ("UPPER", "uppercase", "Contains uppercase letters.", "No uppercase letters."),
    ("DIGIT", "digit", "Contains numbers.", "No numbers."),
    ("SPECIAL", "special", "Contains special characters or spaces.", "No special characters or spaces."),
)

CAP_MESSAGES = {
    "CAP_SHORT": "Score limited because the password is shorter than 8 characters.",
    "CAP_SINGLE_CLASS": "Score limited because only one type of character is used.",
    "CAP_COMMON_EXACT": "Score limited because this is a common password.",
}

GENERIC_RECOMMENDATION = "No specific recommendations. Use a different password for every account."


def _length_finding(length: int, points: int) -> Finding:
    if length < config.WEAK_LENGTH_THRESHOLD:
        return Finding("LEN", "fail", points, "Length is under 8 characters.")
    if length < config.MIN_RECOMMENDED_LENGTH:
        return Finding("LEN", "warn", points, "Length is 8-11 characters; 12 or more is better.")
    return Finding("LEN", "pass", points, "Length is 12 characters or more.")


def build_findings(
    length: int,
    classes: dict[str, bool],
    repeat_runs: int,
    sequence_runs: int,
    common_match: str,
    points: dict[str, int],
) -> tuple[Finding, ...]:
    """Build one finding per rule, in fixed order. points maps rule id to signed points."""
    findings = [_length_finding(length, points["LEN"])]
    for rule_id, class_name, present_text, absent_text in _CLASS_ORDER:
        present = classes[class_name]
        findings.append(
            Finding(rule_id, "pass" if present else "warn", points[rule_id],
                    present_text if present else absent_text)
        )
    findings.append(
        Finding("REPEAT", "warn", points["REPEAT"], "Repeated characters found (3 or more in a row).")
        if repeat_runs else
        Finding("REPEAT", "pass", points["REPEAT"], "No repeated characters in a row.")
    )
    findings.append(
        Finding("SEQUENCE", "warn", points["SEQUENCE"], "Simple sequence found (such as 1234 or abcd).")
        if sequence_runs else
        Finding("SEQUENCE", "pass", points["SEQUENCE"], "No simple sequences found.")
    )
    if common_match == "exact":
        findings.append(Finding("COMMON", "fail", points["COMMON"], "Matches a common password."))
    elif common_match == "base":
        findings.append(Finding("COMMON", "fail", points["COMMON"],
                                "Matches a common password with numbers or symbols added."))
    else:
        findings.append(Finding("COMMON", "pass", points["COMMON"], "Not found in the common-password list."))
    return tuple(findings)


def build_recommendations(
    length: int,
    classes: dict[str, bool],
    repeat_runs: int,
    sequence_runs: int,
    common_match: str,
) -> tuple[str, ...]:
    """Recommendations in the fixed order of TRD section 14."""
    recommendations = []
    if length < config.MIN_RECOMMENDED_LENGTH:
        recommendations.append("Use at least 12 characters.")
    if not classes["lowercase"]:
        recommendations.append("Add lowercase letters.")
    if not classes["uppercase"]:
        recommendations.append("Add uppercase letters.")
    if not classes["digit"]:
        recommendations.append("Add numbers.")
    if not classes["special"]:
        recommendations.append("Add special characters or spaces.")
    if repeat_runs:
        recommendations.append("Avoid repeating the same character three or more times in a row.")
    if sequence_runs:
        recommendations.append("Avoid simple sequences such as 1234 or abcd.")
    if common_match != "none":
        recommendations.append(
            "Avoid common passwords, including common words with numbers or symbols added."
        )
    return tuple(recommendations) or (GENERIC_RECOMMENDATION,)
