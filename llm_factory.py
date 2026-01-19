# LLM Factory - Factory pattern for multiple LLM providers
"""
Factory module for creating LLM instances from different providers.
Supports: Groq, OpenAI, and Ollama (local).
"""

import os
from typing import Optional

# Import Groq (required - main provider)
from langchain_groq import ChatGroq

# OpenAI is optional - only import if available
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    ChatOpenAI = None

# Ollama is optional - only import if available
try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ChatOllama = None


def get_llm(provider: str, model: str, temperature: float = 0.7) -> Optional[object]:
    """
    Factory function to create LLM instances based on provider.
    
    Args:
        provider: LLM provider name ("groq", "openai", "ollama")
        model: Model name (e.g., "llama-3.3-8b-versatile", "gpt-4", "llama2")
        temperature: Temperature for generation (0.0-1.0)
    
    Returns:
        LLM instance (ChatGroq, ChatOpenAI, or ChatOllama)
    
    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    provider = provider.lower()
    
    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return ChatGroq(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    
    elif provider == "openai":
        if not OPENAI_AVAILABLE:
            raise ValueError(
                "OpenAI is not available. Install it with: pip install langchain-openai"
            )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    
    elif provider == "ollama":
        if not OLLAMA_AVAILABLE:
            raise ValueError(
                "Ollama is not available. Install it with: pip install langchain-ollama"
            )
        # Ollama runs locally, no API key needed
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Supported: 'groq', 'openai', 'ollama'")


def get_available_models(provider: str) -> list:
    """
    Returns list of available models for a given provider.
    
    Args:
        provider: LLM provider name
    
    Returns:
        List of model names
    """
    provider = provider.lower()
    
    models = {
        "groq": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768"
        ],
        "openai": [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-3.5-turbo",
            "gpt-4o"
        ],
        "ollama": [
            "llama2",
            "llama3",
            "mistral",
            "codellama",
            "neural-chat"
        ]
    }
    
    return models.get(provider, [])


def validate_provider_config(provider: str):
    """
    Validates if provider is properly configured.
    
    Args:
        provider: LLM provider name
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    provider = provider.lower()
    
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            return False, "GROQ_API_KEY not found in .env file"
        return True, ""
    
    elif provider == "openai":
        if not OPENAI_AVAILABLE:
            return False, "langchain-openai not installed. Run: pip install langchain-openai"
        if not os.getenv("OPENAI_API_KEY"):
            return False, "OPENAI_API_KEY not found in .env file"
        return True, ""
    
    elif provider == "ollama":
        if not OLLAMA_AVAILABLE:
            return False, "langchain-ollama not installed. Run: pip install langchain-ollama"
        # Check if Ollama is running (basic check)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            import requests
            response = requests.get(f"{base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                return True, ""
            else:
                return False, f"Ollama not responding at {base_url}"
        except Exception as e:
            return False, f"Ollama not accessible: {str(e)}"
    
    return False, f"Unknown provider: {provider}"

