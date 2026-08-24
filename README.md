# Streamlit Taschenrechner App 🧮

Eine interaktive Taschenrechner-Webanwendung, gebaut mit Python und Streamlit.

## Features
- **Tastenfeld-GUI:** Vollständig bedienbar über interaktive Buttons.
- **Grundrechenarten:** Addition, Subtraktion, Multiplikation und Division.
- **Spezialfunktionen:** Clear (C), Backspace (⌫), Vorzeichenwechsel (+/-) und Prozentrechnung (%).
- **Fehlerbehandlung:** Bucht Division durch Null sauber ab.
- **State-Management:** Zuverlässige Speicherung der Zustände via `st.session_state`.

## Lokale Installation & Start

1. **Repository klonen oder Dateien herunterladen.**
2. **Virtuelle Umgebung erstellen (optional, aber empfohlen):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
