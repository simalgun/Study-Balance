"""Simple self-checks for the whole project.

Run:  python test_all.py
Each block belongs to one team member (see the comments).
"""

import os
import shutil

import checks
import cli
import report
import storage

TEST_FOLDER = "test_data"
results = []


def check(name, actual, expected):
    if actual == expected:
        results.append(True)
        print(f"PASS  {name}")
    else:
        results.append(False)
        print(f"FAIL  {name}: expected {expected}, got {actual}")


def gives_error(function, text):
    """True if function(text) raises ValueError."""
    try:
        function(text)
    except ValueError:
        return True
    return False


def hours_24(text):
    return checks.check_hours(text, 24)


def sessions_file_is_rejected():
    try:
        storage.load_sessions()
    except ValueError:
        return True
    return False


def goal_file_is_rejected():
    try:
        storage.load_goal()
    except ValueError:
        return True
    return False


def write_file(path, text):
    os.makedirs(storage.DATA_FOLDER, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


# ---------- Member 2: checks.py ----------
def test_checks():
    check("subject is cleaned", checks.clean_subject("  Data   Structures "), "data structures")
    for bad in ["", "   ", "a" * 41, "a,b"]:
        check(f"bad subject rejected: '{bad}'", gives_error(checks.clean_subject, bad), True)
    check("hours 1,5 works", checks.check_hours("1,5", 24), 1.5)
    check("hours 24 works", checks.check_hours("24", 24), 24.0)
    for bad in ["abc", "nan", "inf", "-1", "0", "25", "", "0.05", "1e999"]:
        check(f"bad hours rejected: '{bad}'", gives_error(hours_24, bad), True)


# ---------- Member 1: storage.py ----------
def test_storage():
    check("no file means empty list", storage.load_sessions(), [])
    check("no goal file means 0", storage.load_goal(), 0.0)

    sessions = [{"subject": "python", "hours": 2.0}, {"subject": "veri yapıları", "hours": 1.5}]
    storage.save_sessions(sessions)
    check("save then load", storage.load_sessions(), sessions)

    storage.save_goal(15.0)
    check("goal save then load", storage.load_goal(), 15.0)

    for bad in ["python,abc", "python", "python,1,2", ",2.0", "python,-3", "python,nan"]:
        write_file(storage.sessions_path(), bad)
        check(f"broken sessions line rejected: '{bad}'", sessions_file_is_rejected(), True)
    write_file(storage.goal_path(), "hello")
    check("broken goal file rejected", goal_file_is_rejected(), True)


# ---------- Member 3: report.py ----------
def test_report():
    sessions = [
        {"subject": "python", "hours": 2.0},
        {"subject": "math", "hours": 1.0},
        {"subject": "python", "hours": 3.0},
    ]
    hours, counts = report.count_by_subject(sessions)
    check("hours per subject", hours, {"python": 5.0, "math": 1.0})
    check("sessions per subject", counts, {"python": 2, "math": 1})
    check("most and least", report.find_most_and_least(hours), ("python", "math"))
    check("most and least of nothing", report.find_most_and_least({}), ("", ""))

    text = report.make_report(sessions, 10.0)
    check("report shows python line", "Python: 5.00 hours (2 sessions)" in text, True)
    check("report shows most", "Most studied subject: Python" in text, True)
    check("report shows least", "Least studied subject: Math" in text, True)
    check("report shows goal progress", "4.00 hours to go" in text, True)
    check("goal reached", "reached" in report.make_report(sessions, 6.0), True)
    check("no goal message", "No weekly goal" in report.make_report(sessions, 0), True)
    check("empty report", "No study sessions" in report.make_report([], 0), True)
    equal = [{"subject": "a", "hours": 1.0}, {"subject": "b", "hours": 1.0}]
    check("equal subjects", "nothing to compare" in report.make_report(equal, 0), True)


# ---------- Member 4: cli.py ----------
def cli_gives_error(arguments):
    try:
        cli.run(arguments)
    except ValueError:
        return True
    return False


def test_cli():
    check("add", cli.run(["add", "--subject", "Python", "--hours", "2"]), "Saved: Python - 2.00 hours")
    check("add again (same subject, other case)", cli.run(["add", "--subject", "PYTHON", "--hours", "1,5"]), "Saved: Python - 1.50 hours")
    check("goal", cli.run(["goal", "--hours", "10"]), "Weekly goal set: 10.00 hours")
    text = cli.run(["report"])
    check("report has total", "Total this week: 3.50 hours" in text, True)
    check("add without hours", cli_gives_error(["add", "--subject", "x"]), True)
    check("add without subject", cli_gives_error(["add", "--hours", "1"]), True)
    check("add negative hours", cli_gives_error(["add", "--subject", "x", "--hours", "-3"]), True)
    check("add nan hours", cli_gives_error(["add", "--subject", "x", "--hours", "nan"]), True)
    check("goal without hours", cli_gives_error(["goal"]), True)
    check("new week", cli.run(["new-week", "--yes"]), "New week started. Your weekly goal was kept.")
    check("report after new week", "No study sessions" in cli.run(["report"]), True)
    check("goal kept after new week", "10.00 hours" in cli.run(["report"]), True)


def start_clean():
    """Delete the temporary test folder so every block starts from nothing."""
    if os.path.exists(TEST_FOLDER):
        shutil.rmtree(TEST_FOLDER)


def main():
    storage.DATA_FOLDER = TEST_FOLDER  # tests never touch your real data
    start_clean()
    test_checks()
    start_clean()
    test_storage()
    start_clean()
    test_report()
    start_clean()
    test_cli()
    start_clean()

    passed = results.count(True)
    print(f"\n{passed} of {len(results)} checks passed.")


if __name__ == "__main__":
    main()
