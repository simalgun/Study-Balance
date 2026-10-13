"""Checking and cleaning everything the user types."""

MIN_HOURS = 0.1
MAX_HOURS_PER_SESSION = 24
MAX_WEEKLY_GOAL = 100
MAX_SUBJECT_LENGTH = 40


def clean_subject(raw):
    """Return the subject in a clean, lowercase form, or raise ValueError."""
    subject = " ".join(raw.split()).lower()
    if subject == "":
        raise ValueError("Subject cannot be empty.")
    if len(subject) > MAX_SUBJECT_LENGTH:
        raise ValueError(f"Subject is too long (max {MAX_SUBJECT_LENGTH} characters).")
    if "," in subject:
        raise ValueError("Subject cannot contain a comma.")
    return subject


def check_hours(raw, maximum):
    """Turn text like '1.5' or '1,5' into a number of hours, or raise ValueError."""
    try:
        hours = float(raw.replace(",", "."))
    except ValueError:
        raise ValueError(f"Hours must be a number, got '{raw}'.")
    # Written as "not (good range)" on purpose: the text 'nan' is a valid float,
    # and every comparison with nan is False, so only this form rejects it.
    if not (hours >= MIN_HOURS and hours <= maximum):
        raise ValueError(f"Hours must be between {MIN_HOURS} and {maximum}.")
    return hours
