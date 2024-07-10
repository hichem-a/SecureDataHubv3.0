import tkinter as tk
from tkinter import simpledialog

class PolicyEditor:
    def __init__(self, master, compliance):
        self.top = tk.Toplevel(master)
        self.top.title("Edit Compliance Policies")
        self.top.geometry("500x400")
        self.compliance = compliance
        self.create_widgets()

    def create_widgets(self):
        self.policy_listbox = tk.Listbox(self.top)
        self.policy_listbox.pack(fill=tk.BOTH, expand=True)

        for policy_name in self.compliance.policies:
            self.policy_listbox.insert(tk.END, policy_name)

        btn_frame = tk.Frame(self.top)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Add Policy", command=self.add_policy).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="Edit Policy", command=self.edit_policy).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(btn_frame, text="Delete Policy", command=self.delete_policy).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def add_policy(self):
        policy_name = simpledialog.askstring("Policy Name", "Enter policy name:")
        if policy_name:
            self.compliance.policies[policy_name] = {
                "description": simpledialog.askstring("Description", "Enter policy description:"),
                "requirement": simpledialog.askboolean("Requirement", "Is this requirement mandatory?"),
                "article": simpledialog.askstring("Article", "Enter the related DSGVO article number:")
            }
            self.compliance.update_policies(self.compliance.policies)
            self.policy_listbox.insert(tk.END, policy_name)

    def edit_policy(self):
        selected_policy = self.policy_listbox.get(tk.ACTIVE)
        if selected_policy:
            self.compliance.policies[selected_policy] = {
                "description": simpledialog.askstring("Description", "Enter policy description:", initialvalue=self.compliance.policies[selected_policy]["description"]),
                "requirement": simpledialog.askboolean("Requirement", "Is this requirement mandatory?", initialvalue=self.compliance.policies[selected_policy]["requirement"]),
                "article": simpledialog.askstring("Article", "Enter the related DSGVO article number:", initialvalue=self.compliance.policies[selected_policy]["article"])
            }
            self.compliance.update_policies(self.compliance.policies)

    def delete_policy(self):
        selected_policy = self.policy_listbox.get(tk.ACTIVE)
        if selected_policy:
            del self.compliance.policies[selected_policy]
            self.compliance.update_policies(self.compliance.policies)
            self.policy_listbox.delete(tk.ACTIVE)
