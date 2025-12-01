from db import users_col

def fetch_user_profile(email):
    return users_col.find_one({"email": email}, {"_id": 0})

def update_user_profile(email, profile_data):
    result = users_col.update_one({"email": email}, {"$set": profile_data})
    return {
        "status": "success" if result.modified_count > 0 else "info",
        "message": "Profile updated" if result.modified_count > 0 else "No changes made"
    }
