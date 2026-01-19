def smart_split_message(text: str, limit: int = 4000) -> list[str]:
    """
    Splits a long message into chunks that respect Telegram's message limit.
    Tries to split at newlines to preserve formatting.
    
    Args:
        text: The text to split
        limit: Max characters per chunk (default 4000 to be safe, max is 4096)
        
    Returns:
        List of text chunks
    """
    if len(text) <= limit:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # split by lines to preserve formatting
    lines = text.split('\n')
    
    for line in lines:
        # Check if adding this line (plus newline) would exceed limit
        if len(current_chunk) + len(line) + 1 > limit:
            # If current chunk is not empty, save it
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            # If the line itself is massive (longer than limit), we must hard split it
            if len(line) > limit:
                # Split line into limit-sized pieces
                for i in range(0, len(line), limit):
                    chunks.append(line[i:i+limit])
            else:
                current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

# --- TIMEFRAME CONSTANTS ---

TIMEFRAME_ALIASES = {
    # Minutes
    "1min": "1min", "1m": "1min",
    "3min": "3min", "3m": "3min",
    "5min": "5min", "5m": "5min",
    "15min": "15min", "15m": "15min",
    "30min": "30min", "30m": "30min",
    
    # Hours
    "1hour": "1h", "1h": "1h",
    "2hour": "2h", "2h": "2h",
    "4hour": "4h", "4h": "4h",
    "12hour": "12h", "12h": "12h",
    
    # Days
    "1day": "1day", "1d": "1day", "day": "1day",
    
    # Weeks
    "1week": "1week", "1w": "1week", "week": "1week",
    
    # Months
    "1month": "1month", "1M": "1month", "month": "1month"
}

DISPLAY_NAMES = {
    "1min": "1 Minute",
    "3min": "3 Minutes",
    "5min": "5 Minutes",
    "15min": "15 Minutes",
    "30min": "30 Minutes",
    "1h": "1 Hour",
    "2h": "2 Hours",
    "4h": "4 Hours",
    "12h": "12 Hours",
    "1day": "Daily",
    "1week": "Weekly",
    "1month": "Monthly"
}

SUPPORTED_TIMEFRAMES_MSG = """
📊 **Supported Timeframes:**

⏱️ **Minutes:** 1min, 5min, 15min, 30min
⏰ **Hours:** 1hour, 2hour, 4hour, 12hour
📅 **Daily:** 1day
📆 **Weekly:** 1week
📆 **Monthly:** 1month

💡 *Example:* `/technical BTC 15min`
"""

def parse_timeframe(user_input: str) -> tuple[str | None, str | None, bool]:
    """
    Parse user's timeframe input and return API-compatible format.
    
    Args:
        user_input: str like "15min", "1h", "1day"
    
    Returns:
        tuple: (timeframe_for_api, display_name, is_valid)
    """
    if not user_input:
        return None, None, False
        
    cleaned_input = user_input.lower().strip()
    
    # Check if input is a known alias
    if cleaned_input in TIMEFRAME_ALIASES:
        api_timeframe = TIMEFRAME_ALIASES[cleaned_input]
        return api_timeframe, DISPLAY_NAMES.get(api_timeframe, api_timeframe), True
        
    return None, None, False
