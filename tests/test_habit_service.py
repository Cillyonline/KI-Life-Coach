"""Tests for the habit tracking service."""

from datetime import date
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services import habit_service


def test_create_and_complete_habit(tmp_path) -> None:
    """Habits can be created and marked as completed."""
    db = tmp_path / "habits.db"
    habit_service.init_db(db)
    habit_id = habit_service.create_habit(1, "lesen", db)
    habit_service.complete_habit(1, habit_id, date(2024, 1, 1), db)
    habits = habit_service.get_user_habits(1, db)
    assert habits[0]["streak"] == 1


def test_streak_calculation(tmp_path) -> None:
    """Streak increases with consecutive completions."""
    db = tmp_path / "habits.db"
    habit_service.init_db(db)
    habit_id = habit_service.create_habit(1, "laufen", db)
    habit_service.complete_habit(1, habit_id, date(2024, 1, 1), db)
    habit_service.complete_habit(1, habit_id, date(2024, 1, 2), db)
    streak = habit_service.get_habit_streak(1, habit_id, db)
    assert streak == 2
