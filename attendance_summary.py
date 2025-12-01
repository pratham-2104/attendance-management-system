from db import db
attendance_col = db['attendance']

def get_attendance_summary(email, date):
    attended = list(attendance_col.find({"email": email, "date": date}))
    subjects_present = [entry["subject"] for entry in attended]
    all_subjects = ["Professional Ethics", "Computer Networks", "Cyber Security", "Web Development"]
    result = []
    for subject in all_subjects:
        result.append({
            "subject": subject,
            "status": "present" if subject in subjects_present else "absent"
        })
    return result
