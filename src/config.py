# src/config.py
import os
import yaml

def load_api_key():
    """
    Loads the Gemini API key.
    Prioritizes the environment variable for production/CI/CD environments.
    Falls back to the local YAML file for local development.
    """
    # 1. Check for the environment variable first (used by Docker/Cloud Run)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ Loaded API key from environment variable.")
        return api_key
    
    # 2. If no environment variable, fall back to the local file
    print("Trying to load API key from local file...")
    try:
        with open("key/gemini_api_key.yml", "r") as f:
            config = yaml.safe_load(f)
            print("✅ Loaded API key from local key/gemini_api_key.yml file.")
            return config['gemini_api_key']
    except (FileNotFoundError, KeyError, TypeError):
        print("⚠️ WARNING: API key not found in environment variables or local file.")
        return None

# --- Project Details ---
GCP_PROJECT_ID = "coffee-shop-467807" 
BIGQUERY_DATASET = "coffee_shop_sentiment"
BIGQUERY_TRAINING_TABLE = "labelled" 

# --- Model & Tokenizer Paths ---
MODEL_PATH = "models/sentiment_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"

# --- Model Parameters ---
MAX_LENGTH = 50 

# --- Gemini API Key ---
GEMINI_API_KEY = load_api_key()
