# Testkatalog – MVP

Dieser Katalog dokumentiert Tests für den Minimal Viable Product (MVP) des KI‑Life‑Coach‑Bots. Die Tests folgen der Philosophie "früh validieren, kontinuierlich automatisieren" und werden nach jedem Release-Zyklus überprüft.

## Testübersicht

| Modul/Funktion | Testfall | Beschreibung | Testschritte | Erwartetes Ergebnis | Status | Automatisiert? |
| --- | --- | --- | --- | --- | :---: | :---: |
| Telegram-Bot | Startbefehl akzeptiert | Bot reagiert auf `/start` mit Begrüßung | 1. Bot starten\n2. `/start` senden | Begrüßungsnachricht wird gesendet | 🟩 | Ja |
| Telegram-Bot | Ungültiger Befehl | Bot erhält unbekannten Befehl | 1. Bot starten\n2. `/unknown` senden | Bot meldet unbekannten Befehl ohne Absturz | 🟥 | Geplant |
| Mood-Tracking | Stimmung speichern | Stimmung wird per `/mood` gespeichert | 1. `/mood happy` senden\n2. Datenbank prüfen | Stimmungseintrag in DB vorhanden | 🟩 | Ja |
| Mood-Tracking | Mehrfache Stimmung am Tag | Zweite Stimmung am selben Tag senden | 1. `/mood happy` senden\n2. erneut `/mood sad` senden | System weist auf bereits erfasste Stimmung hin | 🟥 | Nein |
| GPT-Coaching | Reflexion generieren | GPT erzeugt eine Reflexionsantwort | 1. `/reflect Hallo` senden | Antwort wird von OpenAI generiert | 🟩 | Ja |
| GPT-Coaching | API-Ausfall | OpenAI nicht erreichbar | 1. Netzwerk trennen\n2. `/reflect` senden | Fehlermeldung mit Logging, Bot bleibt stabil | 🟥 | Geplant |

## Pflege & Verantwortung

- **Aktualisierung:** Nach jedem Testlauf wird der Status in dieser Tabelle angepasst.
- **Verantwortlich:** QA-Team (z. B. QA-Engineer des Projekts).

