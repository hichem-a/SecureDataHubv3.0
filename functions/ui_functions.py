import json
import os
import random
import string
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog

import pyperclip

from functions.encryption import encrypt, decrypt
from functions.file_management import ensure_files_json_exists
from functions.logging import log_file_action, get_user_activity_log
from functions.notifications import send_notification, get_received_files, get_all_notifications, \
    send_admin_notification
from functions.policy_editor import PolicyEditor
from functions.user_management import add_user_to_system, delete_user, update_user_role


def view_user_data(app):
    """Zeigt die Dateiaktionen aller Benutzer an (nur Admin)"""
    ensure_files_json_exists()  # Sicherstellen, dass files.json existiert
    with open(os.path.join("json", "files.json"), "r") as file:
        try:
            logs = json.load(file)
        except json.JSONDecodeError:
            logs = {}

    user_data = ""
    for user, actions in logs.items():
        user_data += f"User: {user}\n"
        for action in actions:
            user_data += f"  - File: {action['file']}, Action: {action['action']}\n"

    messagebox.showinfo("User Data", user_data)

def add_user(app):
    """Öffnet einen Dialog zur Eingabe eines neuen Benutzers und fügt ihn hinzu"""
    username = simpledialog.askstring("New User", "Enter username:")
    password = simpledialog.askstring("New User", "Enter password:", show="*")

    if username and password:
        if username in app.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            add_user_to_system(username, password, app.users)
            send_admin_notification(f"User {username} added by admin {app.logged_in_user}.", app.users)
            messagebox.showinfo("Success", f"User {username} added successfully.")
    else:
        messagebox.showerror("Error", "Username and password cannot be empty.")

def set_document_expiry(app):
    """Öffnet einen Dialog zum Setzen eines Ablaufdatums für ein Dokument"""
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    if file_path:
        expiry_date = simpledialog.askstring("Set Expiry Date", "Enter expiry date (YYYY-MM-DD):")
        if expiry_date:
            try:
                with open(os.path.join("json", "expiry_dates.json"), "r") as file:
                    expiry_dates = json.load(file)
            except FileNotFoundError:
                expiry_dates = {}

            expiry_dates[file_path] = expiry_date

            with open(os.path.join("json", "expiry_dates.json"), "w") as file:
                json.dump(expiry_dates, file, indent=4)

            messagebox.showinfo("Success", "Expiry date set successfully.")
        else:
            messagebox.showerror("Error", "Expiry date cannot be empty.")

def edit_policies(app):
    """Öffnet das Fenster zur Bearbeitung der Compliance-Richtlinien"""
    editor = PolicyEditor(app.root, app.compliance)
    app.root.wait_window(editor.top)
    send_admin_notification(f"Compliance policies edited by admin {app.logged_in_user}.", app.users)

def manage_notifications(app):
    """Verwaltet die Benachrichtigungen (nur Admin)"""
    notifications = get_all_notifications()
    notifications_text = "\n".join(notifications)
    messagebox.showinfo("Manage Notifications", f"All notifications:\n{notifications_text}")

def manage_users(app):
    """Verwaltet Benutzerkonten (nur Admin)"""
    app.clear_screen()

    frame = ttk.Frame(app.root, padding=20)
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text="Manage Users", font=("Helvetica", 24, 'bold')).pack(pady=20)

    for username, details in app.users.items():
        user_frame = ttk.Frame(frame, padding=5)
        user_frame.pack(fill='x', pady=5)

        ttk.Label(user_frame, text=f"User: {username}").pack(side=tk.LEFT, padx=10)
        ttk.Label(user_frame, text=f"Role: {details['role']}").pack(side=tk.LEFT, padx=10)

        if details['role'] != 'admin':
            ttk.Button(user_frame, text="Delete User", command=lambda u=username: delete_user_func(app, u)).pack(side=tk.RIGHT, padx=5)

    ttk.Button(frame, text="Back", command=app.main_screen).pack(pady=10)

def delete_user_func(app, username):
    """Löscht einen Benutzer (nur Admin)"""
    if username in app.users:
        confirm = messagebox.askyesno("Delete User", f"Are you sure you want to delete user {username}?")
        if confirm:
            delete_user(username, app.users)
            send_admin_notification(f"User {username} deleted by admin {app.logged_in_user}.", app.users)
            messagebox.showinfo("Success", f"User {username} deleted successfully.")
            manage_users(app)
    else:
        messagebox.showerror("Error", "Username not found.")

