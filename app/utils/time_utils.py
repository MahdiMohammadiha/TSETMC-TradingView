def round_timestamp(ts: int, interval: str = "1m") -> int:
    """
    Round a timestamp (in milliseconds) to the beginning of the interval.
    """
    ms = {
        "1m": 60_000,
        "5m": 5 * 60_000,
        "15m": 15 * 60_000,
        "30m": 30 * 60_000,
        "1h": 60 * 60_000,
        "1d": 24 * 60 * 60_000,
    }.get(interval)

    if ms is None:
        raise ValueError(f"Unsupported interval: {interval}")

    return ts - (ts % ms)
