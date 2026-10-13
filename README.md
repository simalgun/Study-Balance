# Study Balance

A small command-line tool for university students. It saves how many hours you study each subject, lets you set a weekly goal, and shows which subject you studied the most and the least this week.

Only plain Python is used (no extra installation). Tested with Python 3.8+.

## Usage

```
python cli.py add --subject Python --hours 2
python cli.py add --subject Mathematics --hours 1.5
python cli.py goal --hours 15
python cli.py report
python cli.py new-week
```

| Command | What it does |
|---|---|
| `add --subject S --hours H` | Saves one study session (H between 0.1 and 24) |
| `goal --hours H` | Sets the weekly goal in total study hours (H up to 100) |
| `report` | Shows hours and number of sessions per subject, the most and least studied subject, the total and the goal progress |
| `new-week [--yes]` | Starts a new week: deletes all saved sessions after asking yes/no (`--yes` skips the question). The goal is kept |
| `--help` | Shows all options |

"This week" means all sessions saved since the last `new-week` command.

Example report:

```
===== WEEKLY STUDY REPORT =====
Python: 5.00 hours (2 sessions)
Mathematics: 1.50 hours (1 session)
Data structures: 0.50 hours (1 session)

Most studied subject: Python
Least studied subject: Data structures

Total this week: 7.00 hours
Weekly goal (15.00 hours): 8.00 hours to go
```

## Files

| File | Purpose |
|---|---|
| `cli.py` | Entry point. Reads the command line (`argparse`), runs the command, prints the result or a clear error |
| `checks.py` | Checks and cleans everything the user types (subject name, hours) |
| `storage.py` | Saves and loads the data files `data/sessions.txt` and `data/goal.txt` |
| `report.py` | Calculates the totals and builds the report text |
| `test_all.py` | Self-checks for every file (`python test_all.py`) |
| `contributions/` | One file per team member |

Data format: `data/sessions.txt` has one line per session, `subject,hours` (for example `python,2.0`). `data/goal.txt` holds one number. The `data` folder is created automatically and is not part of the repository.

## Safety checks (what happens with bad input)

- Hours must be a number from 0.1 up to 24 (goal: up to 100). `abc`, `nan`, `inf`, negative numbers, zero and huge numbers are rejected. `1,5` is accepted as 1.5.
- Subjects are cleaned (extra spaces removed, lowercase, so `Python` and `python` are the same subject). Empty names, names longer than 40 characters and names containing a comma (our file separator) are rejected.
- `add` and `goal` without their required options give a clear message.
- If a data file was edited by hand and is broken, the program says which file and line is wrong instead of crashing.
- `new-week` asks before deleting anything.
- All errors are printed as one short line, never as a long traceback.

## Tests

```
python test_all.py
```

The tests use a temporary folder (`test_data`) and never touch your real data.
