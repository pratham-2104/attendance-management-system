from flask import Flask, request, jsonify
from flask_cors import CORS
from db import users_col, db
from otp_handler import generate_and_send_otp, verify_user_otp
from profile_handler import fetch_user_profile, update_user_profile
from notification_handler import save_notification_preference
from rfid_attendance import mark_attendance
from attendance_summary import get_attendance_summary
from subject_summary import get_subject_summary
from calendar_progress import get_attendance_dates, get_attendance_on_date

app = Flask(__name__)
CORS(app)

@app.route('/request_otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'status': 'fail', 'message': 'Email is required'}), 400
    return jsonify(generate_and_send_otp(email))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    if not email or not otp:
        return jsonify({'status': 'fail', 'message': 'Email and OTP are required'}), 400
    return jsonify(verify_user_otp(email, otp))

@app.route('/get_profile', methods=['POST'])
def get_profile():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"status": "fail", "message": "Email is required"}), 400
    profile = fetch_user_profile(email)
    return jsonify({"status": "success", "data": profile}) if profile else jsonify({"status": "fail", "message": "User not found"}), 404

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"status": "fail", "message": "Email is required"}), 400
    profile_data = {
        "student_name": data.get("student_name"),
        "enrollment_no": data.get("enrollment_no"),
        "phone_no": data.get("phone_no"),
        "branch": data.get("branch"),
        "semester": data.get("semester"),
        "class": data.get("class")
    }
    return jsonify(update_user_profile(email, profile_data))

@app.route('/set_notifications', methods=['POST'])
def set_notifications():
    data = request.get_json()
    email = data.get("email")
    allowed = data.get("allowed")
    if email is None or allowed is None:
        return jsonify({"status": "fail", "message": "Missing email or selection"}), 400
    return jsonify(save_notification_preference(email, allowed))

@app.route('/mark_attendance', methods=['POST'])
def rfid_attendance():
    data = request.get_json()
    email = data.get('email')
    subject = data.get('subject')
    rfid_uid = data.get('rfid')
    if not email or not subject or not rfid_uid:
        return jsonify({"status": "fail", "message": "Missing data"}), 400
    return jsonify(mark_attendance(email, subject, rfid_uid))

@app.route('/attendance_summary', methods=['POST'])
def attendance_summary():
    data = request.get_json()
    email = data.get("email")
    date = data.get("date")
    if not email or not date:
        return jsonify({"status": "fail", "message": "Missing email or date"}), 400
    return jsonify({"status": "success", "data": get_attendance_summary(email, date)})

@app.route('/subject_summary', methods=['POST'])
def subject_summary():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"status": "fail", "message": "Email is required"}), 400
    return jsonify({"status": "success", "data": get_subject_summary(email)})

@app.route('/attendance_dates', methods=['POST'])
def attendance_dates():
    data = request.get_json()
    email = data.get("email")
    month = data.get("month")
    year = data.get("year")
    if not email:
        return jsonify({"status": "fail", "message": "Email is required"}), 400
    return jsonify({"status": "success", "dates": get_attendance_dates(email, month, year)})

@app.route('/attendance_on_date', methods=['POST'])
def attendance_on_date():
    data = request.get_json()
    email = data.get("email")
    date = data.get("date")
    if not email or not date:
        return jsonify({"status": "fail", "message": "Email and date are required"}), 400
    return jsonify({"status": "success", "data": get_attendance_on_date(email, date)})

if __name__ == '__main__':
    app.run(debug=True)
