"""Tests for :mod:`services.gpt_service`."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import sys

import openai
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.gpt_service import GPTService


def _fake_chat_completion_create(**_: dict) -> dict:
    return {"choices": [{"message": {"content": "Reflexion"}}]}


def test_generate_reflection(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Ensure ``generate_reflection`` returns text and logs interactions."""
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(openai.ChatCompletion, "create", _fake_chat_completion_create)
    log_file = tmp_path / "log.json"
    service = GPTService(log_path=log_file)
    result = service.generate_reflection("Prompt", user_id=1, style="analytisch")
    assert result == "Reflexion"
    data = json.loads(log_file.read_text())
    user_hash = sha256(b"1").hexdigest()
    assert user_hash in data
    assert data[user_hash][0]["prompt"] == "Prompt"
