# src/config.py
import os
import yaml

def load_api_key():
    """
    Loads the Gemini API key.
    Prioritizes the environment variable for production/CI/CD environments.
    Falls back to the local YAML file for local development.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ Loaded API key from environment variable.")
        return api_key
    
    print("Trying to load API key from local file...")
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        key_path = os.path.join(base_dir, "key", "gemini_api_key.yml")
        with open(key_path, "r") as f:
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
# --- UPDATED: Changed model filename to the modern .keras format ---
MODEL_PATH = "models/sentiment_model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"

# --- Model Parameters ---
MAX_LENGTH = 50 

# --- Gemini API Key ---
GEMINI_API_KEY = load_api_key()
