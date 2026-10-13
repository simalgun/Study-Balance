"""Study Balance - track your weekly study time.

Examples:
    python cli.py add --subject Python --hours 2
    python cli.py goal --hours 15
    python cli.py report
    python cli.py new-week
"""

import argparse

import checks
import report
import storage


def ask_yes_no(question):
    """Ask until the user answers yes or no."""
    while True:
        try:
            reply = input(question + " (yes/no): ").strip().lower()
        except EOFError:
            return False
        if reply in ("yes", "y"):
            return True
        if reply in ("no", "n"):
            return False
        print("Please enter yes or no.")


def do_add(args):
    if args.subject == "" or args.hours == "":
        raise ValueError("The add command needs --subject and --hours.")
    subject = checks.clean_subject(args.subject)
    hours = checks.check_hours(args.hours, checks.MAX_HOURS_PER_SESSION)
    sessions = storage.load_sessions()
    sessions.append({"subject": subject, "hours": hours})
    storage.save_sessions(sessions)
    return f"Saved: {subject.capitalize()} - {hours:.2f} hours"


def do_goal(args):
    if args.hours == "":
        raise ValueError("The goal command needs --hours.")
    hours = checks.check_hours(args.hours, checks.MAX_WEEKLY_GOAL)
    storage.save_goal(hours)
    return f"Weekly goal set: {hours:.2f} hours"


def do_report(args):
    sessions = storage.load_sessions()
    goal = storage.load_goal()
    return report.make_report(sessions, goal)


def do_new_week(args):
    if not args.yes:
        if not ask_yes_no("Delete all sessions of this week and start a new week?"):
            return "Cancelled. Nothing was deleted."
    storage.save_sessions([])
    return "New week started. Your weekly goal was kept."


def build_parser():
    p = argparse.ArgumentParser(description="Track your weekly study time.")
    p.add_argument("command", choices=["add", "goal", "report", "new-week"],
                   help="what to do")
    p.add_argument("--subject", default="", help="subject name (for add)")
    p.add_argument("--hours", default="", help="hours, for example 1.5 (for add and goal)")
    p.add_argument("--yes", action="store_true", help="do not ask a question (for new-week)")
    return p


def run(arguments=None):
    """Run one command and return the text to show. Raises ValueError for bad input."""
    args = build_parser().parse_args(arguments)
    if args.command == "add":
        return do_add(args)
    if args.command == "goal":
        return do_goal(args)
    if args.command == "report":
        return do_report(args)
    return do_new_week(args)


def main():
    try:
        print(run())
    except ValueError as error:
        print(f"Error: {error}")
    except OSError as error:
        print(f"File problem: {error}")


if __name__ == "__main__":
    main()
