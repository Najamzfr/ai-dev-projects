"""Security utilities."""
import re
from typing import Optional


def sanitize_username(username: str) -> str:
    """Sanitize username input."""
    # Remove leading/trailing whitespace
    username = username.strip()
    
    # Convert to uppercase
    username = username.upper()
    
    # Remove any characters that aren't alphanumeric or underscore
    username = re.sub(r'[^A-Z0-9_]', '', username)
    
    return username


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """Validate username format.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    
    if len(username) > 20:
        return False, "Username must be 20 characters or less"
    
    # Check for valid characters (alphanumeric and underscore only)
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        return False, "Username must contain only alphanumeric characters and underscores"
    
    return True, None


def validate_score(score: int, min_score: int = 0, max_score: int = 999999) -> tuple[bool, Optional[str]]:
    """Validate score range.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if score < min_score:
        return False, f"Score must be at least {min_score}"
    
    if score > max_score:
        return False, f"Score must be at most {max_score}"
    
    return True, None


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize general text input to prevent XSS."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags and content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Truncate to max length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

