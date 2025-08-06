"""Tests for the mood tracking service."""

from datetime import date, datetime
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services import mood_service


def test_save_and_get_mood(tmp_path) -> None:
    """Mood entries can be saved and retrieved."""
    db = tmp_path / "mood.db"
    mood_service.init_db(db)
    now = datetime(2024, 1, 1, 12, 0)
    mood_service.save_mood(1, "😊", now, db)
    moods = mood_service.get_moods(1, date(2024, 1, 1), date(2024, 1, 1), db)
    assert moods[0][1] == "😊"


def test_duplicate_mood_raises(tmp_path) -> None:
    """Saving two moods on the same day raises an error."""
    db = tmp_path / "mood.db"
    mood_service.init_db(db)
    now = datetime(2024, 1, 1, 8, 0)
    mood_service.save_mood(1, "gut", now, db)
    with pytest.raises(ValueError):
        mood_service.save_mood(1, "schlecht", now, db)
