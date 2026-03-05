"""Utility functions for YouTube NotebookLM automation."""


def safe_str(text: str) -> str:
    """
    Safely encode text for console logging on Windows.
    Handles Unicode characters that may cause encoding errors.
    
    Args:
        text: Text that may contain Unicode characters (emojis, special chars)
        
    Returns:
        Text safe for console output (ASCII with replacements)
    """
    if text is None:
        return ""
    
    try:
        # Try to encode to ASCII, replace problematic chars with '?'
        return text.encode('ascii', errors='replace').decode('ascii')
    except Exception:
        # If that fails, manually filter out non-ASCII
        return ''.join(char if ord(char) < 128 else '?' for char in str(text))
