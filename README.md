# SecureDataHub 3.0

## Beschreibung
SecureDataHub 3.0 ist eine fortschrittliche Plattform für die sichere Verwaltung und Verschlüsselung von Daten. Dieses Projekt wurde entwickelt, um modernste Sicherheits- und Datenschutzfunktionen zu bieten, einschließlich Zwei-Faktor-Authentifizierung (2FA), umfassender Protokollierung und Compliance-Überwachung.

## Installation
Folgen Sie diesen Schritten, um das Projekt lokal zu installieren und auszuführen:

1. Klonen Sie das Repository:
    ```bash
    git clone https://github.com/hichem-a/SecureDataHubv3.0.git
    cd SecureDataHubv3.0
    ```

2. Erstellen und aktivieren Sie eine virtuelle Umgebung:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Für Windows: venv\Scripts\activate
    ```

3. Installieren Sie die Abhängigkeiten:
    ```bash
    pip install -r requirements.txt
    ```

4. Führen Sie die Anwendung aus:
    ```bash
    python main.py
    ```

## Verwendung
Nach dem Start der Anwendung wird der Anmeldebildschirm angezeigt. Als Administrator können Sie Benutzer hinzufügen, Richtlinien bearbeiten und Benachrichtigungen verwalten. Reguläre Benutzer können Dateien sicher hochladen, verschlüsseln und teilen.

## Funktionen
| Funktion                   | Beschreibung                                                                                                                                              |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Benutzerverwaltung         | Hinzufügen, Löschen und Bearbeiten von Benutzern.                                                                                                          |
| Zwei-Faktor-Authentifizierung (2FA) | Erhöhte Sicherheit durch 2FA. Benutzer können 2FA aktivieren, um ihre Konten zu schützen.                                                                 |
| Dateiverschlüsselung       | Dateien können sicher verschlüsselt und entschlüsselt werden.                                                                                             |
| Protokollierung            | Detaillierte Protokollierung von Benutzeraktionen, einschließlich Dateioperationen und Anmeldungen.                                                        |
| Compliance-Überwachung     | Automatische Überwachung und Berichterstattung über die Einhaltung von Datenschutzrichtlinien.                                                            |
| Benachrichtigungssystem    | Senden und Empfangen von Benachrichtigungen innerhalb der Plattform.                                                                                       |
| Dashboard                  | Übersicht über Benutzerstatistiken, aktuelle Aktivitäten und Compliance-Status.                                                                           |

## Technologien
- Python
- Tkinter
- TTK Themes
- pyotp
- cryptography

## Mitwirkende
- **Hichem Abdenadher** - [hichem-a](https://github.com/hichem-a)

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.