def change_user_role(app):
    """Ändert die Rolle eines Benutzers (nur Admin)"""
    username = simpledialog.askstring("Change User Role", "Enter username of the user to change role:")
    if username in app.users:
        new_role = simpledialog.askstring("Change User Role", "Enter new role (admin/user):")
        if new_role in ["admin", "user"]:
            update_user_role(username, new_role, app.users)
            send_admin_notification(f"User role of {username} changed to {new_role} by admin {app.logged_in_user}.", app.users)
            messagebox.showinfo("Success", f"Role of {username} changed to {new_role} successfully.")
        else:
            messagebox.showerror("Error", "Invalid role. Please enter 'admin' or 'user'.")
    else:
        messagebox.showerror("Error", "Username not found.")

def delete_my_account(app):
    """Löscht das eigene Konto (Admin)"""
    confirm = messagebox.askyesno("Delete My Account", "Are you sure you want to delete your own account?")
    if confirm:
        delete_user(app.logged_in_user, app.users)
        messagebox.showinfo("Success", "Your account has been deleted.")
        app.login_screen()

def encrypt_files(app):
    """Verschlüsselt bis zu drei ausgewählte Dateien und speichert sie an einem ausgewählten Speicherort"""
    file_paths = filedialog.askopenfilenames(title="Select up to 3 files", filetypes=[("All files", "*.*")])
    if file_paths and len(file_paths) <= 3:
        password = app.password_entry.get()
        violations = app.compliance.check_compliance({"password": password})
        if violations:
            report = app.compliance.generate_report(violations)
            messagebox.showerror("Compliance Error", report)
            return

        for file_path in file_paths:
            try:
                with open(file_path, "rb") as file:
                    data = file.read()
                encrypted_data = encrypt(data, password)
                save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted files", "*.enc")])
                if save_path:
                    with open(save_path, "wb") as file:
                        file.write(encrypted_data)
                    log_file_action(app.logged_in_user, file_path, "encrypt")
                else:
                    messagebox.showerror("Error", "File save cancelled.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encrypt file {file_path}: {str(e)}")
        messagebox.showinfo("Success", "Files encrypted successfully!")
    else:
        messagebox.showerror("Error", "Please select up to 3 files.")

def decrypt_files(app):
    """Entschlüsselt bis zu drei ausgewählte Dateien und speichert sie an einem ausgewählten Speicherort"""
    file_paths = filedialog.askopenfilenames(title="Select up to 3 encrypted files", filetypes=[("Encrypted files", "*.enc")])
    if file_paths and len(file_paths) <= 3:
        password = app.password_entry.get()
        violations = app.compliance.check_compliance({"password": password})
        if violations:
            report = app.compliance.generate_report(violations)
            messagebox.showerror("Compliance Error", report)
            return

        for file_path in file_paths:
            try:
                with open(file_path, "rb") as file:
                    encrypted_data = file.read()
                decrypted_data = decrypt(encrypted_data, password)
                save_path = filedialog.asksaveasfilename(defaultextension="", filetypes=[("All files", "*.*")])
                if save_path:
                    with open(save_path, "wb") as file:
                        file.write(decrypted_data)
                    log_file_action(app.logged_in_user, file_path, "decrypt")
                else:
                    messagebox.showerror("Error", "File save cancelled.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt file {file_path}: {str(e)}")
        messagebox.showinfo("Success", "Files decrypted successfully!")
    else:
        messagebox.showerror("Error", "Please select up to 3 files.")

def check_compliance(app):
    """Überprüft die DSGVO-Compliance eines Passworts"""
    password = app.password_entry.get()
    violations = app.compliance.check_compliance({"password": password})
    if violations:
        report = app.compliance.generate_report(violations)
        messagebox.showerror("Compliance Report", report)
    else:
        messagebox.showinfo("Compliance Report", "No compliance violations found.")

def send_user_notification(app):
    """Sendet eine Benachrichtigung an alle oder einen bestimmten Benutzer"""
    recipient = simpledialog.askstring("Send Notification", "Enter recipient username (or 'all' for everyone):")
    message = simpledialog.askstring("Send Notification", "Enter your message:")

    if recipient and message:
        if recipient == "all":
            for user in app.users:
                send_notification(user, app.logged_in_user, message, None)
            send_admin_notification(f"Admin {app.logged_in_user} sent a message to all users: {message}", app.users)
        elif recipient in app.users:
            send_notification(recipient, app.logged_in_user, message, None)
            send_admin_notification(f"Admin {app.logged_in_user} sent a message to {recipient}: {message}", app.users)
        else:
            messagebox.showerror("Error", "Recipient username not found.")
        messagebox.showinfo("Success", f"Message sent to {recipient} successfully.")
    else:
        messagebox.showerror("Error", "Recipient and message cannot be empty.")

