"""SQLite-backed mood tracking service."""

from __future__ import annotations

import logging
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "mood.db"


def init_db(db_path: Path | str = DB_PATH) -> None:
    """Initialize the SQLite database for mood tracking.

    Creates the database file and required table if they do not yet exist.

    Args:
        db_path: Path to the SQLite database file.
    """
    try:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    mood TEXT NOT NULL,
                    timestamp DATETIME NOT NULL
                )
                """
            )
    except sqlite3.Error:
        logger.exception("Failed to initialize mood database")
        raise


def has_entry_for_date(
    user_id: int, day: date, db_path: Path | str = DB_PATH
) -> bool:
    """Check whether a mood entry exists for a specific day.

    Args:
        user_id: Telegram user identifier.
        day: Date for which to check.
        db_path: Path to the SQLite database file.

    Returns:
        True if an entry for the user on ``day`` exists, otherwise False.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                "SELECT 1 FROM moods WHERE user_id = ? AND DATE(timestamp) = ?",
                (user_id, day.isoformat()),
            )
            return cur.fetchone() is not None
    except sqlite3.Error:
        logger.exception("Database error while checking existing mood")
        raise


def save_mood(
    user_id: int,
    mood: str,
    timestamp: datetime | None = None,
    db_path: Path | str = DB_PATH,
) -> None:
    """Store a mood entry for a user.

    Args:
        user_id: Telegram user identifier.
        mood: Mood description or emoji.
        timestamp: Time of the entry; defaults to current UTC time.
        db_path: Path to the SQLite database file.

    Raises:
        ValueError: If a mood for the user has already been recorded today.
    """
    ts = timestamp or datetime.utcnow()
    if has_entry_for_date(user_id, ts.date(), db_path=db_path):
        raise ValueError("Mood already recorded for today")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO moods (user_id, mood, timestamp) VALUES (?, ?, ?)",
                (user_id, mood, ts.isoformat()),
            )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to save mood for user %s", user_id)
        raise


def get_moods(
    user_id: int,
    start_date: date,
    end_date: date,
    db_path: Path | str = DB_PATH,
) -> List[Tuple[datetime, str]]:
    """Return mood entries for a user within a date range.

    Args:
        user_id: Telegram user identifier.
        start_date: Start date (inclusive).
        end_date: End date (inclusive).
        db_path: Path to the SQLite database file.

    Returns:
        List of tuples ``(timestamp, mood)`` ordered by timestamp ascending.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                """
                SELECT timestamp, mood FROM moods
                WHERE user_id = ? AND DATE(timestamp) BETWEEN ? AND ?
                ORDER BY timestamp ASC
                """,
                (user_id, start_date.isoformat(), end_date.isoformat()),
            )
            rows = cur.fetchall()
            return [
                (datetime.fromisoformat(ts), mood) for ts, mood in rows
            ]
    except sqlite3.Error:
        logger.exception("Failed to fetch moods for user %s", user_id)
        raise


def get_last_mood(
    user_id: int, db_path: Path | str = DB_PATH
) -> Tuple[datetime, str] | None:
    """Return the most recent mood entry for a user.

    Args:
        user_id: Telegram user identifier.
        db_path: Path to the SQLite database file.

    Returns:
        Tuple of ``(timestamp, mood)`` or ``None`` if no entries exist.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                "SELECT timestamp, mood FROM moods WHERE user_id = ? "
                "ORDER BY timestamp DESC LIMIT 1",
                (user_id,),
            )
            row = cur.fetchone()
            return (datetime.fromisoformat(row[0]), row[1]) if row else None
    except sqlite3.Error:
        logger.exception("Failed to fetch last mood for user %s", user_id)
        raise


def export_moods_to_csv(
    user_id: int, file_path: Path | str, db_path: Path | str = DB_PATH
) -> None:
    """Export moods for a user to a CSV file.

    Args:
        user_id: Telegram user identifier.
        file_path: Destination path for the CSV file.
        db_path: Path to the SQLite database file.
    """
    import csv

    try:
        moods = get_moods(user_id, date.min, date.max, db_path=db_path)
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamp", "mood"])
            for ts, mood in moods:
                writer.writerow([ts.isoformat(), mood])
    except Exception:
        logger.exception("Failed to export moods to CSV for user %s", user_id)
        raise
