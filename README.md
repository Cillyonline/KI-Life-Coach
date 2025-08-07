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

