"""Streamlit UI for the Password Strength Analyzer. Contains layout only, no analysis logic."""

from pathlib import Path

import streamlit as st

from src.analyzer import analyze_password
from src.common_passwords import CommonListError, load_common_passwords
from src.config import COMMON_PASSWORDS_FILE, MAX_PASSWORD_LENGTH, MAX_SCORE
from src.feedback import CAP_MESSAGES
from src.models import AnalysisResult
from src.validation import validate_password

COMMON_LIST_PATH = Path(__file__).parent / COMMON_PASSWORDS_FILE
STATUS_SYMBOLS = {"pass": "✓", "warn": "⚠", "fail": "✗"}
LIMITATION_NOTICE = (
    "This score is an educational, rule-based estimate. It does not guarantee a password "
    "cannot be cracked and does not check breach databases."
)


def format_points(points: int) -> str:
    """Format signed points for display; zero is shown as 0."""
    return f"{points:+d}" if points else "0"


def render_result(result: AnalysisResult) -> None:
    """Show score, category, indicator, analysis rows and recommendations."""
    st.subheader(f"Strength: {result.category}")
    st.markdown(f"Score: {result.score}/{MAX_SCORE}")
    st.progress(result.score / MAX_SCORE)

    st.subheader("Analysis")
    for finding in result.findings:
        st.markdown(
            f"{STATUS_SYMBOLS[finding.status]} {finding.message} ({format_points(finding.points)})"
        )
    for cap_id in result.applied_caps:
        st.markdown(f"ℹ {CAP_MESSAGES[cap_id]}")

    st.subheader("Recommendations")
    for recommendation in result.recommendations:
        st.markdown(f"- {recommendation}")


def main() -> None:
    """Build the page: form, validation, analysis and result display."""
    st.set_page_config(page_title="Password Strength Analyzer", layout="centered")
    st.title("Password Strength Analyzer")
    st.markdown("Check a password locally. Nothing is saved or sent anywhere.")

    with st.form("analyze_form", clear_on_submit=False):
        password = st.text_input("Password", type="password", max_chars=MAX_PASSWORD_LENGTH)
        submitted = st.form_submit_button("Analyze")

    if not submitted:
        st.info("Enter a password and press Analyze.")
    else:
        validation = validate_password(password)
        if not validation.is_valid:
            if password == "":
                st.warning(validation.error_message)
            else:
                st.error(validation.error_message)
        else:
            for notice in validation.notices:
                st.info(notice)
            try:
                common_set = load_common_passwords(COMMON_LIST_PATH)
                render_result(analyze_password(password, common_set))
            except CommonListError:
                st.error("The common-password list could not be loaded.")
            except Exception:
                st.error("Something went wrong while analyzing. Nothing was saved.")

    st.caption(LIMITATION_NOTICE)


main()
