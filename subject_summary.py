from db import db
attendance_col = db['attendance']

def get_subject_summary(email):
    all_subjects = ["Professional Ethics", "Computer Networks", "Cyber Security", "Web Development", "Algorithms", "Design Engineering"]
    summary = []
    for subject in all_subjects:
        total_lectures = attendance_col.count_documents({"subject": subject})
        attended_lectures = attendance_col.count_documents({"email": email, "subject": subject})
        summary.append({
            "subject": subject,
            "total_lectures": total_lectures,
            "attended_lectures": attended_lectures
        })
    return summary
