AUDIT = []


def record(actor, action, **fields):
    AUDIT.append({"actor": actor, "action": action, **fields})
    return AUDIT[-1]
