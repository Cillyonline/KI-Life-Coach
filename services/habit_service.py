"""SQLite-backed habit tracking service."""

from __future__ import annotations

import logging
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "habits.db"


def init_db(db_path: Path | str = DB_PATH) -> None:
    """Initialize the SQLite database for habit tracking.

    Creates the database file and required tables if they do not yet exist.

    Args:
        db_path: Path to the SQLite database file.
    """
    try:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    streak INTEGER NOT NULL DEFAULT 0,
                    UNIQUE(user_id, name)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS habit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    log_date DATE NOT NULL,
                    UNIQUE(habit_id, log_date),
                    FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
                )
                """
            )
    except sqlite3.Error:
        logger.exception("Failed to initialize habit database")
        raise


def create_habit(user_id: int, name: str, db_path: Path | str = DB_PATH) -> int:
    """Create a new habit for a user.

    Args:
        user_id: Telegram user identifier.
        name: Name of the habit.
        db_path: Path to the SQLite database file.

    Returns:
        The ID of the newly created habit.

    Raises:
        ValueError: If a habit with the same name already exists for the user.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                "INSERT INTO habits (user_id, name, created_at) VALUES (?, ?, ?)",
                (user_id, name, datetime.utcnow().isoformat()),
            )
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError as exc:
        logger.warning("Habit creation failed for user %s: %s", user_id, exc)
        raise ValueError("Habit name already exists") from exc
    except sqlite3.Error:
        logger.exception("Database error while creating habit for user %s", user_id)
        raise


def complete_habit(
    user_id: int,
    habit_id: int,
    log_date: date | None = None,
    db_path: Path | str = DB_PATH,
) -> None:
    """Mark a habit as completed for a specific day.

    Args:
        user_id: Telegram user identifier.
        habit_id: Identifier of the habit.
        log_date: Date of completion; defaults to today.
        db_path: Path to the SQLite database file.

    Raises:
        ValueError: If the habit does not belong to the user.
    """
    day = log_date or date.today()
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                "SELECT 1 FROM habits WHERE id = ? AND user_id = ?",
                (habit_id, user_id),
            )
            if cur.fetchone() is None:
                raise ValueError("Habit not found")

            conn.execute(
                "INSERT OR IGNORE INTO habit_log (habit_id, log_date) VALUES (?, ?)",
                (habit_id, day.isoformat()),
            )

            streak = _calculate_streak(conn, habit_id, day)
            conn.execute(
                "UPDATE habits SET streak = ? WHERE id = ?",
                (streak, habit_id),
            )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to complete habit %s for user %s", habit_id, user_id)
        raise


def _calculate_streak(conn: sqlite3.Connection, habit_id: int, day: date) -> int:
    """Calculate the current streak for a habit."""
    cur = conn.execute(
        "SELECT log_date FROM habit_log WHERE habit_id = ? ORDER BY log_date DESC",
        (habit_id,),
    )
    streak = 0
    expected = day
    for (log_date_str,) in cur.fetchall():
        log_day = date.fromisoformat(log_date_str)
        if log_day == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif log_day < expected:
            break
    return streak


def get_user_habits(
    user_id: int, db_path: Path | str = DB_PATH
) -> List[Dict[str, object]]:
    """Return all habits for a user including recent history.

    Args:
        user_id: Telegram user identifier.
        db_path: Path to the SQLite database file.

    Returns:
        List of dictionaries containing habit details and the last seven days of
        completion history.
    """
    start_day = date.today() - timedelta(days=6)
    try:
        with sqlite3.connect(db_path) as conn:
            habits_cur = conn.execute(
                "SELECT id, name, streak FROM habits WHERE user_id = ? ORDER BY id",
                (user_id,),
            )
            habits = []
            for habit_id, name, streak in habits_cur.fetchall():
                log_cur = conn.execute(
                    """
                    SELECT log_date FROM habit_log
                    WHERE habit_id = ? AND log_date >= ?
                    """,
                    (habit_id, start_day.isoformat()),
                )
                logs = {date.fromisoformat(d[0]) for d in log_cur.fetchall()}
                habits.append(
                    {
                        "id": habit_id,
                        "name": name,
                        "streak": streak,
                        "logs": logs,
                    }
                )
            return habits
    except sqlite3.Error:
        logger.exception("Failed to fetch habits for user %s", user_id)
        raise


def get_habit_streak(
    user_id: int, habit_id: int, db_path: Path | str = DB_PATH
) -> int:
    """Return the current streak for a habit."""
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.execute(
                "SELECT streak FROM habits WHERE id = ? AND user_id = ?",
                (habit_id, user_id),
            )
            row = cur.fetchone()
            return row[0] if row else 0
    except sqlite3.Error:
        logger.exception(
            "Failed to fetch streak for habit %s of user %s", habit_id, user_id
        )
        raise
