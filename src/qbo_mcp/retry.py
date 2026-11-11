"""Retry/backoff helpers for QuickBooks API calls.

QuickBooks Online throttles at roughly 500 requests/minute and can return
transient 429/5xx responses. These helpers add bounded exponential backoff with
jitter, and a structured description of QBO errors (``QuickbooksException``
carries ``error_code``, ``message`` and ``detail``).
"""

import logging
import random
import time

import requests

logger = logging.getLogger(__name__)

# QBO error codes / HTTP statuses worth retrying.
RETRYABLE_ERROR_CODES = {3000, 429, 500, 502, 503, 504}
_RETRYABLE_HINTS = (
    "429",
    "500",
    "502",
    "503",
    "504",
    "throttl",
    "rate limit",
    "too many requests",
    "timeout",
)


def is_retryable(exc: Exception) -> bool:
    """True if the exception looks transient and a retry could plausibly succeed."""
    if isinstance(exc, requests.exceptions.RequestException):
        return True
    code = getattr(exc, "error_code", None)
    if isinstance(code, int) and code in RETRYABLE_ERROR_CODES:
        return True
    msg = str(exc).lower()
    return any(hint in msg for hint in _RETRYABLE_HINTS)


def describe_qbo_error(exc: Exception) -> dict:
    """Return a structured description of a QBO error, for tool responses."""
    return {
        "error_code": getattr(exc, "error_code", None),
        "message": getattr(exc, "message", str(exc)),
        "detail": getattr(exc, "detail", ""),
    }


def call_with_retry(
    fn,
    *args,
    attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    sleep=time.sleep,
    **kwargs,
):
    """Call ``fn(*args, **kwargs)`` with bounded exponential backoff on transient errors.

    Non-retryable errors and the final attempt raise immediately.
    """
    for attempt in range(1, attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001 - re-raised when not retryable / out of attempts
            if attempt >= attempts or not is_retryable(e):
                raise
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            delay += random.uniform(0, base_delay)
            logger.warning(
                f"Retryable QBO error (attempt {attempt}/{attempts}): {e}; retrying in {delay:.2f}s"
            )
            sleep(delay)
