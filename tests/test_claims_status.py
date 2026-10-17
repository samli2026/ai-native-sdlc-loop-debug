import unittest

from src.claims_status import get_status


class ClaimsStatusTest(unittest.TestCase):
    def test_returns_three_fields(self):
        out = get_status("C-1", lambda _: {
            "state": "in_review", "next_step": "call",
            "expected_date": "2026-07-01", "extra": "dropped",
        })
        self.assertEqual(set(out), {"status", "next_step", "expected_date"})

    def test_rejects_unknown_state(self):
        with self.assertRaises(ValueError):
            get_status("C-1", lambda _: {"state": "lost", "next_step": "", "expected_date": ""})
