"""Saving and loading the data files (plain text, inside the data folder)."""

import os

from checks import MAX_HOURS_PER_SESSION, MAX_WEEKLY_GOAL, check_hours

DATA_FOLDER = "data"


def sessions_path():
    return os.path.join(DATA_FOLDER, "sessions.txt")


def goal_path():
    return os.path.join(DATA_FOLDER, "goal.txt")


def load_sessions():
    """Return a list of dictionaries such as {"subject": "python", "hours": 2.0}."""
    path = sessions_path()
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    sessions = []
    line_number = 0
    for line in content.split("\n"):
        line_number += 1
        if line == "":
            continue
        broken = f"sessions.txt is broken at line {line_number}. Fix or delete the file."
        parts = line.split(",")
        if len(parts) != 2 or parts[0] == "":
            raise ValueError(broken)
        try:
            hours = check_hours(parts[1], MAX_HOURS_PER_SESSION)
        except ValueError:
            raise ValueError(broken)
        sessions.append({"subject": parts[0], "hours": hours})
    return sessions


def save_sessions(sessions):
    """Write every session as one line: subject,hours"""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    lines = []
    for session in sessions:
        lines.append(f"{session['subject']},{session['hours']}")
    with open(sessions_path(), "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def load_goal():
    """Return the weekly goal in hours (0.0 if no goal was set yet)."""
    path = goal_path()
    if not os.path.exists(path):
        return 0.0
    with open(path, "r", encoding="utf-8") as file:
        content = file.read().strip()
    try:
        return check_hours(content, MAX_WEEKLY_GOAL)
    except ValueError:
        raise ValueError("goal.txt is broken. Fix or delete the file.")


def save_goal(hours):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    with open(goal_path(), "w", encoding="utf-8") as file:
        file.write(str(hours))
