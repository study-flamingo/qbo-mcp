"""Tests for retry/backoff helpers."""

import pytest
from quickbooks.exceptions import ValidationException

from qbo_mcp.retry import call_with_retry, describe_qbo_error, is_retryable


def test_is_retryable_throttle_code():
    assert is_retryable(ValidationException("ThrottleExceeded", 3000, "")) is True


def test_is_retryable_validation_not_retryable():
    assert is_retryable(ValidationException("bad input", 2000, "")) is False


def test_describe_qbo_error():
    d = describe_qbo_error(ValidationException("bad input", 2000, "some detail"))
    assert d["error_code"] == 2000
    assert d["message"] == "bad input"
    assert d["detail"] == "some detail"


def test_success_first_try():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        return "ok"

    assert call_with_retry(fn, sleep=lambda _: None) == "ok"
    assert calls["n"] == 1


def test_retries_then_succeeds():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValidationException("ThrottleExceeded", 3000, "")
        return "ok"

    assert call_with_retry(fn, attempts=3, sleep=lambda _: None) == "ok"
    assert calls["n"] == 2


def test_non_retryable_raises_immediately():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise ValidationException("bad input", 2000, "")

    with pytest.raises(ValidationException):
        call_with_retry(fn, attempts=3, sleep=lambda _: None)
    assert calls["n"] == 1


def test_exhausts_attempts():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise ValidationException("ThrottleExceeded", 3000, "")

    with pytest.raises(ValidationException):
        call_with_retry(fn, attempts=3, sleep=lambda _: None)
    assert calls["n"] == 3
