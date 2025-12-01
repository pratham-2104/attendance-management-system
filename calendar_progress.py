from db import db
attendance_col = db['attendance']

def get_attendance_dates(email, month=None, year=None):
    query = {"email": email}
    if month and year:
        query["date"] = {"$regex": f"^{year}-{month:02d}"}
    dates = attendance_col.distinct("date", query)
    return dates

def get_attendance_on_date(email, date):
    records = list(attendance_col.find({"email": email, "date": date}))
    subjects_attended = [r["subject"] for r in records]
    all_subjects = ["Professional Ethics", "Computer Networks", "Cyber Security", "Web Development", "Algorithms", "Design Engineering"]
    summary = []
    for subject in all_subjects:
        summary.append({
            "subject": subject,
            "status": "present" if subject in subjects_attended else "absent"
        })
    return summary
