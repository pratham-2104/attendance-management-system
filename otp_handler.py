import random
from db import users_col

otp_storage = {}

def generate_and_send_otp(email):
    otp = str(random.randint(1000, 9999))
    otp_storage[email] = otp
    print(f"OTP for {email}: {otp}")
    return {"status": "success", "message": "OTP sent (simulated)"}

def verify_user_otp(email, otp):
    if otp_storage.get(email) == otp:
        if not users_col.find_one({"email": email}):
            users_col.insert_one({"email": email})
        return {"status": "success", "message": "OTP verified"}
    return {"status": "fail", "message": "Invalid OTP"}
