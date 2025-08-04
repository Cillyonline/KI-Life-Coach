# KI Life Coach Bot

Ein KI-gestützter LifeCoach-Bot mit Mood-Tracking, GPT-Reflexionsdialogen, Habit-Tracking und optionalem Webinterface.

## Installation

1. Python 3.11+ installieren.
2. Repository klonen und Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example` kopieren und API-Schlüssel eintragen:
   ```bash
   cp .env.example .env
   ```
4. Bot starten:
   ```bash
   python bot/main.py
   ```

## Roadmap

### Phase 1 – Basisfunktionen
- Telegram-Bot mit GPT-Reflexionsdialog
- Mood-Tracking
- Persistenz mit SQLite

### Phase 2 – Habits & Analytics
- Habit-Tracking und Auswertung
- Visualisierung mit Matplotlib

### Phase 3 – Web & Skalierung
- Optionales Flask-Webinterface
- Umstieg auf Postgres
- Deployment & CI/CD

## Hinweise für Entwickler
- OpenAI-API: Verwende das offizielle `openai`-Package und setze den API-Key über die `.env`.
- Telegram-API: `python-telegram-bot` nutzt asynchrone Handler; achte auf robuste Fehlerbehandlung und Logging.
