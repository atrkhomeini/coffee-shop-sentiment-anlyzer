# src/config.py
import os
from dotenv import load_dotenv

# This command automatically finds and loads the variables from your .env file
load_dotenv()

# --- Project Details ---
GCP_PROJECT_ID = "coffee-shop-467807" 
BIGQUERY_DATASET = "coffee_shop_sentiment"
BIGQUERY_TRAINING_TABLE = "labelled" 

# --- Model & Tokenizer Paths ---
MODEL_PATH = "models/sentiment_model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"

# --- Model Parameters ---
MAX_LENGTH = 50 

# --- Gemini API Key ---
# This now directly reads the key loaded from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

