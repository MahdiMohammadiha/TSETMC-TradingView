from datetime import datetime, time as dtime, timedelta


TRADING_START = dtime(12, 30)  # Trading session start time
TRADING_END = dtime(18, 0)  # Trading session end time


def is_within_trading_hours() -> bool:
    """Check if the current time is within trading session hours."""
    now = datetime.now().time()
    return TRADING_START <= now <= TRADING_END


def seconds_until_next_start() -> float:
    """Calculate seconds until the next trading session starts."""
    now = datetime.now()
    next_start = now.replace(
        hour=TRADING_START.hour, minute=TRADING_START.minute, second=0, microsecond=0
    )

    if now.time() >= TRADING_END:
        # Today's session has ended → start tomorrow
        next_start += timedelta(days=1)
    elif now.time() < TRADING_START:
        # Before today's session → wait until it starts
        pass
    else:
        # Inside trading session → no wait
        return 0

    return (next_start - now).total_seconds()
