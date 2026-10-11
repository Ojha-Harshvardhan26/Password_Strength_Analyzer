"""All limits, weights and thresholds for the analyzer (single source: TRD section 12)."""

MAX_PASSWORD_LENGTH = 128
MIN_RECOMMENDED_LENGTH = 12
WEAK_LENGTH_THRESHOLD = 8

POINTS_PER_CHARACTER = 3
LENGTH_SCORING_CAP = 20
POINTS_PER_CLASS = 10

REPEAT_RUN_MIN = 3
SEQUENCE_RUN_MIN = 4
PENALTY_PER_RUN = 10
MAX_PENALTY_REPEAT = 20
MAX_PENALTY_SEQUENCE = 20
PENALTY_COMMON_BASE = 30

CAP_SHORT = 39
CAP_SINGLE_CLASS = 59
CAP_COMMON_EXACT = 10

MIN_SCORE = 0
MAX_SCORE = 100

# (lowest score of the band, category name), highest band first.
CATEGORY_BANDS = (
    (80, "Very Strong"),
    (60, "Strong"),
    (40, "Moderate"),
    (20, "Weak"),
    (0, "Very Weak"),
)

COMMON_PASSWORDS_FILE = "data/common_passwords.txt"
