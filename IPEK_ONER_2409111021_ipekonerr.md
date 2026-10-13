# My Contribution — Study Balance

I was responsible for developing the command-line interface in `cli.py`.

My contributions include:

- Using Python's `argparse` module to read commands and options from the Terminal.
- Adding the `add`, `goal`, `report`, and `new-week` commands.
- Connecting these commands to `checks.py`, `storage.py`, and `report.py`.
- Checking required inputs and showing clear error messages for invalid input.
- Asking for confirmation before deleting the current week's study sessions.
- Testing the CLI commands and running the project checks.

## Test result

I ran `python3 test_all.py`. All 51 checks passed.
