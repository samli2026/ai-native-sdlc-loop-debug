from src.audit import record

MAX_ROWS = 10_000
COLUMNS = ["claim_id", "status", "received_at", "next_step", "expected_date"]


def to_csv(rows):
    lines = [",".join(COLUMNS)]
    for row in rows:
        lines.append(",".join(str(row.get(c, "")) for c in COLUMNS))
    return "\n".join(lines) + "\n"


def export(rows, actor="operator", date_range=("", "")):
    if len(rows) > MAX_ROWS:
        raise ValueError("too many rows; narrow the range")
    record(actor, "claims.export", rows=len(rows), date_range=date_range)
    return to_csv(rows)
