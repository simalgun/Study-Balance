def count_by_subject(sessions):
    hours_per_subject = {}
    count_per_subject = {}
    for session in sessions:
        name = session["subject"]
        hours_per_subject[name] = hours_per_subject.get(name, 0) + session["hours"]
        count_per_subject[name] = count_per_subject.get(name, 0) + 1
    return hours_per_subject, count_per_subject

def find_most_and_least(hours_per_subject):
    most = ""
    least = ""
    for name in hours_per_subject:
        if most == "" or hours_per_subject[name] > hours_per_subject[most]:
            most = name
        if least == "" or hours_per_subject[name] < hours_per_subject[least]:
            least = name
    return most, least

def make_report(sessions, goal):
    lines = ["===== WEEKLY STUDY REPORT ====="]
    hours_per_subject, count_per_subject = count_by_subject(sessions)
    
    if len(sessions) == 0:
        lines.append("No study sessions this week yet.")
    else:
        for name in hours_per_subject:
            count = count_per_subject[name]
            if count == 1:
                word = "session"
            else:
                word = "sessions"
            lines.append(f"{name.capitalize()}: {hours_per_subject[name]:.2f} hours ({count} {word})")
        
        most, least = find_most_and_least(hours_per_subject)
        lines.append("")
        if hours_per_subject[most] == hours_per_subject[least]:
            lines.append("Most/least studied: all subjects have the same hours, nothing to compare.")
        else:
            lines.append(f"Most studied subject: {most.capitalize()}")
            lines.append(f"Least studied subject: {least.capitalize()}")
            
    total = 0
    for session in sessions:
        total += session["hours"]
    lines.append("")
    lines.append(f"Total this week: {total:.2f} hours")
    
    remaining = goal - total
    if goal == 0:
        lines.append("No weekly goal set yet. Example: python cli.py goal --hours 15")
    elif remaining <= 0.001:
        lines.append(f"Weekly goal ({goal:.2f} hours): reached!")
    else:
        lines.append(f"Weekly goal ({goal:.2f} hours): {remaining:.2f} hours to go")
    return "\n".join(lines)
