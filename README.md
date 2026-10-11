# Password Strength Analyzer

A small, local Streamlit app (Tier-1 cybersecurity internship project). Enter a password and get a rule-based score (0-100), a category, a rule-by-rule explanation and recommendations.

**Privacy:** the password is processed in memory only. Application code does not store, log, cache or send it anywhere, and Streamlit usage statistics are disabled.

**Limitations:** the score is an educational estimate, not a guarantee that a password cannot be cracked. It uses a small local common-password list, does not check breach databases, and does not detect keyboard patterns (e.g. `qwerty`), repeated blocks (e.g. `abab`) or leetspeak. Do not test passwords you use for real accounts on a shared or untrusted computer.

## Requirements
Python 3.10 or newer.

## Install and run
```
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://127.0.0.1:8501 and listens on the loopback address only (`.streamlit/config.toml`).


## Scoring in brief
3 points per character (first 20 characters) + 10 per character type (lowercase, uppercase, digit, special), minus penalties for repeated characters, simple sequences and common words. Caps apply to short passwords (<8), single-character-type passwords and exact common passwords. Categories: Very Weak 0-19, Weak 20-39, Moderate 40-59, Strong 60-79, Very Strong 80-100. Full definition: `docs/03_TRD.md`.

## Project layout
`app.py` (UI) ·
`src/` (analysis, scoring, feedback) ·
`data/common_passwords.txt`  ·
`screenshots/`
