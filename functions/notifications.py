import json
import os

def send_notification(recipient, sender, file_path, password):
    """Sendet eine Benachrichtigung an einen Benutzer"""
    notifications = load_notifications()
    if recipient not in notifications:
        notifications[recipient] = []

    notification = {
        "sender": sender,
        "file_path": file_path,
        "password": password
    }
    notifications[recipient].append(notification)
    save_notifications(notifications)

def get_received_files(username):
    """Gibt die empfangenen Dateien eines Benutzers zurück"""
    notifications = load_notifications()
    return notifications.get(username, [])

def get_all_notifications():
    """Gibt alle Benachrichtigungen zurück"""
    notifications = load_notifications()
    all_notifications = []
    for user, user_notifications in notifications.items():
        for notification in user_notifications:
            all_notifications.append(f"{user}: {notification['file_path']} by {notification['sender']}")
    return all_notifications

def send_admin_notification(message, users):
    """Sendet eine Benachrichtigung an alle Admins"""
    notifications = load_notifications()
    for user, details in users.items():
        if details['role'] == 'admin':
            if user not in notifications:
                notifications[user] = []
            notifications[user].append({"sender": "System", "file_path": message, "password": None})
    save_notifications(notifications)

def load_notifications():
    """Lädt die Benachrichtigungen aus der JSON-Datei"""
    try:
        with open(os.path.join("json", "notifications.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_notifications(notifications):
    """Speichert die Benachrichtigungen in der JSON-Datei"""
    with open(os.path.join("json", "notifications.json"), "w") as file:
        json.dump(notifications, file, indent=4)