def view_received_files(app):
    """Zeigt die empfangenen Dateien an und ermöglicht das Öffnen oder Löschen"""
    app.clear_screen()

    frame = ttk.Frame(app.root, padding=20)
    frame.pack(fill='both', expand=True)

    received_files = get_received_files(app.logged_in_user)
    if received_files:
        for file_info in received_files:
            file_path = file_info['file_path']
            sender = file_info['sender']
            password = file_info.get('password', 'No password provided')

            file_frame = ttk.Frame(frame, padding=5)
            file_frame.pack(fill='x', pady=5)

            ttk.Label(file_frame, text=f"File: {file_path} from {sender}").pack(side=tk.LEFT, padx=10)
            ttk.Button(file_frame, text="Copy Password", command=lambda pw=password: copy_to_clipboard(pw)).pack(side=tk.RIGHT, padx=5)
            ttk.Button(file_frame, text="Decrypt and Open", command=lambda fp=file_path, pw=password: decrypt_and_open_file(app, fp, pw)).pack(side=tk.RIGHT, padx=5)
            ttk.Button(file_frame, text="Delete", command=lambda fp=file_path: delete_received_file(app, fp)).pack(side=tk.RIGHT, padx=5)
    else:
        ttk.Label(frame, text="No received files.").pack(pady=20)

    ttk.Button(frame, text="Back", command=app.main_screen).pack(pady=10)

def copy_to_clipboard(text):
    """Kopiert den angegebenen Text in die Zwischenablage"""
    pyperclip.copy(text)
    messagebox.showinfo("Info", "Password copied to clipboard")

def decrypt_and_open_file(app, file_path, password):
    """Entschlüsselt eine geteilte Datei und öffnet sie"""
    confirm = messagebox.askyesno("Decrypt and Open File", "Do you want to decrypt and open the file?")
    if confirm:
        try:
            with open(file_path, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = decrypt(encrypted_data, password)

            temp_path = file_path[:-7]  # Entferne ".shared"
            with open(temp_path, "wb") as temp_file:
                temp_file.write(decrypted_data)
            os.remove(file_path)  # Entferne die .shared-Datei
            os.startfile(temp_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt and open file {file_path}: {str(e)}")

def delete_received_file(app, file_path):
    """Löscht eine empfangene Datei"""
    received_files = get_received_files(app.logged_in_user)
    updated_files = [f for f in received_files if f['file_path'] != file_path]

    with open(os.path.join("json", "notifications.json"), "r") as file:
        notifications = json.load(file)

    notifications[app.logged_in_user] = updated_files

    with open(os.path.join("json", "notifications.json"), "w") as file:
        json.dump(notifications, file, indent=4)

    messagebox.showinfo("Success", f"File {file_path} deleted successfully.")
    view_received_files(app)

def view_user_activity(app):
    """Zeigt das Benutzeraktivitätsprotokoll an"""
    activity_log = get_user_activity_log(app.logged_in_user)
    activity_text = "\n".join(activity_log)
    messagebox.showinfo("User Activity Log", f"Your activity log:\n{activity_text}")

def get_unread_notification_count(app):
    """Gibt die Anzahl ungelesener Benachrichtigungen zurück"""
    notifications = get_received_files(app.logged_in_user)
    return len(notifications)

def share_file_securely(app):
    """Teilt eine Datei sicher mit einem anderen Benutzer"""
    file_path = filedialog.askopenfilename(title="Select a file to share", filetypes=[("All files", "*.*")])
    if file_path:
        recipient = simpledialog.askstring("Share File", "Enter recipient username:")
        if recipient in app.users:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            try:
                with open(file_path, "rb") as file:
                    data = file.read()
                encrypted_data = encrypt(data, password)
                shared_file_path = f"{file_path}.shared"
                with open(shared_file_path, "wb") as file:
                    file.write(encrypted_data)
                send_notification(recipient, app.logged_in_user, shared_file_path, password)
                messagebox.showinfo("Success", f"File {file_path} shared securely with {recipient}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to share file {file_path}: {str(e)}")
        else:
            messagebox.showerror("Error", "Recipient username not found.")
    else:
        messagebox.showerror("Error", "File selection cancelled.")
