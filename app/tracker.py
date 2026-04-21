_session = {
    "total_requests": 0,
    "total_tokens": 0,
    "total_cost_usd": 0.0,
}


def record_usage(usage_entry: dict):
    _session["total_requests"] += 1
    _session["total_tokens"] += usage_entry.get("total_tokens", 0)
    _session["total_cost_usd"] += usage_entry.get("cost_usd", 0.0)


def get_session_totals() -> dict:
    return dict(_session)
