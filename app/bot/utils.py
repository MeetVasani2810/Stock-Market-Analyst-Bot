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
