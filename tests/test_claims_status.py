from src.claims_status import get_status


def test_returns_three_fields():
    out = get_status("C-1", lambda _: {
        "state": "in_review", "next_step": "call", "expected_date": "2026-07-01",
        "extra": "should be dropped",
    })
    assert set(out) == {"status", "next_step", "expected_date"}


def test_rejects_unknown_state():
    try:
        get_status("C-1", lambda _: {"state": "lost", "next_step": "", "expected_date": ""})
    except ValueError:
        return
    raise AssertionError("should raise")
