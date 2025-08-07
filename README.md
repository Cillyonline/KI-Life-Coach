# ki-life-coach-bot

Ein KI-gestützter LifeCoach-Bot mit Fokus auf persönliches Wachstum durch Mood-Tracking, GPT-Coaching und Habit-Tracking.

## Ziele
- Mood-Tracking
- GPT-Coaching
- Habit-Tracking

## Roadmap

### Phase 1 – Telegram-Bot, Mood & GPT
- Telegram-Bot
- Mood-Tracking
- GPT-Reflexionen

### Phase 2 – Analytics & Micro-Learnings
- Analytics
- Micro-Learnings

### Phase 3 – Web & Teams
- Webintegration
- Teamfunktionen

## Installation & Setup

1. Python 3.11+ installieren.
2. Repository klonen und Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example` kopieren und API-Schlüssel eintragen:
   ```bash
   cp .env.example .env
   ```
   Beispielinhalt der `.env`:
   ```env
   TELEGRAM_TOKEN=dein-telegram-token
   OPENAI_API_KEY=dein-openai-key
   ```
4. Bot starten:
   ```bash
   python bot/main.py
   ```

## API-Keys & Security

- **Keine Secrets im Code**: API-Schlüssel werden ausschließlich über Umgebungsvariablen bezogen.
- **GitHub Actions**: In der Repo-Oberfläche unter `Settings > Secrets and variables > Actions` können `TELEGRAM_TOKEN` und `OPENAI_API_KEY` als Secrets hinterlegt werden.
- **Lokale Entwicklung**: Nutze eine `.env`-Datei (siehe `.env.example`). Diese Datei ist durch `.gitignore` geschützt und darf nie committet werden.
- **Logging**: Es werden nur anonymisierte GPT-Logs ohne personenbezogene Daten gespeichert.

## GPT-Integration

- `/reflect [stil] <text>` startet einen Reflexionsdialog. Unterstützte Stile: `motivierend`, `analytisch`, `humorvoll`.
- Der letzte Mood-Eintrag wird zusammen mit dem optionalen Text zu einem Prompt kombiniert und an GPT (z. B. `gpt-3.5-turbo`) gesendet.
- Die Prompts folgen dem Schema: `Ziel → Kontext → Frage → Ausgabeformat`.
- Antworten werden dem User als Textnachricht ausgegeben; Fehler werden verständlich kommuniziert.
- Die letzten fünf Interaktionen werden pro Nutzer anonymisiert lokal protokolliert.

## Mood-Tracking

- `/mood <stimmung>` speichert deine tägliche Stimmung.
- `/moodstats` zeigt eine Übersicht der letzten sieben Tage.
- Die SQLite-Datenbank wird automatisch initialisiert und liegt unter `data/mood.db`.
- Für manuelle Initialisierung: `from services.mood_service import init_db; init_db()`

## Hinweise für Entwickler
- OpenAI-API: Verwende das offizielle `openai`-Package und setze den API-Key über die `.env`.
- Telegram-API: `python-telegram-bot` nutzt asynchrone Handler; achte auf robuste Fehlerbehandlung und Logging.

## Teststrategie & Testkataloge

Die Qualitätssicherung erfolgt meilensteinorientiert. Für jeden Milestone existiert ein eigener Testkatalog mit manuellen und automatisierten Tests. Automatisierte Tests werden mit `pytest` ausgeführt, während manuelle Tests Nutzerinteraktionen und Edge Cases abdecken.

Alle Testkataloge im Überblick:

- [Zentrale Übersicht](TESTKATALOG.md)
- [MVP](TESTKATALOG_MVP.md)
- [Mood](TESTKATALOG_MOOD.md)
- [GPT](TESTKATALOG_GPT.md)
- [Habits](TESTKATALOG_HABITS.md)

