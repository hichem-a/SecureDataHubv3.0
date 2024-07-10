from tkinter import ttk

from functions.ui_functions import delete_my_account


def main_screen(self):
    """Erstellt die Hauptoberfläche der Anwendung"""
    self.clear_screen()

    main_frame = ttk.Frame(self.root, padding=20)
    main_frame.pack(fill='both', expand=True)

    ttk.Label(main_frame, text="SecureDataHub", font=("Helvetica", 24, 'bold')).pack(pady=20)

    dashboard_frame = ttk.Frame(main_frame)
    dashboard_frame.pack(fill='both', expand=True, pady=10)

    ttk.Label(dashboard_frame, text="Dashboard", font=("Helvetica", 18, 'bold')).pack(pady=10)

    stats_frame = ttk.Frame(dashboard_frame)
    stats_frame.pack(fill='x', expand=True, pady=10)

    ttk.Label(stats_frame, text="User Statistics", font=("Helvetica", 14, 'bold')).pack(pady=5)
    ttk.Label(stats_frame, text=f"Total Users: {len(self.users)}").pack(pady=5)
    ttk.Label(stats_frame, text=f"Admins: {len([u for u in self.users.values() if u['role'] == 'admin'])}").pack(pady=5)
    ttk.Label(stats_frame, text=f"Regular Users: {len([u for u in self.users.values() if u['role'] == 'user'])}").pack(pady=5)

    ttk.Label(stats_frame, text="Recent Activities", font=("Helvetica", 14, 'bold')).pack(pady=10)
    # Hier könntest du eine Liste der letzten Aktivitäten hinzufügen

    compliance_frame = ttk.Frame(dashboard_frame)
    compliance_frame.pack(fill='x', expand=True, pady=10)

    ttk.Label(compliance_frame, text="Compliance Status", font=("Helvetica", 14, 'bold')).pack(pady=5)
    # Hier könntest du den aktuellen Compliance-Status anzeigen

    # Weitere Widgets für das Dashboard hinzufügen

    footer_frame = ttk.Frame(self.root, padding=10)
    footer_frame.pack(side='bottom', fill='x')

    self.footer_label = ttk.Label(footer_frame, text=f"Logged in as {self.logged_in_user} ({self.user_role}) - SecureDataHub by Mr H", font=("Helvetica", 10))
    self.footer_label.pack(side='left', padx=10)

    ttk.Button(footer_frame, text="Delete My Account", command=lambda: delete_my_account(self)).pack(side='right')
