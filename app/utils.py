from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

def convert_to_ist(dt: datetime) -> datetime:
    """Convert datetime to IST timezone"""
    if dt.tzinfo is None:
        # If naive datetime, assume UTC
        dt = pytz.utc.localize(dt)
    return dt.astimezone(IST)

def get_current_ist_time() -> datetime:
    """Get current time in IST"""
    return datetime.now(IST)

def datetime_to_ist_string(dt: datetime) -> str:
    """Convert datetime to IST string representation"""
    ist_dt = convert_to_ist(dt)
    return ist_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
