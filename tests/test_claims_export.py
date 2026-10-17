import unittest

from src.audit import AUDIT
from src.claims_export import COLUMNS, MAX_ROWS, export


def row(**kw):
    base = {"claim_id": "C-1", "status": "in_review", "received_at": "2026-06-02",
            "next_step": "call", "expected_date": "2026-07-01", "pii": "x"}
    base.update(kw)
    return base


class ClaimsExportTest(unittest.TestCase):
    def test_columns_exact_and_no_pii(self):
        out = export([row()]).splitlines()[0].split(",")
        self.assertEqual(out, COLUMNS)

    def test_caps_rows(self):
        with self.assertRaises(ValueError):
            export([row()] * (MAX_ROWS + 1))

    def test_writes_audit(self):
        AUDIT.clear()
        export([row()], actor="ops-1", date_range=("2026-06-01", "2026-06-30"))
        self.assertEqual(AUDIT[-1]["action"], "claims.export")
        self.assertEqual(AUDIT[-1]["actor"], "ops-1")
