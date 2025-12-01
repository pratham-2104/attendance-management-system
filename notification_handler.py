from db import users_col

def save_notification_preference(email, allowed):
    result = users_col.update_one({"email": email}, {"$set": {"notifications": allowed}})
    return {
        "status": "success" if result.modified_count > 0 else "info",
        "message": "Notification preference updated"
    }
