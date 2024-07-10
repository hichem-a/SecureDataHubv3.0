import json
import os
from functions.file_management import ensure_files_json_exists

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "json")

def ensure_json_dir_exists():
    """Stellt sicher, dass der JSON-Ordner existiert"""
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

def log_file_action(user, file_path, action):
    """Protokolliert die Dateiaktionen eines Benutzers"""
    ensure_files_json_exists()  # Sicherstellen, dass files.json existiert
    with open(os.path.join(JSON_DIR, "files.json"), "r") as file:
        try:
            logs = json.load(file)
        except json.JSONDecodeError:
            logs = {}

    if user not in logs:
        logs[user] = []

    logs[user].append({
        "file": file_path,
        "action": action
    })

    with open(os.path.join(JSON_DIR, "files.json"), "w") as file:
        json.dump(logs, file, indent=4)

def get_user_activity_log(user):
    """Ruft das Benutzeraktivitätsprotokoll ab"""
    ensure_files_json_exists()  # Sicherstellen, dass files.json existiert
    with open(os.path.join(JSON_DIR, "files.json"), "r") as file:
        try:
            logs = json.load(file)
            return [f"File: {log['file']}, Action: {log['action']}" for log in logs.get(user, [])]
        except json.JSONDecodeError:
            return []
