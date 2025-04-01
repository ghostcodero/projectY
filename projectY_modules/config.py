"""
Configuration management for ProjectY.
Handles environment variables validation and access.
"""

import os

# Module level variables initialized as None
OPENAI_API_KEY = None
SERPAPI_KEY = None
PERPLEXITY_API_KEY = None

def validate_and_load_env_vars():
    """Check that all required environment variables are set and load them into global variables."""
    global OPENAI_API_KEY, SERPAPI_KEY, PERPLEXITY_API_KEY
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for GPT-4 and Whisper",
        "SERPAPI_KEY": "SerpAPI key for search results",
        "PERPLEXITY_API_KEY": "Perplexity API key for verification"
    }
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"{var} ({description})")
    
    if missing:
        raise ValueError(
            "Missing required environment variables:\n" + 
            "\n".join(f"- {key}" for key in missing)
        )
    
    # Only set the global variables if all keys exist
    global_vars = globals()
    for var in required_vars:
        global_vars[var] = os.getenv(var)

# Load environment variables when module is imported
validate_and_load_env_vars() 