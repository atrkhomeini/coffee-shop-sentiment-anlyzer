# src/config.py
import os
import yaml

# --- Project Details ---
# Replace with your actual Google Cloud Project ID
GCP_PROJECT_ID = "coffee-shop-467807" 
BIGQUERY_DATASET = "coffee_shop_sentiment"
# This would be the table with your *labeled* training data
BIGQUERY_TRAINING_TABLE = "labelled" 

# --- Model & Tokenizer Paths ---
# These paths are relative to the project's root directory
MODEL_PATH = "models/sentiment_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"

# --- Model Parameters ---
# Ensure this matches the value used during your model training
MAX_LENGTH = 10000 

# --- Gemini API Key ---
# Load GEMINI_API_KEY from the YAML file
key_file_path = os.path.join(os.path.dirname(__file__), '../key/gemini_api_key.yml')
with open(key_file_path, 'r') as file:
    gemini_key_data = yaml.safe_load(file)
GEMINI_API_KEY = gemini_key_data.get('GEMINI_API_KEY')
