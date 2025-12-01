from db import db
from datetime import datetime

attendance_col = db['attendance']

def mark_attendance(email, subject, rfid_uid):
    today = datetime.now().strftime('%Y-%m-%d')
    existing = attendance_col.find_one({"email": email, "subject": subject, "date": today})
    if existing:
        return {"status": "info", "message": "Already marked"}
    attendance_col.insert_one({
        "email": email,
        "subject": subject,
        "rfid_uid": rfid_uid,
        "date": today,
        "status": "present"
    })
    return {"status": "success", "message": "Attendance marked"}
