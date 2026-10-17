CACHE_SECONDS = 60
STATES = ("received", "in_review", "approved", "paid")


def get_status(claim_id, fetch):
    claim = fetch(claim_id)
    if claim["state"] not in STATES:
        raise ValueError("unknown state")
    return {
        "status": claim["state"],
        "next_step": claim["next_step"],
        "expected_date": claim["expected_date"],
    }
