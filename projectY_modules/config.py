"""
Configuration management for ProjectY.
Handles environment variables validation and access.
"""

import os
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

# Module level variables initialized as None
OPENAI_API_KEY = None
PERPLEXITY_API_KEY = None

def validate_and_load_env_vars():
    """Check that all required environment variables are set and load them into global variables."""
    global OPENAI_API_KEY, PERPLEXITY_API_KEY
    
    logger.debug("Starting environment variable validation")
    
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for GPT-4 and Whisper",
        "PERPLEXITY_API_KEY": "Perplexity API key for verification"
    }
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"{var} ({description})")
            logger.warning(f"Missing environment variable: {var}")
        else:
            logger.debug(f"Found environment variable: {var}")
    
    if missing:
        error_msg = "Missing required environment variables:\n" + "\n".join(f"- {key}" for key in missing)
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Only set the global variables if all keys exist
    global_vars = globals()
    for var in required_vars:
        global_vars[var] = os.getenv(var)
        logger.debug(f"Loaded environment variable: {var}")

    logger.info("Successfully validated and loaded all environment variables")

# Load environment variables when module is imported
validate_and_load_env_vars() 