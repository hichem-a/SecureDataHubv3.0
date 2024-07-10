import json
import os

JSON_DIR = os.path.join(os.path.dirname(__file__), "..", "json")

def ensure_json_dir_exists():
    """Stellt sicher, dass der JSON-Ordner existiert"""
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

class Compliance:
    def __init__(self):
        self.policies = self.load_policies()

    def load_policies(self):
        """Lädt die Compliance-Richtlinien aus einer JSON-Datei"""
        ensure_json_dir_exists()
        if not os.path.exists(os.path.join(JSON_DIR, "policies.json")):
            return {}
        with open(os.path.join(JSON_DIR, "policies.json"), "r") as file:
            return json.load(file)

    def update_policies(self, policies):
        """Aktualisiert die Compliance-Richtlinien"""
        with open(os.path.join(JSON_DIR, "policies.json"), "w") as file:
            json.dump(policies, file, indent=4)

    def check_compliance(self, data):
        """Überprüft die DSGVO-Compliance"""
        violations = []
        for policy, details in self.policies.items():
            if details["requirement"] and not data.get(policy):
                violations.append(f"Policy {policy}: {details['description']} (Article {details['article']})")
        return violations

    def generate_report(self, violations):
        """Erstellt einen Compliance-Bericht"""
        return "\n".join(violations)
