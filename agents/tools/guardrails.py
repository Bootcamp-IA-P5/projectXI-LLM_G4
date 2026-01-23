"""
Content validation guardrails.
"""
from typing import Tuple, List


# Guardrails configuration
GUARDRAILS = {
    "length": {
        "Blog": (800, 2000),
        "LinkedIn": (150, 300),
        "Twitter": (1, 280),
        "Instagram": (100, 150)
    },
    "forbidden_words": [
        "garantizado", "100%", "gratis", "urgente", "click aquí",
        "guaranteed", "free", "urgent", "click here"
    ],
    "required_elements": {
        "Blog": ["introduction", "conclusion"],
        "LinkedIn": ["hashtag"],
        "Twitter": ["hashtag"],
        "Instagram": ["hashtag", "emoji"]
    }
}


def validate_content(content: str, platform: str) -> Tuple[bool, List[str]]:
    """
    Validate generated content against guardrails.
    
    Args:
        content: Generated content text
        platform: Target platform (Blog, LinkedIn, Twitter, Instagram)
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # 1. Check length
    word_count = len(content.split())
    if platform in GUARDRAILS["length"]:
        min_len, max_len = GUARDRAILS["length"][platform]
        if word_count < min_len:
            errors.append(f"Content too short: {word_count} words (min: {min_len})")
        elif word_count > max_len:
            errors.append(f"Content too long: {word_count} words (max: {max_len})")
    
    # 2. Check forbidden words
    content_lower = content.lower()
    for word in GUARDRAILS["forbidden_words"]:
        if word.lower() in content_lower:
            errors.append(f"Forbidden word detected: '{word}'")
    
    # 3. Check required elements
    if platform in GUARDRAILS["required_elements"]:
        required = GUARDRAILS["required_elements"][platform]
        
        if "hashtag" in required and "#" not in content:
            errors.append("Missing required hashtags")
        
        if "emoji" in required:
            # Simple emoji detection (checks for common emoji ranges)
            has_emoji = any(ord(char) > 127 for char in content)
            if not has_emoji:
                errors.append("Missing emojis (recommended for Instagram)")
    
    # 4. Check for potential hallucinations
    hallucination_markers = [
        "according to studies",
        "según estudios",
        "research shows",
        "la investigación muestra",
        "statistics show",
        "las estadísticas muestran"
    ]
    
    for marker in hallucination_markers:
        if marker in content_lower and "http" not in content_lower:
            errors.append(f"Claims without sources: '{marker}' found but no links provided")
            break
    
    return len(errors) == 0, errors


def check_tone_consistency(content: str, expected_tone: str) -> Tuple[bool, str]:
    """
    Check if content matches expected tone.
    
    Args:
        content: Generated content
        expected_tone: Expected tone (professional, friendly, bold)
    
    Returns:
        Tuple of (matches, feedback)
    """
    tone_indicators = {
        "professional": ["excelente", "innovador", "solución", "excellent", "innovative", "solution"],
        "friendly": ["hola", "te", "juntos", "hello", "you", "together"],
        "bold": ["revolucionar", "transformar", "cambiar", "revolutionize", "transform", "change"]
    }
    
    if expected_tone.lower() not in tone_indicators:
        return True, "Tone check not applicable"
    
    content_lower = content.lower()
    indicators = tone_indicators[expected_tone.lower()]
    
    matches = sum(1 for indicator in indicators if indicator in content_lower)
    
    if matches >= 2:
        return True, f"Tone matches '{expected_tone}'"
    else:
        return False, f"Tone doesn't match '{expected_tone}' (found {matches} indicators)"
