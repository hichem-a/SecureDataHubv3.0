import json
import shutil
import os
from tkinter import messagebox

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "json")

def ensure_json_dir_exists():
    """Stellt sicher, dass der JSON-Ordner existiert"""
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

def ensure_files_json_exists():
    """Stellt sicher, dass die Datei files.json existiert"""
    ensure_json_dir_exists()
    if not os.path.exists(os.path.join(JSON_DIR, "files.json")):
        with open(os.path.join(JSON_DIR, "files.json"), "w") as file:
            json.dump({}, file)

def backup_data():
    """Erstellt eine Sicherung der Daten"""
    src = os.path.join(JSON_DIR, "files.json")
    dst = os.path.join(JSON_DIR, "backup_files.json")
    shutil.copy(src, dst)
    messagebox.showinfo("Success", "Data backup created successfully.")

def restore_data():
    """Stellt die gesicherten Daten wieder her"""
    src = os.path.join(JSON_DIR, "backup_files.json")
    dst = os.path.join(JSON_DIR, "files.json")
    shutil.copy(src, dst)
    messagebox.showinfo("Success", "Data restored successfully.")
