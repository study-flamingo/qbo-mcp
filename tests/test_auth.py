"""Tests for the lazy/expiry-aware authentication service."""

import json
import time
from datetime import date

import pytest

from qbo_mcp.auth import QBOService
from qbo_mcp.config import QBOConfig


class FakeAuthClient:
    """Stands in for intuitlib AuthClient without any network access."""

    def __init__(self, expires_in=3600):
        self.access_token = "access"
        self.refresh_token = "refresh"
        self.realm_id = "123"
        self.environment = "sandbox"
        self.expires_in = expires_in
        self.refresh_calls = 0

    def refresh(self):
        self.refresh_calls += 1
        self.access_token = "access-new"
        self.refresh_token = "refresh-new"


def _config(tmp_path):
    cfg = QBOConfig()
    cfg.token_file = tmp_path / "tokens.json"
    return cfg


def test_init_does_not_create_auth_client(tmp_path):
    """Construction must be side-effect free (no AuthClient => no discovery call)."""
    cfg = _config(tmp_path)
    cfg.token_file.write_text(
        json.dumps(
            {
                "access_token": "a",
                "refresh_token": "r",
                "realm_id": "1",
                "expires_at": time.time() + 3600,
            }
        )
    )
    svc = QBOService(config=cfg)
    assert svc._auth_client is None


def test_ensure_authenticated_skips_refresh_when_token_valid(tmp_path):
    cfg = _config(tmp_path)
    svc = QBOService(config=cfg)
    svc._auth_client = FakeAuthClient()
    svc._tokens = {
        "access_token": "a",
        "refresh_token": "r",
        "realm_id": "1",
        "expires_at": time.time() + 3600,
    }

    assert svc.ensure_authenticated() is True
    assert svc._auth_client.refresh_calls == 0


def test_ensure_authenticated_refreshes_when_expired(tmp_path):
    cfg = _config(tmp_path)
    svc = QBOService(config=cfg)
    svc._auth_client = FakeAuthClient()
    svc._tokens = {
        "access_token": "a",
        "refresh_token": "r",
        "realm_id": "1",
        "expires_at": time.time() - 10,  # already expired
    }

    assert svc.ensure_authenticated() is True
    assert svc._auth_client.refresh_calls == 1
    # new expiry recorded and persisted
    saved = json.loads(cfg.token_file.read_text())
    assert saved["access_token"] == "access-new"
    assert saved["expires_at"] > time.time()


def test_ensure_authenticated_non_interactive_raises_without_tokens(tmp_path):
    cfg = _config(tmp_path)
    svc = QBOService(config=cfg)
    svc._auth_client = FakeAuthClient()
    svc._auth_client.access_token = None
    svc._auth_client.refresh_token = None
    svc._tokens = {}

    with pytest.raises(ValueError):
        svc.ensure_authenticated(interactive=False)
